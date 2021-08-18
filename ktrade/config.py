import os

basedir = os.path.expanduser('~')

class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"sqlite://{os.path.join(basedir, 'ktrade.db')}"
