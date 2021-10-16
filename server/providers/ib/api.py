import logging
import re

from ibapi.client import EClient, TickAttribLast, TickAttrib, Order, ExecutionFilter
from ibapi.wrapper import EWrapper, TickType, TickTypeEnum, BarData
from ibapi.contract import Contract

from server.models import WatchedTicker, Trade
from server.provider_actions import trade_failed, trade_bought, trade_sold, trade_on_hold, trade_filled, trade_status_changed, ticker_updated
from server.providers.ib.account_summary_actions import AccountSummaryActions
from server.providers.ib.historical_data_actions import HistoricalDataActions
from server.enums.trade_status import TradeStatus
from server.price_cache import PriceCache

log = logging.getLogger(__name__)

class IBApi(EWrapper, EClient):
  """
  The main API class for interacting with TWS
  """

  #
  # Public API methods that are not overrides of the `EWrapper` or
  # `EClient` classes
  #

  def __init__(self, parent):
    EClient.__init__(self, self)

    self.req_id = None
    self.parent = parent

    self.ticker_to_request = {}
    self.request_to_ticker = {}
    self.historical_data_requests = {}
    self.open_orders = {}
    self.pending_cancellations = set()
    self.price_cache = PriceCache()

  def next_request_id(self):
    self.req_id += 1
    return self.req_id

  def request_historical_data(self, contract: Contract, watched_ticker: WatchedTicker):
    """
    Makes a request to retrieve historical data for the past 20
    days for the specified watched ticker
    """
    req_id = self.next_request_id()
    self.price_cache.init_cache_for_ticker(watched_ticker.id)
    self.historical_data_requests[req_id] = {
      "ticker": contract.symbol,
      "bars": [],
      "watched_ticker": watched_ticker
    }

    self.reqHistoricalData(req_id, contract, "", "20 D", "1 day", "TRADES", 1, 1, False, [])

  def request_realtime_feed(self, contract: Contract, watched_ticker: WatchedTicker):
    """
    Sends a request to TWS to start sending a realtime feed of data for
    the given ticker
    """
    req_id = self.next_request_id()

    self.price_cache.init_cache_for_ticker(watched_ticker.id)
    self.request_to_ticker[req_id] = watched_ticker
    self.ticker_to_request[watched_ticker.id] = req_id
    self.reqMktData(req_id, contract, "233", False, False, [])

  def stop_realtime_feed(self, watched_ticker):
    """
    Sends a request to TWS to stop sending real-time feeds for the
    given ticker
    """
    sub_id = self.ticker_to_request.get(watched_ticker.id)
    if sub_id != None:
      self.cancelMktData(sub_id)
      del self.ticker_to_request[watched_ticker.id]
      del self.request_to_ticker[sub_id]
      self.price_cache.delete_watched_ticker(watched_ticker.id)

  def place_order(self, trade: Trade, contract: Contract, order: Order):
    """
    Sends a request to TWS to place an order, and records the order ID
    to keep track of any responses we receive
    """

    log.debug("[TWS] Placing order with TWS")
    self.open_orders[order.orderId] = {
      "order": order,
      "trade": trade
    }

    self.placeOrder(order.orderId, contract, order)

  def cancel_order(self, order_id: int):
    """
    Submit a request for TWS to cancel an order
    """
    self.pending_cancellations.add(order_id)
    self.cancelOrder(order_id)

  #
  # The following methods are all overridden from either the EWrapper or
  # EClient classes
  #

  def nextValidId(self, orderId: int):
    """
    Called by TWS to inform the client of the next available request
    ID. This will update an internal counter that is used by the main
    client for all future requests/orders
    """
    super().nextValidId(orderId)
    self.req_id = orderId


  def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
    """
    Called when the account summary that was requested has been
    returned by TWS. Handling of the response is delegated to the
    `AccountSummaryActions` class.
    """
    super().accountSummary(reqId, account, tag, value, currency)
    
    action = AccountSummaryActions()
    action.call(account=account, value=value, tag=tag)

  def connectionClosed(self):
    """
    Called when the connection to TWS is closed for one reason or another.
    Unless the app is being terminated, this is likely an error. As such,
    we will raise an exception and let the managing code above handle the
    issue
    """
    raise ConnectionError("TWS connectioned closed")

  def historicalData(self,  req_id: int, bar: BarData):
    """
    Called when a historical data bar has been received. This will accumulate
    the bars until the `historicalDataEnd` method is called
    """

    super().historicalData(req_id, bar)
    self.historical_data_requests[req_id]["bars"].append(bar)

  def historicalDataEnd(self, req_id: int, start: str, end: str):
    """
    Called when the historical data bars have been fully received. This
    method will update the watched ticker record with the latest price
    known, and also calculate the ADR
    """
    super().historicalDataEnd(req_id, start, end)
    
    request = self.historical_data_requests[req_id]
    watched_ticker = request.get("watched_ticker")

    action = HistoricalDataActions()
    prices = action.call(
      watched_ticker=watched_ticker,
      bars=request.get("bars"))

    self.price_cache.update_cached_price(watched_ticker.id, "low", prices["low"])
    self.price_cache.update_cached_price(watched_ticker.id, "high", prices["high"])
    
    del self.historical_data_requests[req_id]

  #
  # Real-time feed updates
  #
  
  def tickPrice(self, tickerId: int, field: int, price: float, attribs: TickAttrib):
    """
    Called when TWS notifies us about a change in price
    for a ticker. We will map this response back to a
    real-time request and update our data accordingly
    """
  
    super().tickPrice(tickerId, field, price, attribs)

    log.debug("[TWS] Tick price update received")
    watched_ticker = self.request_to_ticker[tickerId]
    
    if field == TickTypeEnum.LAST or field == TickTypeEnum.CLOSE:
      cached_prices = self.price_cache.cached_prices_for_ticker(watched_ticker.id)

      ticker_updated(watched_ticker, "price", price)
      self.price_cache.update_cached_price(watched_ticker.id, "price", price)

      # Update the low price if we've dropped below it
      if cached_prices["low"] == None or price < cached_prices["low"]:
        ticker_updated(watched_ticker, "low", price)
        self.price_cache.update_cached_price(watched_ticker.id, "low", price)

      # Update the high price if we've gone above it
      if cached_prices["high"] == None or price > cached_prices["high"]:
        ticker_updated(watched_ticker, "high", price)
        self.price_cache.update_cached_price(watched_ticker.id, "high", price)

  def orderStatus(self, orderId: int, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
    """
    Called when the status of an order changes. This might not always
    be called if for instance an order is filled immediately, so we
    also have to listen to the `execDetails` callback as well
    """

    super().orderStatus(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    log.debug("[TWS] Order status update received")
    open_order = self.open_orders.get(orderId)
    if open_order:
      log.debug("[TWS] Open order found")
      trade = open_order.get("trade")
      order = open_order.get("order")

      if order.orderType == "STP":
        # We won't do anything here just yet. This is just the stop loss
        # for the main trade record so nothing to update really
        return

      # We only really care about the `filled` and `inactive` at this point
      if status == "Filled":
        log.debug("[TWS] Order filled")
        trade_filled(trade)

      elif status == "Inactive":
        trade_on_hold(trade)

  def execDetails(self, reqId, contract, execution):
    """
    Called by TWS every time something is executed. This is used to track
    all changes to orders. If for instance a large order is filled over
    multiple purchases, this method will be called for each one.
    """
    super().execDetails(reqId, contract, execution)

    log.debug("[TWS] Received exec update for order")

    open_order = self.open_orders.get(execution.orderId)
    if open_order:
      trade = open_order.get("trade")

      if execution.side == "SLD":
        # This is a sell execution, so we'll decrease our stored position details
        trade_sold(trade, execution.shares)

      else:
        # This is a buy execution, so we'll increase our stored position details
        trade_bought(trade, execution.shares)

  def error(self, reqId, errorCode, errorString):
    """
    Called by TWS when there is an error filling an order.
    """
    super().error(reqId, errorCode, errorString)

    log.debug("[TWS] Received an error from TWS")
    open_order = self.open_orders.get(reqId)
    if open_order:
      trade = open_order.get("trade")

      # 202 is `cancelled` but we requested it, so it's not actually an error
      if errorCode == 202 and reqId in self.pending_cancellations:
        self.pending_cancellations.remove(reqId)
        return

      # We've receive an error so we're going to have to cancel the order. We'll
      # ignore warning codes, as they aren't a reason to terminate an order

      if 100 <= errorCode <= 449 or errorCode == 507 or 10000 <= errorCode <= 10284:
        if errorCode == 399:
          log.debug("[TWS] Received an order message error. Checking if warning")
          matches = re.search(".*(Warning:.*)", errorString, re.IGNORECASE)

          if matches is None:
            # Not a warning, just fail
            log.debug("[TWS] Cancelling order. Error is not a warning")
            trade_failed(trade, errorString)
          
          else:
            log.debug("[TWS] Keeping order open. Error was a warning")
            trade_status_changed(trade, TradeStatus(trade.order_status), matches[1])

        else:
          log.debug("[TWS] Cancelling order. Error is not a warning")
          trade_failed(trade, errorString)