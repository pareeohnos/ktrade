# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory, request
from server.enums.trim_size import TrimSize
from server.decorators import check_configured
from server.models import Trade, TradeSchema, WatchedTicker
from server.queue_messages.buy_message import BuyMessage
from server.queue_messages.trim_message import TrimMessage
from server.queue_messages.sell_message import SellMessage
from server.queues import inbound_queue
from datetime import datetime
from server.enums.trade_status import TradeStatus
from db_manager import ManagedSession

routes = Blueprint('trade_routes', __name__)

@routes.route('/trades', methods=['POST'])
@check_configured
def create():
  params = request.get_json()
  id = params['watched_ticker_id']

  with ManagedSession() as session:
    watched_ticker = WatchedTicker.find(session, id)
    trade = Trade(
      ticker=watched_ticker.ticker,
      filled=0,
      price_at_order=watched_ticker.price,
      ordered_at=datetime.now(),
      order_status=TradeStatus.PENDING.value,
      order_type="MKT",
      current_position_size=0)

    session.add(trade)
  
  inbound_queue.put(BuyMessage(watched_ticker=watched_ticker, trade=trade))

  return jsonify("OK")

# Buy a ticker
@routes.route('/trades', methods=['GET'])
@check_configured
def initial_setup():
  trades = Trade.query.all()
  schema = TradeSchema()

  return jsonify(schema.dump(trades, many=True))

@routes.route('/trim', methods=['POST'])
@check_configured
def trim():
  """
  Trims down a position by a specified amount
  """

  params = request.get_json()
  trade_id = params['trade']
  amount = params['amount'].upper()

  if amount not in ["THIRD", "HALF"]:
    return jsonify({ "error": "Invalid option. You can trim by a THIRD or HALF" }), 422

  with ManagedSession() as session:
    trade = Trade.find(session, trade_id)

    if not trade.can_be_trimmed():
      return jsonify({ "error": "Cannot trim an order that has not been filled" }), 422

    inbound_queue.put(TrimMessage(trade=trade, amount=TrimSize[amount]))
    schema = TradeSchema()

    return jsonify(schema.dump(trade))

@routes.route('/trades/<trade_id>', methods=['DELETE'])
@check_configured
def destroy(trade_id=None):
  """
  Removes a trade from the database. This will not make any attempt
  to close positions, or move stop losses etc. It will just delete
  it
  """

  with ManagedSession() as session:
    # Delete everything
    session.query(Trade).filter_by(id=trade_id).delete()
    return jsonify({ "success": True })

@routes.route('/trades/<trade_id>/close', methods=['POST'])
@check_configured
def close(trade_id=None):
  """
  Closes an existing position if it is open. There must be at least 1
  share left in the position, or have not been filled yet.
  """

  with ManagedSession() as session:
    trade = Trade.find(session, trade_id)

    if trade.current_position_size > 0:
      # We need to sell what we've got left
      inbound_queue.put(SellMessage(trade=trade, amount=trade.current_position_size))

    elif TradeStatus(trade.order_status) == TradeStatus.PENDING:
      # We'll just cancel the order
      inbound_queue.put(CancelOrderMessage(trade=trade))

  return jsonify({ "success": True })
