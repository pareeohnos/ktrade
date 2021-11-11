import math
import logging
from functools import reduce
from server.models import WatchedTicker, Account
from server.config import configuration_for

log = logging.getLogger(__name__)

def calculate_adr(bars):
  """
  Given a series of bars from the IB client, calculates the ADR
  """
  total = reduce(
    lambda acc, bar: acc + (bar.high / bar.low),
    bars,
    0)

  return round(100 * ((total / len(bars)) - 1), 1)

def calculate_position_sizes(watched_ticker: WatchedTicker):
  """
  Calculates the correct position size for a BUY order. This takes
  into account the size of the account, and the user-defined risk
  values to determine how large an order should be
  """

  # Our risk variables as configured by the user
  max_risk_percent = float(configuration_for("max_risk").value) / 100.0
  max_position_amount_percent = float(configuration_for("max_size").value) / 100.0

  # Get our prices for things and account size
  stop_loss = watched_ticker.low
  current_price = watched_ticker.price
  total_account_size = account_size()

  # We can't open a position if it's already at the stop loss
  if current_price == stop_loss:
    return {
      "position_size": 0,
      "stop_loss": stop_loss
    }

  # Calculate our position size. This is determined by calculating
  # the number of shares we can buy, before we hit or exceed our
  # max amount we're prepared to spend based on risk
  loss_amount = current_price - stop_loss
  max_risk_amount = total_account_size * max_risk_percent
  max_position_amount = total_account_size * max_position_amount_percent
  position_size = max_risk_amount / loss_amount
  
  # Calculate the value of this trade and make sure it doesn't exceed our
  # max position size
  position_amount = position_size * current_price

  if position_amount > max_position_amount:
    log.debug("[Calculations] BUY exceeds max position amount. Trimming position")
    position_amount = max_position_amount
    position_size = position_amount / current_price

  # We have to round down to the nearest whole number, as the API doesn't support
  # fractional shares :(
  return {
    "position_size": math.floor(position_size),
    "stop_loss": stop_loss
  }

def account_size():
  """
  Determines the size of the account. If the user has configured the app
  to automatically fetch the account size then this will be stored in the
  database. Otherwise, they will have specified a value to use for this.
  """

  fetch_account_size = configuration_for("fetch_account_size").value
  fetch_account_size = int(fetch_account_size) == 1
  if fetch_account_size:
    # This will already be stored, so grap that
    account = Account.query.one()
    return account.total_size

  else:
    # Return the user-defined amount
    return float(configuration_for("account_size").value)