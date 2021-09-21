from enum import Enum

class TradeStatus(Enum):
  """
  A simple enum class representing the different statuses that
  we use for a trade
  """
  
  # We've just created the trade and are waiting for something
  # to happen
  PENDING = "pending"

  # The order has started filling, but not yet finished
  BUYING = "buying"
  
  # We are in the middle of trying to trim
  TRIMMING = "trimming"

  # We are in the middle of trying to sell
  SELLING = "selling"

  # The order has simply failed
  FAILED = "failed"

  # For whatever reason, the order has been put on some
  # kind of hold, but not necessarily cancelled/failed
  ON_HOLD = "on_hold"

  # The order has been filled, and there's nothing more to do
  COMPLETE = "complete"