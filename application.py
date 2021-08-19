# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils.functions import database_exists
from flask_cors import CORS
from threading import Thread

db = SQLAlchemy(session_options={'autocommit': True})

def create_app(**config_overrides):
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    app.config.update(config_overrides)
    CORS(app, resources={r'/*': {'origins': '*'}})

    db.init_app(app)
    migrate = Migrate(app, db)

    from ktrade.router import routes

    for route in routes:
        app.register_blueprint(route)

    from ktrade.ib_api import start_listening

    def startThread():
        ib = Thread(daemon=True, target=start_listening)
        ib.start()

    startThread()
    return app
