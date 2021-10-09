from application import socketio
from server.models import WatchedTicker

def ticker_price_update(watched_ticker: WatchedTicker, field: str, value: float):
  socketio.emit("tickerUpdated", { "watched_ticker_id": watched_ticker.id, "field": field, "value": value })

def info(message):
  socketio.emit("info", { "message": message })

def warn(message):
  socketio.emit("warning", { "message": message })

def error(message):
  socketio.emit("error", { "message": message })

def success(message):
  socketio.emit("success", { "message": message })