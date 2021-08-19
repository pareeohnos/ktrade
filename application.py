from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils.functions import database_exists
from flask_cors import CORS

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

    return app
