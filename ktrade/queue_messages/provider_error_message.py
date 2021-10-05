from ktrade.queue_messages.queue_message import QueueMessage

class ProviderErrorMessage(QueueMessage):
  def __init__(self, exception: Exception):
    super().__init__(type='PROVIDER_ERROR')
    self.exception = exception
