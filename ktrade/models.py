from application import db
from marshmallow import Schema, fields

class WatchedTicker(db.Model):
  __tablename__ = "watched_tickers"
  id = db.Column(db.Integer, primary_key=True)
  ticker = db.Column(db.String, nullable=False, unique=True)

class WatchedTickerSchema(Schema):
  id = fields.Int()
  ticker = fields.Str()

class Configuration(db.Model):
  __tablename__ = "configurations"
  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String, nullable=False, unique=True)
  value = db.Column(db.String, nullable=False)
