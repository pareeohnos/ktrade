import logging
from application import db
from ibapi.client import Order
from ibapi.contract import Contract
from server.providers.provider_interface import ProviderInterface
from server.config import configuration_for
from server.providers.ib.api import IBApi
from server.models import WatchedTicker, Trade
from server.queue_messages.provider_error_message import ProviderErrorMessage
from server.provider_actions import update_order_ids
from threading import Thread
from time import sleep

log = logging.getLogger(__name__)

class IBProvider(ProviderInterface):
  def __init__(self, switchboard_queue):
    self.switchboard_queue = switchboard_queue
    self.api = IBApi(self)
    self.connected = False

  def is_connected(self):
    """
    Returns whether or not the connection has been established
    to the TWS client
    """
    return self.connected

  def connect(self, app):
    """
    Attempt to connect to TWS. This will start up a background
    thread where the TWS connection will stay active
    """
    log.info("[IB] Connecting to TWS")

    host = configuration_for("tws_host").value
    port = configuration_for("tws_port").value
    self.api.connect(host, int(port), 1)

    api_thread = Thread(target=self.ib_loop, daemon=True, args=[app])
    api_thread.start()

    log.debug("[IB] Loading next request ID")
    self.api.reqIds(-1)

    # Wait until we've had a response with the next order ID before we do anything else
    while not isinstance(self.api.req_id, int):
      log.debug("[IB] Waiting for connection")
      sleep(1)

    # We're all done
    self.connected = True

  def request_realtime_feed(self, watched_ticker: int):
    """
    Requests a real-time feed for the specified watched ticker.
    """
    req_id = self.api.next_request_id()
    contract = self.build_contract(watched_ticker.ticker)

    log.debug("[IB] Requesting historical data")
    self.api.request_historical_data(contract=contract, watched_ticker=watched_ticker)

    log.debug("[IB] Registering for real-time feed")
    self.api.request_realtime_feed(contract=contract, watched_ticker=watched_ticker)

  def stop_realtime_feed(self, watched_ticker: WatchedTicker):
    """
    If a real-time feed has been requested previously, it will be cancelled.
    """
    log.debug(f"[IB] Cancelling subscription to {watched_ticker.ticker} data")
    self.api.stop_realtime_feed(watched_ticker)

  def buy(self, trade: Trade, position_size: float, stop_loss: float):
    """
    Prepares the orders required to send to TWS, to purchase the shares and
    setup the stop loss for the low of the day.
    """
    contract = self.build_contract(trade.ticker)

    # The main buy order
    order_id = self.api.next_request_id()
    order = Order()
    order.orderId = order_id
    order.action = "BUY"
    order.totalQuantity = position_size
    order.orderType = "MKT"
    order.transmit = False

    # And the stop loss
    stop_order = Order()
    stop_order.action = "SELL"
    stop_order.orderType = "STP"
    stop_order.auxPrice = stop_loss
    stop_order.totalQuantity = position_size
    stop_order.orderId = self.api.next_request_id()
    stop_order.parentId = order_id
    stop_order.transmit = True

    # And go!
    self.api.place_order(trade, contract, order)
    self.api.place_order(trade, contract, stop_order)

    # Update our trade record to add the order ID's
    update_order_ids(
      trade,
      order_id=order.orderId,
      stop_order_id=stop_order.orderId)

  def cancel_order(self, order_id: int):
    """
    Cancels the specified order ID
    """
    self.api.cancel_order(order_id)

  def sell(self, trade: Trade, amount: float):
    """
    Places a SELL order with TWS for the specified amount.
    """
    contract = self.build_contract(trade.ticker)

    sell_order = Order()
    sell_order.action = "SELL"
    sell_order.orderType = "MKT"
    sell_order.orderId = self.api.next_request_id()
    sell_order.totalQuantity = amount
    sell_order.transmit = True

    self.api.place_order(trade, contract, sell_order)

  def trim(self, trade: Trade, trim_size: float, stop_position: float, stop_size: float):
    """
    Prepares the modifications to the original orders to trim the position
    size by the desired amount. This will also adjust the stop loss to reduce
    its size by the amount being trimmed
    """

    # We're good to go. Lets modify our stop loss to break even
    contract = self.build_contract(trade.ticker)

    # Sell our portion of shares
    log.debug(f"[IB] Selling {trim_size} shares")
    sell_order = Order()
    sell_order.action = "SELL"
    sell_order.orderType = "MKT"
    sell_order.orderId = self.api.next_request_id()
    sell_order.totalQuantity = trim_size
    sell_order.transmit = True
    self.api.place_order(trade, contract, sell_order)

    # Move stop
    log.debug(f"[IB] Moving stop loss to {trade.price_at_order}, reducing to {stop_size} shares")
    stop_order = Order()
    stop_order.action = "SELL"
    stop_order.orderType = "STP"
    stop_order.auxPrice = trade.price_at_order
    stop_order.totalQuantity = stop_size
    stop_order.orderId = self.api.next_request_id()
    stop_order.transmit = True

    # Had problems modifying the existing order, so safer to just
    # cancel the old one, and setup a new one
    self.api.cancel_order(trade.stop_order_id)
    self.api.place_order(trade, contract, stop_order)
    
    # Update the stop order ID for later
    update_order_ids(
      trade,
      stop_order_id=stop_order.orderId
    )

  def close_position(self, trade: Trade):
    """
    Sells the remainder of the open trade
    """

    log.debug(f"[IB] Closing position of {trade.ticker}")
    
    contract = self.build_contract(trade.ticker)
    sell_order = Order()
    sell_order.action = "SELL"
    sell_order.orderType = "MKT"
    sell_order.totalQuantity = trade.current_position_size
    sell_order.orderId = self.api.next_request_id()
    sell_order.transmit = True
    self.api.place_order(trade, contract, sell_order)

    # Now make sure our stop loss is also cancelled
    self.api.cancel_order(trade.stop_order_id)

    update_order_ids(
      trade,
      stop_order_id=None,
      order_id=None)
  #
  # Everything below is part of the private API and should not
  # be called from outside this class
  #

  def ib_loop(self, app):
    """
    Starts the IB Api client
    """

    try:
      with app.app_context():
        self.api.run()
    
    except ConnectionError as e:
      self.connected = False
      log.error("[IB] Connection to TWS failed. Exiting")
      self.switchboard_queue.put(ProviderErrorMessage(exception=e))
      

  def build_contract(self, ticker: str):
    """
    Builds a new `Contract` object required for placing orders,
    or other requests
    """

    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    return contract

  def load_account_data(self):
    """
    Loads a summary of the account that is logged in on TWS.
    """

    log.debug("[IB] Requesting account summary. Only getting USD value")
    self.api.reqAccountSummary(self.api.next_request_id(), "All", "$LEDGER:USD")