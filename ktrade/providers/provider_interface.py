from ktrade.models import WatchedTicker, Trade

class ProviderInterface:
  """
  Provides an informal interface that is required to implement a new
  provider within KTrade. A provider is used to interface with an external
  broker/exchange, such as TWS
  """

  def connect(app):
    pass

  def is_connected():
    pass

  def load_account_data():
    pass

  def request_realtime_feed(watched_ticker: WatchedTicker):
    pass

  def stop_realtime_feed(watched_ticker: WatchedTicker):
    pass


  # Main trade actions
  def buy(trade: Trade, position_size: float, stop_loss: float):
    pass

  def trim(trade: Trade, trim_size: float, stop_position: float, stop_size: float):
    pass

  def close_position(trade: Trade):
    pass
