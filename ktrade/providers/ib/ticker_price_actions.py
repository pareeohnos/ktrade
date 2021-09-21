import logging
from ktrade.models import WatchedTicker
from ibapi.wrapper import TickTypeEnum
from ktrade.provider_actions import ticker_updated

log = logging.getLogger(__name__)

def ticker_price_update(watched_ticker: WatchedTicker, field: int, price: float):
  """
  Decides what to do with the price sent by TWS. This will updated
  the watched ticker record according to what field has been changed
  """

  if field == TickTypeEnum.LAST or field == TickTypeEnum.CLOSE:
    price_updated(watched_ticker, price)
  
  # elif field == TickTypeEnum.HIGH:
  #   high_updated(watched_ticker, price)

  # elif field == TickTypeEnum.LOW:
  #   low_updated(watched_ticker, price)

def price_updated(watched_ticker: WatchedTicker, price: float):
  """
  Updates the `low` price for the ticker. This will update
  the record in the database, and send the new value to 
  the UI as well
  """

  ticker_updated(watched_ticker, "price", price)
  
  # Update the low price if we've dropped below it
  if price < watched_ticker.low:
    ticker_updated(watched_ticker, "low", price)

  # Update the high price if we've gone above it
  if price > watched_ticker.high:
    ticker_updated(watched_ticker, "high", price)

def high_updated(watched_ticker: WatchedTicker, price: float):
  """
  Updates the `high` price for the ticker. This will update
  the record in the database, and send the new value to 
  the UI as well
  """

  ticker_updated(watched_ticker, "high", price)

def low_updated(watched_ticker: WatchedTicker, price: float):
  """
  Updates the `low` price for the ticker. This will update
  the record in the database, and send the new value to 
  the UI as well
  """

  ticker_updated(watched_ticker, "low", price)