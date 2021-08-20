import logging
from ktrade.config import is_configured, configuration_for
from time import sleep
from ktrade.queues import inbound_queue, outbound_queue
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from threading import Thread

class IBApi(EWrapper, EClient):
  def __init__(self):
    EClient.__init__(self, self)

def ib_loop(api):
  api.run()

def start_listening(app):
  """ The main entry point to the background thread which is responsible
  for sending and receiving messages to and from TWS
  """
  ib = IBApi()
  log = logging.getLogger(__name__)
  connected = False

  with app.app_context():
    log.debug("Started IB background thread")

    while not connected:
      # sleep(5)
      if (is_configured()):
      #   # App is configured, lets get connecting!
        log.debug("App configured. Connecting to TWS")
        host = configuration_for("tws_host").value
        port = configuration_for("tws_port").value

        ib.connect(host, int(port), 1)
        api_thread = Thread(target=ib_loop, daemon=True, args=[ib])
        api_thread.start()
        connected = True
      else:
        # Not configured. We'll wait a bit then try again
        log.debug("App not configured. Will retry in 5 seconds")
        sleep(5)

    # Now we're connected, we wait for message from the client
    log.info("TWS connected. Awaiting messages...")
    while True:
      message = inbound_queue.get(block=True)
      log.info(f'Received message: {message.message_type}')
