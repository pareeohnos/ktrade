from enum import Enum

class TradeActivityType(Enum):
  """
  A simple enum class representing the different statuses that
  we use for a trade
  """
  
  BOUGHT = "bought"
  TRIMMED = "trimmed"
  SOLD = "sold"
  COMPLETED = "completed"
  FAILED = "failed"