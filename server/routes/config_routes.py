# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, send_from_directory, request
from server.decorators import check_configured
from settings import ROOT_PATH
from application import db
from server.models import Configuration

CLIENT_PATH = f'{ROOT_PATH}/client/dist'

routes = Blueprint('config_routes', __name__)

# Run the initial setup wizard
@routes.route('/initial_setup', methods=['GET'])
def initial_setup():
    return send_from_directory(CLIENT_PATH, 'index.html')

# Submission of the configuration
@routes.route('/configure', methods=['POST'])
def configure():
  params = request.get_json()

  max_risk = params['maxRisk']
  max_size = params['maxSize']
  tws_host = params['twsHost']
  tws_port = params['twsPort']
  fetch_account_size = params['fetchAccountSize']
  account_size = params['accountSize']

  # Save the config
  Configuration.query.delete()
  objects = [
    Configuration(key="max_risk", value=max_risk),
    Configuration(key="max_size", value=max_size),
    Configuration(key="tws_host", value=tws_host),
    Configuration(key="tws_port", value=tws_port),
    Configuration(key="fetch_account_size", value=fetch_account_size),
    Configuration(key="account_size", value=account_size),
  ]

  db.session.bulk_save_objects(objects)
  db.session.commit()

  return jsonify({ 'saved': True })
