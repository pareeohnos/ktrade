from functools import reduce
from application import db
from ktrade.models import WatchedTicker
from ktrade.ui import notify_ticker_update

def calculateAdr(bars):
  """
  Given a series of bars from the IB client, calculates the ADR
  """
  total = reduce(
    lambda acc, bar: acc + (bar.high / bar.low),
    bars,
    0)

  return 100 * ((total / len(bars)) - 1)

def saveHistoricalData(ticker: str, bars):
  """
  Given a series of bars from the IB client, updates the high/low
  values on the watched ticker. This method assumes the bars are in
  the correct order, as it will use the last bar supplied as the
  latest data.
  """
  latest_bar = bars[-1]
  high = latest_bar.high
  low = latest_bar.low

  watched_ticker = WatchedTicker.query.filter_by(ticker=ticker).first()
  adr = calculateAdr(bars)

  watched_ticker.high = high
  watched_ticker.low = low
  watched_ticker.adr = adr

  notify_ticker_update(ticker, "adr", adr)

  db.session.commit()