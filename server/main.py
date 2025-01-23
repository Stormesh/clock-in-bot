# Eventlet is used to patch the standard library to make it non-blocking
import eventlet
eventlet.monkey_patch()

#Flask
from flask import Flask, jsonify
from flask_cors import CORS
import modules.socket as socket

app = Flask(__name__)
CORS(app)
sio = socket.init_socket(app)

# My custom modules
from modules.dis_data import read_data, save_data, add_data
import modules.config as config
from modules.general_data import user_data, get_server
from modules.discord_clock import ClockInView

#Discord PY
import discord
from discord.ext import commands

#Systematic imports
from dotenv import load_dotenv
import asyncio, os

#Typing
from typing import Optional

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = os.getenv('FLASK_PORT', 7546)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@app.route('/api/users', methods=['GET'])
def get_user_data():
    return jsonify(user_data)

async def clock(channel: discord.TextChannel, interaction: discord.Interaction):
    embed = discord.Embed(title='Clock In/Out', description='Select an option below to clock in/out.', color=discord.Color.blurple())
    view = ClockInView()
    message = await channel.send(embed=embed, view=view)

    server = get_server(channel.guild.id)
    if server:
        if interaction.guild:
            channel_id = int(server['clockId'])
            clock_channel = interaction.guild.get_channel(channel_id)
            message_id = server.get('messageId')
            if message_id:
                if isinstance(clock_channel, discord.TextChannel):
                    clock_message = await clock_channel.fetch_message(int(message_id))
                    if clock_message:
                        await clock_message.delete()
                        clock_message = message
            server['messageId'] = message.id
            await save_data('modules/data.json')

@bot.event
async def on_ready():
    global data

    await read_data('modules/data.json')

    print(f'We have logged in as {bot.user}')

    for guild in bot.guilds:
        server = get_server(guild.id)

        if server:
            if server.get('messageId'):
                clock_id = int(server['clockId'])
                clock_channel = bot.get_channel(clock_id)
                if isinstance(clock_channel, discord.TextChannel):
                    message_id = int(server['messageId'])
                    clock_message = await clock_channel.fetch_message(message_id)
                    if clock_message:
                        await clock_message.edit(view=ClockInView())
        else:
            await add_data({
                'id': guild.id
            }, 'modules/data.json')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name='setup', description='Sets up the clock app')
async def setup(interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role, logs: discord.TextChannel, sheet_url: str, clock_role: Optional[discord.Role] = None, break_role: Optional[discord.Role] = None, meeting_role: Optional[discord.Role] = None, part_role: Optional[discord.Role] = None):
    if interaction.guild:
        server = get_server(interaction.guild.id)
        if server:
            setupPermRoleId = server.get('setupPermRoleId')
            if setupPermRoleId:
                setupPermRole = interaction.guild.get_role(int(setupPermRoleId))
                if isinstance(interaction.user, discord.Member):
                    if setupPermRole not in interaction.user.roles:
                        await interaction.response.send_message(config.no_permission_setup_message, ephemeral=True)
                        return

            server['clockId'] = channel.id
            server['logId'] = logs.id
            server['roleId'] = role.id
            server['sheetUrl'] = sheet_url

            def set_role(role_data: Optional[discord.Role], role_key: str):
                if role_data:
                    server[role_key] = role_data.id
                else:
                    server.pop(role_key, None)

            set_role(clock_role, 'clockRoleId')
            set_role(break_role, 'breakRoleId')
            set_role(meeting_role, 'meetingRoleId')
            set_role(part_role, 'partRoleId')

            await save_data('modules/data.json')

    await interaction.response.send_message(f'Clock app set up in {channel.mention}\nLogs channel set up in {logs.mention}\nUsers who can access the app need to have the {role.mention} role.', ephemeral=True)
    await clock(channel, interaction)

def run_flask():
    if FLASK_HOST and FLASK_PORT:
        sio.run(app, host=FLASK_HOST, port=int(FLASK_PORT)) # type: ignore

async def main():
    eventlet.spawn(run_flask)

    if BOT_TOKEN:
        await bot.start(BOT_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
