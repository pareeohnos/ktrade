import logging
import traceback
from ktrade.config import is_configured, configuration_for
from time import sleep
from ktrade.queues import inbound_queue
from ktrade.queue_messages.watch_message import WatchMessage
from ibapi.client import EClient, TickAttribLast, TickAttrib, Order, ExecutionFilter
from ibapi.wrapper import EWrapper, TickType, TickTypeEnum, BarData
from ibapi.contract import Contract
from threading import Thread
from ktrade.models import WatchedTicker, Account, Trade, TradeActivity
from datetime import datetime
from application import db
import ktrade.ui as ui
import math
from functools import reduce
from fractions import Fraction
from sqlalchemy import or_

subscriptions = {}
requests = {}
historicalDataRequests = {}
executionsRequests = {}
log = logging.getLogger(__name__)

# class IBApi(EWrapper, EClient):
#   def __init__(self):
#     EClient.__init__(self, self)
#     self.req_id = None

#   def next_request_id(self):
#     self.req_id += 1
#     return self.req_id

#   def nextValidId(self, orderId: int):
#     super().nextValidId(orderId)
#     self.req_id = orderId

#   def tickString(self, tickerId: TickType, field: int, value: str):
#     super().tickString(tickerId, field, value)
  
#   def tickPrice(self, tickerId: int, field: int, price: float, attribs: TickAttrib):
#     super().tickPrice(tickerId, field, price, attribs)

#     ticker = requests[tickerId]

#     if field == TickTypeEnum.LAST or field == TickTypeEnum.CLOSE:
#       events.price_updated(ticker, price)
    
#     elif field == TickTypeEnum.HIGH:
#       events.high_updated(ticker, price)

#   def tickSize(self, tickerId: int, field: int, size: int):
#     super().tickSize(tickerId, field, size)
#     # print(f"GOT SIZE: tickerId: {tickerId}, field: {field}, size: {size}")

#   def historicalData(self,  req_id: int, bar: BarData):
#     super().historicalData(req_id, bar)
#     historicalDataRequests[req_id]["bars"].append(bar)

#   def historicalDataEnd(self, req_id: int, start: str, end: str):
#     super().historicalDataEnd(req_id, start, end)
    
#     request = historicalDataRequests[req_id]
#     saveHistoricalData(request["ticker"], request["bars"])
    
    
#     del historicalDataRequests[req_id]

#   def accountSummary(self, req_id: int, account: str, tag: str, value: str, currency: str):
#     super().accountSummary(req_id, account, tag, value, currency)
    
#     if tag == "NetLiquidationByCurrency":
#       events.account_summary_received(account, float(value))

#   def openOrder(self, orderId: int, contract: Contract, order: Order, orderState):
#     super().openOrder(orderId, contract, order, orderState)

#     trade = Trade.query.filter_by(order_id=orderId).first()
#     if trade:
#       ui.info(f"Order for {trade.ticker} submitted")

#   def orderStatus(self, orderId: int, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
#     super().orderStatus(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

#     # Find our trade in the db
#     trade = Trade.query.filter_by(order_id=orderId).first()
#     if trade:
#       if status == "Filled":
#         log.debug(f"Order {orderId} has been filled")
#         trade.order_status = status
#         trade.filled = filled
#         trade.remaining = remaining

#         # Add an activity entry
#         activity = TradeActivity(
#           when=datetime.now(),
#           activity_type="buy",
#           quantity=filled
#         )

#         trade.activities.append(activity)

#         db.session.add(activity)
#         db.session.commit()

#         ui.success(f"Order filled. Bought {filled} {trade.ticker}")

#       elif status == "Inactive":
#         trade.order_status = "Inactive"
#         activity = TradeActivity(
#           when=datetime.now(),
#           activity_type=""
#         )

#   def execDetails(self, reqId, contract, execution):
#     super().execDetails(reqId, contract, execution)

#     # request = requestExecutions[reqId]
#     trade = Trade.query.filter(or_(Trade.order_id == execution.orderId, Trade.stop_order_id == execution.orderId)).first()
#     if trade:
#       log.debug(f"Order {trade.order_id} has been filled")

#       # Found our match so we can finally update our order status
#       if execution.side == "SLD":
#         trade.current_position_size -= execution.shares
#       else:
#         trade.filled += execution.shares
#         trade.remaining -= execution.shares
#         trade.current_position_size += execution.shares
      
#       if trade.remaining == 0:
#         trade.order_status = "Filled"
#         ui.success(f"Order filled. Bought {trade.filled} {trade.ticker}")

#       activity = TradeActivity(
#         when=datetime.now(),
#         activity_type="buy",
#         quantity=execution.shares
#       )

#       trade.activities.append(activity)

#     else:
#       # It wasn't a buy, so it was a trim/sell. Grab the activity from the original
#       # trade instead and we'll work from there
#       activity = TradeActivity.query.filter_by(order_id=execution.orderId).first()
#       trade = Trade.query.filter_by(id=activity.trade_id).first()

#       trade.current_position_size -= execution.shares


#     db.session.add(activity)
#     db.session.commit()

#   def error(self, reqId, errorCode, errorString):
#     super().error(reqId, errorCode, errorString)
#     ui.error(errorString)



ib = IBApi()

def ib_loop(app, api):
  with app.app_context():
    api.run()


# def start_listening(app):
#   """ The main entry point to the background thread which is responsible
#   for sending and receiving messages to and from TWS
#   """
#   connected = False

#   with app.app_context():
#     log.debug("Started IB background thread")

#     while not connected:
#       if (is_configured()):
#         # App is configured, lets get connecting!
#         log.debug("App configured. Connecting to TWS")
#         host = configuration_for("tws_host").value
#         port = configuration_for("tws_port").value

#         ib.connect(host, int(port), 1)

#         api_thread = Thread(target=ib_loop, daemon=True, args=[app, ib])
#         api_thread.start()
        
#         ib.reqIds(-1)

#         while not isinstance(ib.req_id, int):
#           log.debug("Waiting for connection")
#           sleep(1)

#         connected = True
#       else:
#         # Not configured. We'll wait a bit then try again
#         log.debug("App not configured. Will retry in 5 seconds")
#         sleep(5)

#     # Now we're connected, we wait for message from the client
#     log.info("TWS connected. Awaiting messages...")

#     run_loop()

def run_loop():
  # load_account_data()
  watch_existing_tickers()

  while True:
    try:
      # message = inbound_queue.get(block=True)
      # log.debug(f'Received message: {message.message_type}')

      # if message.message_type == "WATCH":
      #   watch(message)

      # elif message.message_type == "UNWATCH":
      #   unwatch(message)

      # elif message.message_type == "BUY":
      #   buy(message)

      # elif message.message_type == "TRIM":
      #   trim(message)

    except:
      print("Error in background thread")
      log.error("An unexpected error occurred in the background thread")
      traceback.print_exc()

# def buy(message):
#   """
#   Place a buy order for the specified ticker
#   """
#   log.debug(f"Buying {message.ticker}")

#   # Our risk variables as configured by the user
#   max_risk_percent = float(configuration_for("max_risk").value) / 100.0
#   max_position_amount_percent = float(configuration_for("max_size").value) / 100.0
  
#   # Other records we'll need
#   watched_ticker = WatchedTicker.query.filter_by(ticker=message.ticker).first()
#   account = Account.query.one()

#   # Get our prices for things and account size
#   stop_loss = watched_ticker.low
#   current_price = watched_ticker.price
#   account_size = account.total_size

#   # Calculate our position size. This is determined by calculating
#   # the number of shares we can buy, before we hit or exceed our
#   # max amount we're prepared to spend based on risk
#   loss_amount = current_price - stop_loss
#   max_risk_amount = account_size * max_risk_percent
#   max_position_amount = account_size * max_position_amount_percent
#   position_size = max_risk_amount / loss_amount
  
#   # Calculate the value of this trade and make sure it doesn't exceed our
#   # max position size
#   position_amount = position_size * current_price

#   if position_amount > max_position_amount:
#     log.debug("BUY exceeds max position amount. Trimming position")
#     position_amount = max_position_amount
#     position_size = position_amount / current_price

#   # We have to round down to the nearest whole number, as the API doesn't support
#   # fractional shares :(
#   position_size = math.floor(position_size)
#   log.info(f"Buying {position_size} of {message.ticker} @ {current_price}")
  
#   order_id = ib.next_request_id()

#   contract = Contract()
#   contract.symbol = message.ticker
#   contract.secType = "STK"
#   contract.exchange = "SMART"
#   contract.currency = "USD"
  
#   # The main buy order
#   order = Order()
#   order.orderId = order_id
#   order.action = "BUY"
#   order.totalQuantity = position_size
#   order.orderType = "MKT"
#   order.transmit = False

#   # And the stop loss
#   stop_order = Order()
#   stop_order.action = "SELL"
#   stop_order.orderType = "STP"
#   stop_order.auxPrice = stop_loss
#   stop_order.totalQuantity = position_size
#   stop_order.orderId = ib.next_request_id()
#   stop_order.parentId = order_id
#   stop_order.transmit = True

#   # Almost good to go, we're going to save this record
#   # in the datbase now so we can track it later
#   trade = Trade(
#     ticker=message.ticker,
#     amount_ordered=position_size,
#     ordered_at=datetime.now(),
#     order_status="ApiPending",
#     filled=0,
#     remaining=position_size,
#     price_at_order=current_price,
#     order_type="MKT",
#     order_id=order.orderId,
#     stop_order_id=stop_order.orderId,
#     current_stop=stop_loss,
#     current_position_size=0
#   )

#   db.session.add(trade)
#   db.session.commit()


#   # And go!
#   # ib.placeOrder(order.orderId, contract, order)
#   # ib.placeOrder(stop_order.orderId, contract, stop_order)

#   # Now annoyingly, TWS might not report an order update if it fills
#   # immediately, so we need to now keep track of the order by repeatedly
#   # requesting execution details
#   # monitor_executions = Thread(target=track_order_status, daemon=True, args=[order_id])
#   # monitor_executions.start()


# def load_account_data():
#   # Fetching account details
#   log.info("Requesting account summary")
#   ib.reqAccountSummary(ib.next_request_id(), "All", "$LEDGER:USD")

# def watch_existing_tickers():
#   watches = WatchedTicker.query.all()
#   for watched_ticker in watches:
#     log.info(f"Watching {watched_ticker.ticker}")
#     msg = WatchMessage(ticker=watched_ticker.ticker)
#     watch(msg)

# def watch(message):
#   """
#   Start watching a ticker. This will request its historical data
#   and register for real-time updates
#   """
#   contract = Contract()
#   contract.symbol = message.ticker
#   contract.secType = "STK"
#   contract.exchange = "SMART"
#   contract.currency = "USD"

#   log.info(f'Requesting historic data for {message.ticker}')
#   # Get the historic data
#   req_id = ib.next_request_id()
#   ib.reqHistoricalData(req_id, contract, "", "20 D", "1 day", "TRADES", 1, 1, False, [])
#   historicalDataRequests[req_id] = {
#     "ticker": message.ticker,
#     "bars": []
#   }

#   # Get "historic" data of today, so we can get the highs/lows
#   req_id = ib.next_request_id()
#   log.info(f'Requesting data feed for {message.ticker}')
#   subscriptions[message.ticker] = req_id
#   requests[req_id] = message.ticker
#   ib.reqMktData(req_id, contract, "233", False, False, [])

# def unwatch(message):
#   """
#   Unsubscribe from real-time updates for the specified 
#   ticker
#   """
#   log.info(f"Cancelling subscription to {message.ticker} data")
#   req_id = ib.next_request_id()
#   subId = subscriptions[message.ticker]
#   if subId:
#     # ib.cancelTickByTickData(subId)
#     ib.cancelMktData(subId)
#     del subscriptions[message.ticker]
#     del requests[subId]

# def trim(message):
#   """
#   Trim down a position by a specified amount. Trimming a position consists
#   of a few steps:

#   1. Sell the desired amount
#   2. Cancel the existing stop order
#   3. Create a new stop order at break even (if this is the first trim)
#   """
#   log.info("Trimming down position")
#   order_id = message.order_id
#   trade = Trade.query.filter_by(order_id=order_id).first()
#   move_stop = True

#   # Find our trimming activities
#   activities = TradeActivity.query.filter(
#     TradeActivity.trade_id==trade.id,
#     TradeActivity.activity_type.in_(["trim_third", "trim_half"])).all()
  
#   trimmed = 0
#   trimmed += sum(Fraction(1, 3) for a in activities if a.activity_type == "trim_third")
#   trimmed += sum(Fraction(1, 2) for a in activities if a.activity_type == "trim_half")

#   # Get our amount to trim by
#   trim_amount = 0
#   activity_type = ""
#   if message.amount == "THIRD":
#     trim_amount = Fraction(1, 3)
#     activity_type = "trim_third"
#   elif message.amount == "HALF":
#     trim_amount = Fraction(1, 2)
#     activity_type = "trim_half"

#   if trimmed > 0:
#     # This will have already been moved
#     move_stop = False

#   # Make sure we CAN trim by that amount. Otherwise we might just be selling the full position
#   full_order_size = trade.amount_ordered
#   if full_order_size - (full_order_size * trim_amount) <= 0:
#     # Nope, can't do it. We'll just return an error to the ui
#     ui.error("Unable to trim position. Not enough shares remaining")
#     return

#   # New position size calculations
#   new_position_size = float(trade.current_position_size - (trade.current_position_size * trim_amount))
#   new_position_size = math.floor(new_position_size)
#   sell_amount = trade.current_position_size - new_position_size

#   print(f"SELLING {sell_amount}")
#   print(f"NEW POSITION {new_position_size}")

#   # We're good to go. Lets modify our stop loss to break even
#   contract = Contract()
#   contract.symbol = trade.ticker
#   contract.secType = "STK"
#   contract.exchange = "SMART"
#   contract.currency = "USD"

#   # Move stop
#   stop_order = Order()
#   stop_order.action = "SELL"
#   stop_order.orderType = "STP"
#   stop_order.auxPrice = trade.price_at_order
#   stop_order.totalQuantity = new_position_size
#   stop_order.orderId = trade.stop_order_id
#   stop_order.parentId = trade.order_id
#   stop_order.transmit = True

#   # Should update the stop order
#   ib.placeOrder(trade.stop_order_id, contract, stop_order)

#   # Now sell shit
#   sell_order = Order()
#   sell_order.action = "SELL"
#   sell_order.orderType = "MKT"
#   sell_order.orderId = ib.next_request_id()
#   sell_order.totalQuantity = sell_amount
#   sell_order.transmit = True

#   # Log the activity and we're done
#   activity = TradeActivity(
#     when=datetime.now(),
#     activity_type=activity_type,
#     quantity=sell_amount,
#     order_id=sell_order.orderId,
#     trade_id=trade.id
#   )

#   db.session.add(activity)
#   db.session.commit()

#   ib.placeOrder(sell_order.orderId, contract, sell_order)

#   ui.success(f"Trimmed {trade.ticker} by {sell_amount}")
    

def track_order_status(order_id):
  print("COMMENTED OUT FOR NOW")
  # trade = Trade.query.filter_by(order_id=orderId).first()
  # while trade.order_status not in ["ApiCancelled", "Cancelled", "Filled", "Inactive"]:
  #   # The order is still waiting. Lets get details and then wait before trying again
  #   filter = ExecutionFilter()
  #   filter.symbol = trade.ticker
  #   filter.secType = "STK"
  #   filter.exchange = "SMART"

  #   request_id = ib.next_request_id()
  #   executionsRequests[request_id] = { "trade_id": trade.id, "filter": filter }
  #   ib.requestExecutions(request_id, filter)

  #   sleep(5)
  #   trade = Trade.query.filter_by(order_id=orderId).first()