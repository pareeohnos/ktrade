# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory, request
from application import db
from ktrade.models import WatchedTicker, WatchedTickerSchema
from sqlalchemy.exc import IntegrityError

routes = Blueprint('watch_routes', __name__)

# Buy a ticker
@routes.route('/watch', methods=['POST'])
def start_watching():
  params = request.get_json()
  ticker = params['ticker'].upper()

  try:
    watch = WatchedTicker(ticker=ticker)
    db.session.add(watch)
    db.session.flush()

    schema = WatchedTickerSchema()
    return schema.dump(watch)

  except IntegrityError:
    return jsonify({
      "error": f'Already watching {ticker}'
    }), 422
