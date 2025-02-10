# Quart
from quart import Quart, jsonify, request
from quart_cors import cors # type: ignore
import modules.socket as socket

app = Quart(__name__)
cors(app)
sio = socket.init_socket(app)

# Custom modules
from modules.general_data import read_data, save_data, add_data
import modules.config as config
from modules.general_data import user_data, get_user, get_server
from modules.discord_clock import ClockInView, perform_clock_out
from modules.env import load_env
from modules.bot_init import bot

# Discord PY
import discord

# Systematic imports
import asyncio, os
import uvicorn

# Typing
from typing import Optional

load_env()
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = os.getenv('FLASK_PORT', 7546)

@app.route('/api/users', methods=['GET'])
def get_user_data():
    users = [ # type: ignore
        {**user, 'id': str(user['id']), 'guildId': str(user['guildId'])}
        for user in user_data
    ]
    return jsonify(users)

@app.route('/api/users/dm/<int:user_id>', methods=['POST', 'DELETE'])
async def dm_user(user_id: str):
    data = await request.get_json()
    message = data['message']
    user_id_int = int(user_id)
    try:
        user = bot.get_user(user_id_int)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if request.method == 'POST':
            await user.send(f'You have been warned for: **{message}**')
            return jsonify({'message': 'Message sent successfully'}), 200
        if request.method == 'DELETE':
            current_user = get_user(user_id_int)
            if not current_user:
                return jsonify({'error': 'User not found'}), 404
            await user.send(f'You have been removed from the clock in bot for: **{message}**')
            await perform_clock_out(user_id_int, current_user['guildId'], kick=True)
            await sio.emit('update', {'message': f'{user.display_name} has been removed.'}) # type: ignore
            return jsonify({'message': 'User deleted successfully'}), 200
    except ValueError:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'error': 'User not found'}), 404

async def clock(channel: discord.TextChannel, interaction: discord.Interaction):
    embed = discord.Embed(title='Clock In/Out', description='Select an option below to clock in/out.', color=discord.Color.blurple())
    view = ClockInView()
    message = await channel.send(embed=embed, view=view)

    server = get_server(channel.guild.id)
    if server and interaction.guild:
        clock_channel_id = int(server['clockId'])
        clock_channel = interaction.guild.get_channel(clock_channel_id)
        message_id = server.get('messageId')
        if message_id and isinstance(clock_channel, discord.TextChannel):
            old_message = await clock_channel.fetch_message(int(message_id))
            if old_message:
                await old_message.delete()
        server['messageId'] = message.id
        await save_data('modules/data/data.json')

@bot.event
async def on_ready():
    await read_data('modules/data/data.json')
    print(f'Logged in as {bot.user}')

    for guild in bot.guilds:
        server = get_server(guild.id)
        if server:
            message_id = server.get('messageId')
            if message_id:
                clock_channel_id = int(server['clockId'])
                clock_channel = bot.get_channel(clock_channel_id)
                if isinstance(clock_channel, discord.TextChannel):
                    old_message = await clock_channel.fetch_message(int(message_id))
                    if old_message:
                        await old_message.edit(view=ClockInView())
        else:
            await add_data({'id': guild.id}, 'modules/data.json')
    
    try:
        synced_commands = await bot.tree.sync()
        print(f'Synced {len(synced_commands)} commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name='setup', description='Sets up the clock app')
async def setup(interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role, logs: discord.TextChannel, sheet_url: str, clock_role: Optional[discord.Role] = None, break_role: Optional[discord.Role] = None, meeting_role: Optional[discord.Role] = None, part_role: Optional[discord.Role] = None):
    if not interaction.guild:
        await interaction.response.send_message(config.no_guild_message, ephemeral=True)
        return

    server = get_server(interaction.guild.id)
    if not server:
        return

    if isinstance(interaction.user, discord.Member) and not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message(config.no_permission_setup_message, ephemeral=True)
        return

    server.update({
        'clockId': channel.id,
        'logId': logs.id,
        'roleId': role.id,
        'sheetUrl': sheet_url
    })

    def set_roles(role_data: dict[Optional[discord.Role], str]):
        if not role_data:
            return
        
        for role, role_key in role_data.items():
            if role is None:
                return server.pop(role_key, None)

            server[role_key] = role.id

    set_roles({
        clock_role: 'clockRoleId',
        break_role: 'breakRoleId',
        meeting_role: 'meetingRoleId',
        part_role: 'partRoleId'
    })

    await save_data('modules/data/data.json')

    await interaction.response.send_message(f'Clock app set up in {channel.mention}\nLogs channel set up in {logs.mention}\nUsers who can access the app need to have the {role.mention} role.', ephemeral=True)
    await clock(channel, interaction)

async def run_quart():
    if FLASK_HOST and FLASK_PORT:
        config_uvicorn = uvicorn.Config(app, host=FLASK_HOST, port=int(FLASK_PORT), log_level="info")
        server = uvicorn.Server(config_uvicorn)
        await server.serve()

async def main():
    quart_task = asyncio.create_task(run_quart())
    discord_task = asyncio.create_task(bot.start(BOT_TOKEN))

    await asyncio.gather(quart_task, discord_task)

if __name__ == '__main__':
    asyncio.run(main())

