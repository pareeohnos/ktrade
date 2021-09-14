from ktrade.queue_messages.queue_message import QueueMessage

class TrimMessage(QueueMessage):
  def __init__(self, order_id, amount):
    super().__init__(type='TRIM')

    self.order_id = order_id
    self.amount = amount
