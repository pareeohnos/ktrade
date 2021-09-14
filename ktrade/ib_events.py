from application import db
from ktrade.models import WatchedTicker, Account
from ktrade.ui import notify_ticker_update

def high_updated(ticker, price):
  """
  Updates the `high` price for the ticker. This will update
  the record in the database, and send the new value to 
  the UI as well
  """
  watched_ticker = _find_watched_ticker(ticker)
  watched_ticker.high = price
  db.session.commit()

  notify_ticker_update(ticker, "high", price)

def low_updated(ticker, price):
  """
  Updates the `low` price for the ticker. This will update
  the record in the database, and send the new value to 
  the UI as well
  """
  watched_ticker = _find_watched_ticker(ticker)
  watched_ticker.low = price
  db.session.commit()

  notify_ticker_update(ticker, "low", price)

def price_updated(ticker, price):
  """
  Updates the `low` price for the ticker. This will update
  the record in the database, and send the new value to 
  the UI as well
  """
  watched_ticker = _find_watched_ticker(ticker)
  watched_ticker.price = price
  notify_ticker_update(ticker, "price", price)
  
  # Update the low price if we've dropped below it
  if watched_ticker.low > price:
    watched_ticker.low = price
    notify_ticker_update(ticker, "low", price)


  # Update the high price if we've gone above it
  if watched_ticker.high < price:
    watched_ticker.high = price
    notify_ticker_update(ticker, "high", price)


  db.session.commit()

def account_summary_received(number: str, value: float):
  """
  Updates the total value of the account. This will be used
  for calculating the correct position size
  """
  account = Account.query.filter_by(number=number).first()
  if account is None:
    account = Account(number=number)
    db.session.add(account)

  account.total_size = value
  db.session.commit()

def _find_watched_ticker(ticker):
  return WatchedTicker.query.filter_by(ticker=ticker).first()