# Set the path
import os, sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import create_app, db
app = create_app()

@app.before_first_request
def initialise_db():
    logging.debug('Creating database')
    db.create_all()
