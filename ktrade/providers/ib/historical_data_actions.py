import logging
from ktrade.models import WatchedTicker
from application import db
from ktrade.calculations import calculate_adr
from ktrade.provider_actions import ticker_updated

log = logging.getLogger(__name__)

class HistoricalDataActions:
  """
  Provides actions for handling responses from the TWS
  client related to historical data
  """

  def call(self, watched_ticker: WatchedTicker, bars: list):
    """
    Given a series of bars from the IB client, updates the high/low
    values on the watched ticker. This method assumes the bars are in
    the correct order, as it will use the last bar supplied as the
    latest data.
    """
    latest_bar = bars[-1]
    high = latest_bar.high
    low = latest_bar.low

    adr = calculate_adr(bars)

    ticker_updated(watched_ticker=watched_ticker, field="high", value=high)
    ticker_updated(watched_ticker=watched_ticker, field="low", value=low)
    ticker_updated(watched_ticker=watched_ticker, field="adr", value=adr)