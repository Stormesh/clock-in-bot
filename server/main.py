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
from modules.dis_data import get_data, read_data, save_data, add_data
from modules.clock_funcs import clock_in, clock_out, meeting_in, break_in, view_time, check_role
import modules.config as config
import modules.clock_str as clock_str
from modules.user_data import user_data

#Discord PY
import discord
from discord.ext import commands

#Systematic imports
from dotenv import load_dotenv
import asyncio, os

#Typing
from typing import Optional, Any

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = os.getenv('FLASK_PORT', '8000')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@app.route('/api/users', methods=['GET'])
def get_user_data():
    return jsonify(user_data)

def get_user(user_id: int):
    return next((user for user in user_data if user['id'] == user_id), None)

def get_server(server_id: int | None):
    return next((server for server in get_data() if server['id'] == server_id), None)

class ClockInView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # Clock In
    @discord.ui.button(label='Clock In', style=discord.ButtonStyle.green, emoji='⏰')
    async def clock_in_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if not await check_role(interaction):
            return
        
        user = get_user(user_id)
        if user:
            if user['isClockedIn']:
                await interaction.followup.send(config.already_clocked_in_message, ephemeral=True)
                return
            elif user['clockTime'] > 1:
                await interaction.followup.send(config.cant_reset_time_message, ephemeral=True)
                return

        server = get_server(interaction.guild_id)
        if server:
            log_id = int(server['logId'])
            if interaction.guild:
                log_channel = interaction.guild.get_channel(log_id)
                if isinstance(log_channel, discord.TextChannel):
                    embed = discord.Embed(title='Clocked in', description=f'{interaction.user.mention} has clocked in.', color=discord.Color.green())
                    await log_channel.send(embed=embed)

        await interaction.followup.send(config.clock_in_message, ephemeral=True)
        if isinstance(interaction.user, discord.Member):
            if server:
                if interaction.guild:
                    clockInId = server.get('clockRoleId')
                    if clockInId:
                        clockInRole = interaction.guild.get_role(int(clockInId))
                        if clockInRole:
                            await interaction.user.add_roles(clockInRole)
        await clock_in(interaction)

    #Clock Out
    @discord.ui.button(label='Clock Out', style=discord.ButtonStyle.red, emoji='🛑')
    async def clock_out_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        global user_data

        await interaction.response.defer()
        user_id = interaction.user.id

        if await check_role(interaction):
            user = get_user(user_id)
            if not user:
                out_response = config.no_interaction_message
            else:
                if not user['isClockedIn']:
                    out_response = config.not_clocked_in_message
                else:
                    server = get_server(interaction.guild_id)
                    if server:
                        log_id = int(server['logId'])
                        if interaction.guild:
                            log_channel = interaction.guild.get_channel(log_id)
                            if isinstance(log_channel, discord.TextChannel):
                                if user and user['isClockedIn']:
                                    embed = discord.Embed(title='Clocked out', description=await clock_out(interaction), color=discord.Color.red())
                                    await log_channel.send(embed=embed)
                    out_response = await clock_out(interaction, log=True)

                    # user['isClockedIn'] = False
                    # user['onBreak'] = False
                    # user['onMeeting'] = False
                    # user['clockTime'] = 0
                    # user['meetingTime'] = 0
                    # user['breakTime'] = 0
                    try:
                        user_data.remove(user)
                    except ValueError:
                        print('User not found in user_data.')

                    if isinstance(interaction.user, discord.Member):
                        if server:
                            if interaction.guild:
                                clock_in_id = server.get('clockRoleId')
                                if clock_in_id:
                                    clock_in_role = interaction.guild.get_role(int(clock_in_id))
                                    if clock_in_role in interaction.user.roles:
                                        await interaction.user.remove_roles(clock_in_role)

                                break_id = server.get('breakRoleId')
                                if break_id:
                                    break_role = interaction.guild.get_role(int(break_id))
                                    if break_role in interaction.user.roles:
                                        await interaction.user.remove_roles(break_role)

                                meeting_id = server.get('meetingRoleId')
                                if meeting_id:
                                    meeting_role = interaction.guild.get_role(int(meeting_id))
                                    if meeting_role in interaction.user.roles:
                                        await interaction.user.remove_roles(meeting_role)
            await interaction.followup.send(out_response, ephemeral=True)

    #Clock Break
    @discord.ui.button(label='Break', style=discord.ButtonStyle.blurple, emoji='🍔')
    async def clock_break_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if await check_role(interaction):
            user = get_user(user_id)
            if not user:
                await interaction.followup.send(config.no_interaction_message, ephemeral=True)
            else:
                if not user['isClockedIn']:
                    if not user['onBreak']:
                        await interaction.followup.send(config.not_clocked_in_message, ephemeral=True)
                    else:
                        await interaction.followup.send(config.already_on_break_message, ephemeral=True)
                else:
                    await interaction.followup.send(config.on_break_message, ephemeral=True)
                    server = get_server(interaction.guild_id)
                    if server:
                        log_id = int(server['logId'])
                        if interaction.guild:
                            log_channel = interaction.guild.get_channel(log_id)
                            if isinstance(log_channel, discord.TextChannel):
                                if user and user['isClockedIn']:
                                    embed = discord.Embed(title='Break', description=f'{interaction.user.mention} has taken a break.', color=discord.Color.blurple())
                                    await log_channel.send(embed=embed)

                        if isinstance(interaction.user, discord.Member):
                            if interaction.guild:
                                clock_in_id = server.get('clockRoleId')
                                if clock_in_id:
                                    clock_in_role = interaction.guild.get_role(int(clock_in_id))
                                    if clock_in_role in interaction.user.roles:
                                        await interaction.user.remove_roles(clock_in_role)

                                break_id = server.get('breakRoleId')
                                if break_id:
                                    break_role = interaction.guild.get_role(int(break_id))
                                    if break_role:
                                        await interaction.user.add_roles(break_role)
                    if isinstance(interaction.user, discord.Member):
                        await break_in(interaction, interaction.user)

    #Clock Back
    @discord.ui.button(label='Clock Back', style=discord.ButtonStyle.grey, emoji='🔄')
    async def clock_back_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if await check_role(interaction):
            user = get_user(user_id)
            if user:
                back_response = config.already_back_message if user['isClockedIn'] else config.back_message if user['clockTime'] > 1 else config.not_clocked_in_message

                server = get_server(interaction.guild_id)
                if server:
                    log_id = int(server['logId'])
                    if interaction.guild:
                        log_channel = interaction.guild.get_channel(log_id)
                        if isinstance(log_channel, discord.TextChannel):
                            if user['clockTime'] > 1 and not user['isClockedIn']:
                                meeting_time: int = user['meetingTime']
                                meeting_hours = clock_str.get_clock_hours(meeting_time)
                                meeting_minutes = clock_str.get_clock_minutes(meeting_time)

                                break_time: int = user['breakTime']
                                break_hours = clock_str.get_clock_hours(break_time)
                                break_minutes = clock_str.get_clock_minutes(break_time)
                                desc = f'{interaction.user.mention} is now back in from a meeting of {meeting_hours}h {meeting_minutes}m.' if user['onMeeting'] else f'{interaction.user.mention} is now back in from a break of {break_hours}h {break_minutes}m.' if user['onBreak'] else f'{interaction.user.mention} is now back in.'
                                embed = discord.Embed(title='Back in', description=desc, color=discord.Color.light_gray())
                                await log_channel.send(embed=embed)

                await interaction.followup.send(back_response, ephemeral=True)
                if user['clockTime'] > 1 and not user['isClockedIn']:
                    if isinstance(interaction.user, discord.Member):
                        if server:
                            break_id = server.get('breakRoleId')
                            if break_id:
                                break_role = interaction.user.get_role(int(break_id))
                                if break_role in interaction.user.roles:
                                    await interaction.user.remove_roles(break_role)

                            meeting_id = server.get('meetingRoleId')
                            if meeting_id:
                                meeting_role = interaction.user.get_role(int(meeting_id))
                                if meeting_role in interaction.user.roles:
                                    await interaction.user.remove_roles(meeting_role)

                            clock_in_id = server.get('clockRoleId')
                            if clock_in_id:
                                if interaction.guild:
                                    clock_in_role = interaction.guild.get_role(int(clock_in_id))
                                    if clock_in_role:
                                        await interaction.user.add_roles(clock_in_role)
                    await clock_in(interaction, True)
            else:
                await interaction.followup.send(config.no_interaction_message, ephemeral=True)

    #View Time
    @discord.ui.button(label='View Your Time', style=discord.ButtonStyle.gray, emoji='🕰️')
    async def view_time_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        time_response = config.no_interaction_message

        user = get_user(user_id)
        if user:
            time_response = await view_time(interaction)

        await interaction.followup.send(time_response, ephemeral=True)

    #Meeting Start
    @discord.ui.button(label='Meeting In', style=discord.ButtonStyle.green, emoji='📅')
    async def start_meeting_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if await check_role(interaction):
            user = get_user(user_id)
            if user:
                if user['isClockedIn']:
                    embed = discord.Embed(title='In meeting', description=f'{interaction.user.mention} is in a meeting.', color=discord.Color.green())
                    if interaction.guild:
                        server = next((server for server in get_data() if server['id'] == interaction.guild.id), None)
                        if server:
                            log_id = int(server['logId'])
                            log_channel = interaction.guild.get_channel(log_id)
                            if isinstance(log_channel, discord.TextChannel):
                                await log_channel.send(embed=embed)
                            if isinstance(interaction.user, discord.Member):
                                clock_role_id = server.get('clockRoleId')
                                if clock_role_id:
                                    clock_in_role = interaction.guild.get_role(int(clock_role_id))
                                    if clock_in_role in interaction.user.roles:
                                        await interaction.user.remove_roles(clock_in_role)
                                meeting_role_id = server.get('meetingRoleId')
                                if meeting_role_id:
                                    meeting_role = interaction.guild.get_role(int(meeting_role_id))
                                    if meeting_role:
                                        await interaction.user.add_roles(meeting_role)
                            await interaction.followup.send(config.meeting_message, ephemeral=True)
                            await meeting_in(interaction)
                elif user['onMeeting']:
                    await interaction.followup.send(config.already_in_meeting_message, ephemeral=True)
                else:
                    await interaction.followup.send(config.not_clocked_in_message, ephemeral=True)
            else:
                await interaction.followup.send(config.no_interaction_message, ephemeral=True)

async def clock(channel: discord.TextChannel, interaction: discord.Interaction):
    embed = discord.Embed(title='Clock In/Out', description='Select an option below to clock in/out.', color=discord.Color.blurple())
    view = ClockInView()
    message = await channel.send(embed=embed, view=view)

    server = next((server for server in get_data() if server['id'] == channel.guild.id), None)
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
        server = next((server for server in get_data() if server['id'] == guild.id), None)

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
        server = next((server for server in get_data() if server['id'] == interaction.guild.id), None)
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

            def set_role(role_data: Any, role_key: str):
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
        sio.run(app, host=FLASK_HOST, port=FLASK_PORT) # type: ignore

async def main():
    eventlet.spawn(run_flask) # type: ignore

    if BOT_TOKEN:
        await bot.start(BOT_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
