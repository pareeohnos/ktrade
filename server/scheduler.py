import logging
import sched
import time
import pytz

from time import sleep
from datetime import datetime, date, time, timedelta
from threading import Thread

from db_manager import ManagedSession
from server.models import WatchedTicker

log = logging.getLogger(__name__)
scheduler = None

class Scheduler:
  """
  The scheduler is used to run jobs in the background at specific
  intervals. This will ensure things like the LOD value is reset
  when the market opens, or it is the start of a new day if the 
  app is still running
  """
  def start(self, app):
    """
    Starts the background job scheduler
    """
    log.debug("[Scheduler] Starting")

    scheduler_thread = Thread(daemon=True, target=self._start_scheduler, args=[app])
    scheduler_thread.start()

  def _start_scheduler(self, app):
    with app.app_context():
      # Immediately clear out the LOD values. When the app
      # starts up, they're re-calculated anyway so we'll
      # just clear them
      self._reset_lod_values()


      while True:

        tz = pytz.timezone('America/New_York')
        now = datetime.now().astimezone(tz)

        tomorrow_start = tz.localize(datetime(now.year, now.month, now.day, 0, 0, 0, 0) + timedelta(days=1))
        market_open = tz.localize(datetime(now.year, now.month, now.day, 9, 29, 50, 0))
        wake_up_time = None
        
        # If the market is open, we'll schedule to reset at midnight.
        # Otherwise, we'll reset when the market opens
        if market_open < now:
          # The market is already open so we're gonna wait until midnight
          # now to reset things
          log.info("[Scheduler] Market is open. Will reset at midnight")
          wake_up_time = tomorrow_start
        else:
          # The market isn't open yet, so we'll wake up when it is
          log.info("[Scheduler] Market is not open. Will reset just before it opens")
          wake_up_time = market_open

        # Time to sleep
        seconds = (wake_up_time - now).total_seconds()
        log.info(f"[Scheduler] Sleeping for {seconds} seconds")
        sleep(seconds)

        # And we're awake! Lets clear out the LOD values for all of our watched tickers
        self._reset_lod_values()

  def _reset_lod_values(self):
    log.debug("[Scheduler] Resetting LOD values")
    with ManagedSession() as session:
      watched_tickers = WatchedTicker.all(session)
      for watched_ticker in watched_tickers:
        watched_ticker.low = None
