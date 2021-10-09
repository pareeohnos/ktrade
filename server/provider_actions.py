from datetime import datetime
from db_manager import ManagedSession
from server.enums.trade_status import TradeStatus
from server.enums.trade_activity_type import TradeActivityType
from server.models import Trade, TradeActivity, WatchedTicker
import server.ui as ui

def update_order_ids(trade: Trade, order_id = None, stop_order_id = None):
  """
  Updates the order id, the stop order id, or both. If neither are provided
  then nothing will be updated.
  """

  with ManagedSession() as session:
    trade = Trade.find(session, trade.id)

    if order_id is not None:
      trade.order_id = order_id

    if stop_order_id is not None:
      trade.stop_order_id = stop_order_id

def ticker_updated(watched_ticker: WatchedTicker, field: str, value: float):
  """
  Updates a field on the watched ticker record, and notifies
  the UI that something has changed
  """
  with ManagedSession() as session:
    watched_ticker = WatchedTicker.find(session, watched_ticker.id)
    setattr(watched_ticker, field, value)
    ui.ticker_price_update(watched_ticker, field, value)

def trade_failed(trade: Trade, reason: str):
  """
  Updates the trade record to mark it as failed, and sets the
  specified reason. This will also sent a notification to the
  UI to show that something has failed, and log a trade activity
  """
  with ManagedSession() as session:
    trade = Trade.find(session, trade.id)
    trade.order_status = TradeStatus.FAILED.value
    trade.order_status_desc = reason

    activity = TradeActivity(
      when=datetime.now(),
      activity_type=TradeActivityType.FAILED.value,
      what=f"Trade failed: {reason}",
      trade_id=trade.id
    )

    session.add(activity)

    # Lastly, notify the UI
    ui.error(reason)

def trade_bought(trade: Trade, quantity: int):
  """
  Updates the trade to update its count of remaining shares. If
  there are no more remaining, the trade will be marked as filled
  and completed Notifies the UI and creates a trade activity.
  """
  with ManagedSession() as session:
    trade = Trade.find(session, trade.id)
    trade.filled += quantity
    trade.remaining -= quantity
    trade.current_position_size += quantity

    buy_activity = TradeActivity(
      when=datetime.now(),
      activity_type=TradeActivityType.BOUGHT.value,
      quantity=quantity,
      trade_id=trade.id
    )

    session.add(buy_activity)

    if trade.remaining == 0:
      # That's finished it, the order is now filled
      trade.order_status = TradeStatus.COMPLETE.value
      filled_activity = TradeActivity(
        when=datetime.now(),
        activity_type=TradeActivityType.COMPLETED.value,
        quantity=trade.amount_ordered,
        trade_id=trade.id
      )
      session.add(filled_activity)

      ui.success(f"Order filled. Bought {trade.filled} {trade.ticker}")

    else:
      # Not yet completely filled
      trade.order_status = TradeStatus.BUYING.value
      ui.success(f"Bought {quantity} {trade.ticker}")

    session.add(buy_activity)

def trade_sold(trade: Trade, quantity: int):
  """
  Updates the trade to set its current position size based on the number
  of shares sold
  """
  with ManagedSession() as session:
    trade = Trade.find(session, trade.id)
    trade.current_position_size -= quantity

    sell_activity = TradeActivity(
      when=datetime.now(),
      activity_type=TradeActivityType.SOLD.value,
      quantity=quantity,
      trade_id=trade.id
    )

    session.add(sell_activity)

def trade_filled(trade: Trade):
  """
  Marks a trade as having been completely filled and records
  an activity for it
  """

  with ManagedSession() as session:
    trade = Trade.find(session, trade.id)
    trade.order_status = TradeStatus.COMPLETE.value
    trade.filled = trade.amount_ordered
    trade.remaining = 0

    filled_activity = TradeActivity(
      when=datetime.now(),
      activity_type=TradeActivityType.COMPLETED.value,
      trade_id=trade.id
    )

    session.add(filled_activity)

  ui.success(f"Order filled - {trade.filled} {trade.ticker}")

def trade_on_hold(trade: Trade):
  """
  Marks a trade as being on hold
  """

  with ManagedSession() as session:
    trade = Trade.find(session, trade.id)
    trade.order_status = TradeStatus.ON_HOLD.value

    hold_activity = TradeActivity(
      when=datetime.now(),
      activity_type=TradeActivityType.ON_HOLD.value,
      trade_id=trade.id
    )

    session.add(hold_activity)

def trade_status_changed(trade: Trade, status: TradeStatus, description: str):
  """
  Updates the status of the trade, and sets a description
  explaining why that status now applies
  """

  with ManagedSession() as session:
    trade = Trade.find(session, trade.id)
    trade.order_status = status.value
    trade.order_status_desc = description

    activity = TradeActivity(
      when=datetime.now(),
      activity_type=TradeActivityType.STATUS_UPDATED.value,
      trade_id=trade.id
    )

    session.add(activity)

