from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

load_dotenv()
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '*')

sio: SocketIO | None = None

def init_socket(app: Flask):
    global sio
    if sio is None:
        sio = SocketIO(app, cors_allowed_origins=CORS_ALLOWED_ORIGINS)
    return sio

def get_socket():
    if sio is None:
        raise Exception('SocketIO is not initialized')
    return sio
