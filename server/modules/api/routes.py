from quart import jsonify, request, Blueprint
from ..api import sio
from ..data.common import user_data, get_user, get_servers, get_channels_from_server
from ..bot_init import bot
from ..discord.clock import perform_clock_out

users_bp = Blueprint("users", __name__)


@users_bp.route("/api/users", methods=["GET"])
def get_user_data():
    users = [  # type: ignore
        {
            **user,
            "id": str(user["id"]),
            "guildId": str(user["guildId"]),
            "channelId": str(user["channelId"]),
        }
        for user in user_data
    ]
    return jsonify(users)


@users_bp.route("/api/users/<int:channel_id>", methods=["GET"])
def get_users_by_channel(channel_id: int):
    users = [  # type: ignore
        {
            **user,
            "id": str(user["id"]),
            "guildId": str(user["guildId"]),
            "channelId": str(user["channelId"]),
        }
        for user in user_data
        if user["channelId"] == channel_id
    ]
    return jsonify(users)


@users_bp.route("/api/users/dm/<int:user_id>", methods=["POST", "DELETE"])
async def dm_user(user_id: str):
    data = await request.get_json()
    message = data["message"]
    user_id_int = int(user_id)
    try:
        user = bot.get_user(user_id_int)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if request.method == "POST":
            await user.send(f"You have been warned for: **{message}**")
            return jsonify({"message": "Message sent successfully"}), 200

        if request.method == "DELETE":
            current_user = get_user(user_id_int)
            if not current_user:
                return jsonify({"error": "User not found"}), 404
            await user.send(
                f"You have been removed from the clock in bot for: **{message}**"
            )
            await perform_clock_out(
                user_id_int,
                current_user["guildId"],
                current_user["channelId"],
                kick=True,
            )
            await sio.emit("update", {"message": f"{user.display_name} has been removed."})  # type: ignore
            return jsonify({"message": "User deleted successfully"}), 200
    except ValueError:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"error": "User not found"}), 404


servers_bp = Blueprint("servers", __name__)


@servers_bp.route("/api/servers/", methods=["GET"])
def get_servers_data():
    servers = get_servers()
    return jsonify(servers)


channels_bp = Blueprint("channels", __name__)


@channels_bp.route("/api/channels/<int:server_id>", methods=["GET"])
def get_channels(server_id: int):
    channels = get_channels_from_server(server_id)
    return jsonify(channels)
