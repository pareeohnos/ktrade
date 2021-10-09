# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory, request
from application import db
from server.models import WatchedTicker, WatchedTickerSchema
from sqlalchemy.exc import IntegrityError
from server.queues import inbound_queue
from server.queue_messages.watch_message import WatchMessage, UnwatchMessage
from server.switchboard import Switchboard

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
    db.session.expunge(watch)

    inbound_queue.put(WatchMessage(watched_ticker=watch))

    schema = WatchedTickerSchema()
    return schema.dump(watch)

  except IntegrityError:
    return jsonify({
      "error": f'Already watching {ticker}'
    }), 422

@routes.route('/unwatch', methods=['POST'])
def unwatch():
  params = request.get_json()
  id = params['id']

  watched_ticker = WatchedTicker.find(db.session, id)

  if (watched_ticker is None):
    return jsonify({
      'error': 'You are not watching this ticker'
    }), 422


  inbound_queue.put(UnwatchMessage(watched_ticker=watched_ticker))
  schema = WatchedTickerSchema()
  db.session.delete(watched_ticker)
  db.session.commit()

  return schema.dump(watched_ticker)