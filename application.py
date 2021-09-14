# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils.functions import database_exists
from flask_cors import CORS
from threading import Thread
from flask_socketio import SocketIO
import os

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()

def create_app(**config_overrides):
    """
    Creates an app instance for Flask to start running. This is invoked
    via `wsgi.py`
    """
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    app.config.update(config_overrides)
    CORS(app, resources={r'/*': {'origins': '*'}})

    ## Setup websockets
    import ktrade.routes.websocket_routes
    socketio.init_app(app)

    # Init the app and the db migration lib
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # Setup our API routes
    from ktrade.router import routes

    for route in routes:
        app.register_blueprint(route)

    return app
