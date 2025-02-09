from quart import Quart
import socketio # type: ignore
from modules.env import load_env
import os
from typing import Optional

load_env()

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').replace(' ', '').split(',')
ADDITIONAL_ALLOWED_ORIGINS = os.getenv('ADDITIONAL_ALLOWED_ORIGINS', '').replace(' ', '').split(',')
CORS_ALLOWED_ORIGINS.extend(ADDITIONAL_ALLOWED_ORIGINS)
cors_origins = CORS_ALLOWED_ORIGINS if CORS_ALLOWED_ORIGINS != ['*'] else '*'

sio: Optional[socketio.AsyncServer] = None

def init_socket(app: Quart) -> socketio.AsyncServer:
    global sio
    if sio is None:
        sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=cors_origins)
        app.asgi_app = socketio.ASGIApp(sio, app.asgi_app)
    return sio

def get_socket() -> socketio.AsyncServer:
    if sio is None:
        raise Exception('SocketIO is not initialized')
    return sio
