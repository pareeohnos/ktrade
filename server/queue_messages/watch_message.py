from server.queue_messages.queue_message import QueueMessage

class WatchMessage(QueueMessage):
  def __init__(self, watched_ticker):
    super().__init__(type='WATCH')
    self.watched_ticker = watched_ticker

class UnwatchMessage(QueueMessage):
  def __init__(self, watched_ticker):
    super().__init__(type='UNWATCH')
    self.watched_ticker = watched_ticker