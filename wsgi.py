# Set the path
import os, sys
import logging
from threading import Thread
from application import create_app, db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = create_app()

if os.environ["FLASK_RUN_FROM_CLI"]:
    print("Start by flask command")
    # We're being run directly from `flask` command. Check that we're
    # running the `run` command before starting background threads.
    # We don't want to start them if we're not
    script, command, *rest = sys.argv

    if command == "run":
        # This is the `run` command so fire up the background threads
        from ktrade.ib_api import start_listening
        ib = Thread(daemon=True, target=start_listening, args=[app])
        ib.start()

@app.before_first_request
def initialise_db():
    logging.debug('Creating database')
    db.create_all()
