from server.models import WatchedTicker, Trade

class ProviderInterface:
  """
  Provides an informal interface that is required to implement a new
  provider within KTrade. A provider is used to interface with an external
  broker/exchange, such as TWS
  """

  def connect(self, app):
    pass

  def is_connected(self):
    pass

  def load_account_data(self):
    pass

  def request_realtime_feed(self, watched_ticker: WatchedTicker):
    pass

  def stop_realtime_feed(self, watched_ticker: WatchedTicker):
    pass

  def update_prices(self, watched_ticker: WatchedTicker):
    pass


  # Main trade actions
  def buy(self, trade: Trade, position_size: float, stop_loss: float):
    pass

  def trim(self, trade: Trade, trim_size: float, stop_position: float, stop_size: float):
    pass

  def close_position(self, trade: Trade):
    pass
