from application import socketio
from server.models import WatchedTicker, Trade

def ticker_price_update(watched_ticker: WatchedTicker, field: str, value: float):
  socketio.emit("tickerUpdated", { "watched_ticker_id": watched_ticker.id, "field": field, "value": value })

def trade_filled(trade: Trade, amount: int):
  socketio.emit("tradeFilled", { "trade_id": trade.id, "order_id": trade.order_id, "amount": amount })

def trade_sold(trade: Trade, amount: int):
  socketio.emit("tradeSold", { "trade_id": trade.id, "order_id": trade.order_id, "amount": amount })

def trade_status_changed(trade: Trade, status: str, description: str):
  socketio.emit("tradeStatus", { "trade_id": trade.id, "order_id": trade.order_id, "status": status, "description": description })

def info(message):
  socketio.emit("info", { "message": message })

def warn(message):
  socketio.emit("warning", { "message": message })

def error(message):
  socketio.emit("error", { "message": message })

def success(message):
  socketio.emit("success", { "message": message })