import click
from flask import Blueprint
from flask_migrate import Migrate
from app import app, db

db_blueprint = Blueprint('db', __name__)

@db_blueprint.cli.command('setup')
def setup():
    """ Create the database """
    migrate = Migrate(app, db)
