from enum import Enum
from fractions import Fraction

class TrimSize(Enum):
  """
  A simple enum class representing the different trim sizes
  """
  THIRD = Fraction(1, 3)
  HALF = Fraction(1, 2)