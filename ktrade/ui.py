from application import socketio

def notify_ticker_update(ticker, field, value):
  socketio.emit("tickerUpdated", { "ticker": ticker, "field": field, "value": value })

def info(message):
  socketio.emit("info", { "message": message })

def warn(message):
  socketio.emit("warning", { "message": message })

def error(message):
  socketio.emit("error", { "message": message })

def success(message):
  socketio.emit("success", { "message": message })