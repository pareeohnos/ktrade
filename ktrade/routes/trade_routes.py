# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory, request
from ktrade.decorators import check_configured
from settings import ROOT_PATH
from application import db
# from ktrade.models import Configuration
from ktrade.queues import inbound_queue
from ktrade.queue_messages.buy_message import BuyMessage
# from ktrade.queue_messages import BuyMessage

routes = Blueprint('trade_routes', __name__)

# Buy a ticker
@routes.route('/buy', methods=['POST'])
def initial_setup():
  inbound_queue.put(BuyMessage(ticker="TSLA"))
  return jsonify("OK")
