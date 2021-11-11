import logging
import math
import traceback

from db_manager import ManagedSession
from server.config import is_configured, configuration_for
from server.models import WatchedTicker, Trade
from server.enums.trim_size import TrimSize
from server.providers.ib_provider import IBProvider
from server.provider_actions import trade_failed
from server.queues import inbound_queue
from server.calculations import calculate_position_sizes
from threading import Thread
from time import sleep

log = logging.getLogger(__name__)

class Switchboard:
  """
  The switchboard is responsible for routing client requests to the
  relevant provider. All instructions to buy, trim, sell etc will go
  through the switchboard
  """

  def __init__(self):
    self.tws = IBProvider(inbound_queue)
    self.connected = False

  def start(self, app):
    """ The main entry point to the background thread which is responsible
    for sending and receiving messages to and from TWS
    """

    log.debug("[Switchboard] Starting")
    switchboard_thread = Thread(daemon=True, target=self.initialise, args=[app])
    switchboard_thread.start()

  def is_connected(self):
    return self.connected

  def initialise(self, app):
    """
    The main loop that runs in the background thread. This is the loop
    which will listen for messages from other parts of the app
    """

    log.debug("[Switchboard] Background thread started")
    with app.app_context():
      log.debug("[Switchboard] Checking configuration")
      
      while not self.connected:
        try:
          if (is_configured()):
            log.info("[Switchboard] App is configured. Connecting to TWS")
            self.tws.connect(app)

            while not self.tws.is_connected():
              log.debug("[Switchboard] Waiting for provider to connect")
              sleep(1)

            self.connected = True
            self.start_listening()

          else:
            log.info("[Switchboard] App not configured. Sleeping for 5 seconds")
            sleep(5)

        except ConnectionError:
          log.error("[Switchboard] Received a disconect from provider. Restarting")
          self.connected = False
          sleep(5)

  def start_listening(self):
    """
    Registers for real-time feeds for existing watched tickers,
    and then starts listening for commands from other parts of
    the app
    """

    log.info("[Switchboard] Connected and listening")

    fetch = configuration_for("fetch_account_size").value
    load_account_data = int(fetch) == 1
    if load_account_data:
      self.tws.load_account_data()
    else:
      log.info(f'[Switchboard] Skipping account loading. Fixed capital size being used')

    self.watch_existing_tickers()

    while True:
      try:
        with ManagedSession() as session:
          message = inbound_queue.get(block=True)
          log.debug(f'[Switchboard] Received {message.message_type} message')

          if message.message_type == "WATCH":
            self.watch(message.watched_ticker)

          elif message.message_type == "UNWATCH":
            self.unwatch(message.watched_ticker)

          elif message.message_type == "BUY":
            self.buy(message.watched_ticker, message.trade)

          elif message.message_type == "TRIM":
            self.trim(message.trade, message.amount)

          elif message.message_type == "SELL":
            self.sell(message.trade, message.amount)

          elif message.message_type == "CANCEL":
            self.cancel(message.trade)

          # Received an error message from a provider
          elif message.message_type == "PROVIDER_ERROR":
            log.error("[Switchboard] Received error from provider")
            self.connected = False
            raise message.exception



      except ConnectionError as e:
        # Looks like the connection terminated so we can't just continue. We'll
        # need to restart the whole process
        self.connected = False
        raise e
      except:
        print("Error in background thread")
        log.error("An unexpected error occurred in the background thread")
        traceback.print_exc()

  def watch_existing_tickers(self):
    """
    Makes a request to the provider to start streaming data for tickers that
    are already being watched
    """

    log.debug("[Switchboard] Requesting real-time feed for existing watched tickers")
    watches = WatchedTicker.query.all()

    for watched_ticker in watches:
      self.watch(watched_ticker)

  #
  # Message actions
  #

  def buy(self, watched_ticker: WatchedTicker, trade: Trade):
    """
    Submits a "BUY" request to the provider
    """

    log.debug(f"[Switchboard] Buying {trade.ticker}")

    if watched_ticker.price == watched_ticker.low:
      # We can't buy as we'd immediately be stopped out so we'll fail
      # this trade
      trade_failed(trade, "Current price is the same as the stop loss price")
      return


    position_sizes = calculate_position_sizes(watched_ticker)

    # Update the trade record with what we can. The provider
    # will set the order ID's as we don't know them in the
    # switchboard
    with ManagedSession() as session:
      trade = Trade.find(session, trade.id)
      trade.amount_ordered = position_sizes.get("position_size")
      trade.remaining = trade.amount_ordered
      trade.current_stop = position_sizes.get("stop_loss")

    self.tws.buy(
      trade=trade,
      position_size=position_sizes.get("position_size"),
      stop_loss=position_sizes.get("stop_loss"))

  def cancel(self, trade: Trade):
    """
    Requests that the entire order be cancelled. This will simply cancel
    an order, and will not attempt to sell any existing positions
    """
    log.debug(f"[Switchboard] Cancelling order for {trade.ticker}")
    self.tws.cancel_order(trade.order_id)
    self.tws.cancel_order(trade.stop_order_id)


  def sell(self, trade: Trade, amount: float):
    """
    Requests that the provider sell the specified amount
    """
    log.debug(f"[Switchboard] Placing a SELL order for {amount} {trade.ticker}")

    if trade.current_position_size == amount:
      # This will sell everything, so we'll just close the
      # entire position
      log.debug(f"[Switchboard] Closing position, SELL request was for full position")
      self.tws.close_position(trade)
    
    else:
      self.tws.sell(
        trade=trade,
        amount=amount)

  def trim(self, trade: Trade, amount: TrimSize):
    """
    Trim down a position by a specified amount. Trimming a position consists
    of a few steps:

    1. Sell the desired amount
    2. Cancel the existing stop order
    3. Create a new stop order at break even (if this is the first trim)
    """

    log.debug("[Switchboard] Trimming down position")

    # Calculate the trim size, ensuring it doesn't exceed the amount we have
    # left. If it does, we'll sell whatever is left
    trim_size = math.ceil(trade.amount_ordered * amount.value)

    if trim_size > trade.current_position_size:
      # We're going to simply close out our position
      self.tws.close_position(trade)

    else:
      stop_size = trade.current_position_size - trim_size
      self.tws.trim(
        trade=trade,
        trim_size=trim_size,
        stop_position=trade.price_at_order,
        stop_size=stop_size)



  def watch(self, watched_ticker: WatchedTicker):
    """
    Requests that the provider register for a real-time feed for the
    given ticker
    """
    log.debug(f"[Switchboard] Requesting real-time feed for {watched_ticker.ticker}")
    self.tws.request_realtime_feed(watched_ticker)

  def unwatch(self, watched_ticker: WatchedTicker):
    """
    Requests that the provider stop receiving real-time feeds for
    the given ticker
    """
    log.debug(f"[Switchboard] Requesting a stop to real-time feed for {watched_ticker.ticker}")
    self.tws.stop_realtime_feed(watched_ticker)