# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory, request
from ktrade.decorators import check_configured
from ktrade.models import Trade, TradeSchema
from ktrade.queue_messages.buy_message import BuyMessage
from ktrade.queue_messages.trim_message import TrimMessage
from ktrade.queues import inbound_queue

routes = Blueprint('trade_routes', __name__)

@routes.route('/trades', methods=['POST'])
@check_configured
def create():
  params = request.get_json()
  ticker = params['ticker'].upper()
  inbound_queue.put(BuyMessage(ticker=ticker))

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
  params = request.get_json()
  trade_id = params['trade']
  amount = params['amount'].upper()

  if amount not in ["THIRD", "HALF"]:
    return jsonify({ "error": "Invalid option. You can trim by a THIRD or HALF" }), 422

  trade = Trade.query.filter_by(id=trade_id).first()
  inbound_queue.put(TrimMessage(order_id=trade.order_id, amount=amount))
  schema = TradeSchema()

  return jsonify(schema.dump(trade))