import pytz
from datetime import datetime, date, time, timedelta

tz = pytz.timezone('America/New_York')

def is_market_open():
  """
  Simple check to see if the market is currently open. This just checks
  if the time in New York is 9:30:00
  """

  return market_open_time() < now()

def seconds_since_open():
  """
  Returns the number of seconds that the market has been open
  """
  
  return (market_open_time() - now()).seconds

def market_open_time():
  """
  Returns the time that the market opens today. Note this will just
  generate the time 9:30:00 and not check if the market is actually
  open today
  """

  current_time = now()
  return tz.localize(datetime(current_time.year, current_time.month, current_time.day, 9, 30, 0, 0))

def now():
  """
  Returns the current time in the market timezone
  """

  return datetime.now().astimezone(tz)
