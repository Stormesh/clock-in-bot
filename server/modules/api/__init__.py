from quart import Quart
from quart_cors import cors  # type: ignore
from .. import socket

app = Quart(__name__)
cors(app)
sio = socket.init_socket(app)

from .routes import users_bp, servers_bp, channels_bp

app.register_blueprint(users_bp)
app.register_blueprint(servers_bp)
app.register_blueprint(channels_bp)
