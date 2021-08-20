from ktrade.queue_messages.queue_message import QueueMessage

class BuyMessage(QueueMessage):
  def __init__(self, ticker):
    super().__init__(type='BUY', ticker=ticker)
