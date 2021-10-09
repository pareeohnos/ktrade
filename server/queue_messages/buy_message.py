from server.queue_messages.queue_message import QueueMessage
from server.models import Trade, WatchedTicker

class BuyMessage(QueueMessage):
  def __init__(self, watched_ticker: WatchedTicker, trade: Trade):
    super().__init__(type='BUY')
    self.watched_ticker = watched_ticker
    self.trade = trade
