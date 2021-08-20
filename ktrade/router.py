# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory
# from flask_cors import CORS
from application import db
from settings import ROOT_PATH

from ktrade.models import Configuration, WatchedTicker
from ktrade.decorators import check_configured

CLIENT_PATH = f'{ROOT_PATH}/client/dist'

from ktrade.routes.config_routes import routes as config_routes
from ktrade.routes.trade_routes import routes as trade_routes
from ktrade.routes.base_routes import routes as base_routes

routes = [
    config_routes,
    trade_routes,
    base_routes
]

# for route in routes:
#     CORS(route, resources={r'/*': {'origins': '*'}})


# #
# # API ROUTES
# #
# # These paths are used by the UI to request the data it needs,
# # or perform actions
# #
# @ktrade_app.route('/trades', methods=['GET'])
# @check_configured
# def trades():
#     return jsonify(['test'])
