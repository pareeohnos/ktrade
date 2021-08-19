import logging
from ktrade.config import is_configured
from time import sleep

# class IBApi():

def start_listening():
  print("HELLO")
  logging.debug("Started IB background thread")
  while True:
    sleep(5)
    print("tick")
    # if (is_configured()):
    #   # App is configured, lets get connecting!
    #   logging.debug("App configured. Connecting to TWS")
    # else:
    #   # Not configured. We'll wait a bit then try again
    #   logging.debug("App not configured. Will retry in 5 seconds")
    #   sleep(5)