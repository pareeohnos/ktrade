from flask import Flask, jsonify, send_from_directory
from subprocess import call
# from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CLIENT_PATH = '../client/dist'
# CORS(app, resources={r'/*', {'origins': '*'}})

#
# STATIC ASSET ROUTES
#
# This is only a local-running app, so no nginx or other proxy
# to handle static assets
#
@app.route('/assets/<path:path>', methods=['GET'])
def send_asset(path):
    return send_from_directory(f'{CLIENT_PATH}/assets', path)

#
# The root path of the app. This will be the initial
# path that is loaded
#
@app.route('/', methods=['GET'])
def root():
    return send_from_directory(CLIENT_PATH, 'index.html')

#
# API ROUTES
#
# These paths are used by the UI to request the data it needs,
# or perform actions
#



#
# Catch all route. The UI is handling all routing, so if a page
# is loaded that isn't `/` the server still needs to issue the
# right HTML for the UI to take over. All other routes not already
# matched will be handled here
#
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    return send_from_directory(CLIENT_PATH, 'index.html')

if __name__ == '__main__':
    app.run()
