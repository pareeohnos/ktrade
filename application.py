# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils.functions import database_exists
from flask_cors import CORS
from ktrade import IBApi

db = SQLAlchemy(session_options={'autocommit': True})


def ib_loop():
    ib.run()

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

    # Start the IB thread
    ib = IBApi()

    return app
