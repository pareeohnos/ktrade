import logging
from server.models import WatchedTicker
from application import db
from server.calculations import calculate_adr
from server.provider_actions import ticker_updated

log = logging.getLogger(__name__)

class HistoricalDataActions:
  """
  Provides actions for handling responses from the TWS
  client related to historical data
  """

  def call(self, watched_ticker: WatchedTicker, bars: list, action: str):
    """
    Given a series of bars from the IB client, updates the high/low
    values on the watched ticker. This method assumes the bars are in
    the correct order, as it will use the last bar supplied as the
    latest data.
    """

    if action == "adr":
      adr = calculate_adr(bars)
      ticker_updated(watched_ticker=watched_ticker, field="adr", value=adr)

      return {
        "adr": adr
      }

    elif action == "prices":
      low = None
      high = None

      for bar in bars:
        if low == None or bar.low < low:
          low = bar.low

        if high == None or bar.high > high:
          high = bar.high

      
      ticker_updated(watched_ticker=watched_ticker, field="high", value=high)
      ticker_updated(watched_ticker=watched_ticker, field="low", value=low)

      return {
        "high": high,
        "low": low,
      }