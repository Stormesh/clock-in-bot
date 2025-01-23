from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '*').replace(' ', '').split(',')

sio: Optional[SocketIO] = None

def init_socket(app: Flask) -> SocketIO:
    global sio
    if sio is None:
        cors_origins = CORS_ALLOWED_ORIGINS if CORS_ALLOWED_ORIGINS != ['*'] else '*'
        sio = SocketIO(app, cors_allowed_origins=cors_origins)
    return sio

def get_socket() -> SocketIO:
    if sio is None:
        raise Exception('SocketIO is not initialized')
    return sio
