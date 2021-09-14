from flask import Flask, render_template
from flask_socketio import send
from application import socketio

@socketio.on('message')
def handle_message(message):
  send(message)
