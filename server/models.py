from application import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields
from server.enums.trade_status import TradeStatus


class BaseModel(db.Model):
  __abstract__ = True

  @classmethod
  def find(cls, session, id):
    return session.query(cls).filter_by(id=id).one()

  @classmethod
  def find_by(cls, session, **kwargs):
    return session.query(cls).filter_by(**kwargs).first()

  @classmethod
  def all(cls, session):
    return session.query(cls).all()

def camelcase(s):
  parts = iter(s.split("_"))
  return next(parts) + "".join(i.title() for i in parts)

class APISchema(Schema):
  def on_bind_field(self, field_name, field_obj):
    field_obj.data_key = camelcase(field_obj.data_key or field_name)

#
# Watched tickers
#
class WatchedTicker(BaseModel):
  __tablename__ = "watched_tickers"
  id = db.Column(db.Integer, primary_key=True)
  ticker = db.Column(db.String, nullable=False, unique=True)
  high = db.Column(db.Float)
  low = db.Column(db.Float)
  price = db.Column(db.Float)
  adr = db.Column(db.Float)


class WatchedTickerSchema(APISchema):
  id = fields.Int()
  ticker = fields.Str()
  high = fields.Float()
  low = fields.Float()
  price = fields.Float()
  adr = fields.Float()

#
# Accounts
#
class Account(BaseModel):
  __tablename__ = "accounts"
  id = db.Column(db.Integer, primary_key=True)
  number = db.Column(db.String, unique=True)
  total_size = db.Column(db.Float)

class AccountSchema(APISchema):
  id = fields.Int()
  number = fields.String()
  totalSize = fields.Float()

#
# Trades
#
class Trade(BaseModel):
  __tablename__ = "trades"
  id = db.Column(db.Integer, primary_key=True)
  ticker = db.Column(db.String, nullable=False)

  # The time the order was sent to TWS, NOT the time it was actually
  # filled
  amount_ordered = db.Column(db.Float)
  ordered_at = db.Column(db.DateTime)
  order_status = db.Column(db.String, nullable=False)
  order_status_desc = db.Column(db.Text)
  
  # Tracking the number of shares still to fill.
  filled = db.Column(db.Float, nullable=False)
  remaining = db.Column(db.Float)
  
  # The price of the stock when the order was placed. NOT the
  # price it filled at, as it might fill at multiple prices
  price_at_order = db.Column(db.Float)
  order_type = db.Column(db.String)
  
  # The order ID used by the broker
  order_id = db.Column(db.Integer, unique=True, index=True)
  stop_order_id = db.Column(db.Integer, unique=True, index=True)
  
  # These will change over time as things are trimmed
  current_stop = db.Column(db.Float)
  current_position_size = db.Column(db.Float)

  activities = relationship("TradeActivity", back_populates="trade", cascade="all, delete")

  def can_be_trimmed(self):
    return TradeStatus(self.order_status) == TradeStatus.COMPLETE

class TradeSchema(APISchema):
  id = fields.Int()
  ticker = fields.String()
  ordered_at = fields.DateTime()
  order_status = fields.String()
  order_status_desc = fields.String()
  filled = fields.Float()
  remaining = fields.Float()
  price_at_order = fields.Float()
  order_type = fields.String()
  order_id = fields.Integer()
  stop_order_id = fields.Integer()
  current_stop = fields.Float()
  current_position_size = fields.Float()

class TradeActivity(BaseModel):
  """
  The trade activity model records a log of all activity that takes
  place against a single "trade". If for instance I buy 1000 shares
  of AAPL, it might not fill immediately. Or perhaps I trim my position
  by 1/3. In both of these scenarios, records will be added to the
  activities table to show what has happened.

  It will record every time part of a position is filled, or a position
  is sold etc. Anything that happens in a trade, will be logged here.
  """
  __tablename__ = "trade_activities"

  id = db.Column(db.Integer, primary_key=True)

  # When the activity was received from TWS
  when = db.Column(db.DateTime, nullable=False)

  # Any helpful information about this activity
  what = db.Column(db.Text, nullable=True)

  # What type of activity this is. This might be a fill, or a sell, or any other
  # type introduced later.
  activity_type = db.Column(db.String, nullable=False)

  # If buying/selling, this will record how many shares were bought/sold
  quantity = db.Column(db.Float)

  # If trimming/selling
  order_id = db.Column(db.Integer, nullable=True, index=True)

  trade_id = db.Column(db.Integer, ForeignKey("trades.id"), nullable=False)

  trade = relationship("Trade", back_populates="activities")


#
# Internal app configuration
#
class Configuration(BaseModel):
  __tablename__ = "configurations"
  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String, nullable=False, unique=True)
  value = db.Column(db.String, nullable=False)
