from server.queue_messages.queue_message import QueueMessage
from server.models import Trade

class CancelOrderMessage(QueueMessage):
  def __init__(self, trade: Trade):
    super().__init__(type='CANCEL')
    self.trade = trade
