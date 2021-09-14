# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory, request
from application import db
from ktrade.models import WatchedTicker, WatchedTickerSchema
from sqlalchemy.exc import IntegrityError
from ktrade.queues import inbound_queue
from ktrade.queue_messages.watch_message import WatchMessage, UnwatchMessage

routes = Blueprint('watch_routes', __name__)

@routes.route('/watches', methods=['GET'])
def watches():
  watches = WatchedTicker.query.all()
  schema = WatchedTickerSchema()

  return jsonify(schema.dump(watches, many=True))

# Buy a ticker
@routes.route('/watch', methods=['POST'])
def start_watching():
  params = request.get_json()
  ticker = params['ticker'].upper()

  try:
    watch = WatchedTicker(ticker=ticker, price=0, high=0, low=0)
    db.session.add(watch)
    db.session.commit()
    db.session.flush()

    inbound_queue.put(WatchMessage(ticker=ticker))

    schema = WatchedTickerSchema()
    return schema.dump(watch)

  except IntegrityError:
    return jsonify({
      "error": f'Already watching {ticker}'
    }), 422

@routes.route('/unwatch', methods=['POST'])
def unwatch():
  params = request.get_json()
  ticker = params['ticker'].upper()

  watched_ticker = WatchedTicker.query.filter_by(ticker=ticker).first()

  if (watched_ticker is None):
    return jsonify({
      'error': f'You are not watching {ticker}'
    }), 422


  inbound_queue.put(UnwatchMessage(ticker=ticker))
  schema = WatchedTickerSchema()
  db.session.delete(watched_ticker)
  db.session.commit()

  return schema.dump(watched_ticker)