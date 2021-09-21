from ktrade.queue_messages.queue_message import QueueMessage
from ktrade.enums.trim_size import TrimSize
from ktrade.models import Trade

class TrimMessage(QueueMessage):
  def __init__(self, trade: Trade, amount: TrimSize):
    super().__init__(type='TRIM')

    self.trade = trade
    self.amount = amount
