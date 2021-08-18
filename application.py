from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils.functions import database_exists

db = SQLAlchemy()

def create_app(**config_overrides):
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    app.config.update(config_overrides)

    db.init_app(app)
    migrate = Migrate(app, db)

    from ktrade.routes import ktrade_app

    app.register_blueprint(ktrade_app)

    return app
