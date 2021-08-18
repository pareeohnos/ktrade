import os

user_dir = os.path.expanduser('~')

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(user_dir, '.ktrade.db')}"
