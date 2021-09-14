from ktrade.queue_messages.queue_message import QueueMessage

class WatchMessage(QueueMessage):
  def __init__(self, ticker):
    super().__init__(type='WATCH')
    self.ticker = ticker

class UnwatchMessage(QueueMessage):
  def __init__(self, ticker):
    super().__init__(type='UNWATCH')
    self.ticker = ticker