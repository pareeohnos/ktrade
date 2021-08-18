from application import db

class WatchedTicker(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ticket = db.Column(db.String, nullable=False, unique=True)

class Configuration(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String, nullable=False, unique=True)
  value = db.Column(db.String, nullable=False)
