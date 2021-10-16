# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils.functions import database_exists
from flask_cors import CORS
from threading import Thread
from flask_socketio import SocketIO
from db_manager import init_engine, init_session_factory
from settings import SQLALCHEMY_DATABASE_URI
import os

db = SQLAlchemy(session_options={"expire_on_commit": False})
socketio = SocketIO(cors_allowed_origins="*")
migrate = Migrate()

def create_app(**config_overrides):
    """
    Creates an app instance for Flask to start running. This is invoked
    via `wsgi.py`
    """
    app = Flask(__name__)

    settings_path = os.path.dirname(os.path.abspath(__file__))
    app.config.from_pyfile(os.path.join(settings_path, 'settings.py'))
    app.config.update(config_overrides)
    CORS(app, resources={r'/*': {'origins': '*'}})

    ## Setup websockets
    import server.routes.websocket_routes
    socketio.init_app(app)

    # Init the app and the db migration lib
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # Setup our actual db that is used throughout the app
    init_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
    init_session_factory()

    # Setup our API routes
    from server.router import routes

    for route in routes:
        app.register_blueprint(route)

    return app
