# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory
from server.decorators import check_configured
from settings import ROOT_PATH

CLIENT_PATH = f'{ROOT_PATH}/client/dist'

routes = Blueprint('base_routes', __name__)
#
# STATIC ASSET ROUTES
#
# This is only a local-running app, so no nginx or other proxy
# to handle static assets
#
@routes.route('/assets/<path:path>', methods=['GET'])
def send_asset(path):
    return send_from_directory(f'{CLIENT_PATH}/assets', path)

#
# The root path of the app. This will be the initial
# path that is loaded
#
@routes.route('/', methods=['GET'])
@check_configured
def root():
    return send_from_directory(CLIENT_PATH, 'index.html')

#
# Catch all route. The UI is handling all routing, so if a page
# is loaded that isn't `/` the server still needs to issue the
# right HTML for the UI to take over. All other routes not already
# matched will be handled here
#
@routes.route('/<path:path>', methods=['GET'])
@check_configured
def catch_all(path):
    return send_from_directory(CLIENT_PATH, 'index.html')
