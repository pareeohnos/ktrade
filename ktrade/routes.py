from flask import Blueprint, jsonify, send_from_directory
from flask_cors import CORS
from application import db
from settings import ROOT_PATH

from ktrade.models import Configuration, WatchedTicker
from ktrade.decorators import check_configured

CLIENT_PATH = f'{ROOT_PATH}/client/dist'
ktrade_app = Blueprint('ktrade_app', __name__)

CORS(ktrade_app, resources={r'/*': {'origins': '*'}})

#
# STATIC ASSET ROUTES
#
# This is only a local-running app, so no nginx or other proxy
# to handle static assets
#
@ktrade_app.route('/assets/<path:path>', methods=['GET'])
def send_asset(path):
    return send_from_directory(f'{CLIENT_PATH}/assets', path)

#
# The root path of the app. This will be the initial
# path that is loaded
#
@ktrade_app.route('/', methods=['GET'])
@check_configured
def root():
    print(CLIENT_PATH)
    return send_from_directory(CLIENT_PATH, 'index.html')

#
# API ROUTES
#
# These paths are used by the UI to request the data it needs,
# or perform actions
#
@ktrade_app.route('/trades', methods=['GET'])
@check_configure
def trades():
    return jsonify(['test'])


#
# Catch all route. The UI is handling all routing, so if a page
# is loaded that isn't `/` the server still needs to issue the
# right HTML for the UI to take over. All other routes not already
# matched will be handled here
#
@ktrade_app.route('/<path:path>', methods=['GET'])
@check_configure
def catch_all(path):
    return send_from_directory(CLIENT_PATH, 'index.html')
