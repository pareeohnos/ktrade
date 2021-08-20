from application import db

class WatchedTicker(db.Model):
  __tablename__ = "watched_tickers"
  id = db.Column(db.Integer, primary_key=True)
  ticket = db.Column(db.String, nullable=False, unique=True)

class Configuration(db.Model):
  __tablename__ = "configurations"
  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String, nullable=False, unique=True)
  value = db.Column(db.String, nullable=False)
