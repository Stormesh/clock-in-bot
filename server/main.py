import discord, datetime, math
import asyncio, os, threading
import toml
from modules.dis_data import get_data, read_data, save_data, add_data
from modules.rest import get, post, patch
import modules.clock_str as clock_str
from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional, Any
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_data: list[dict[str, Any]] = []

config = toml.load('config.toml')

break_time_limit = (config['break']['break_time'] if config else 30) * 60 # 30 minutes
part_break_time_limit = (config['break']['part_break_time'] if config else 15) * 60 # 15 minutes

no_interaction_message = 'You have to clock in first.'

@app.route('/api/users', methods=['GET'])
def get_user_data():
    return jsonify(user_data)

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id: int):
    user = next((user for user in user_data if user['id'] == id), None)
    return jsonify(user)

async def clock_in(interaction: discord.Interaction, back: bool = False):
    user_id = interaction.user.id
    user_name = interaction.user.display_name

    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        user_data.append({
            'id': user_id,
            'name': user_name,
            'avatar': interaction.user.display_avatar.url,
            'clockTime': 0,
            'meetingTime': 0,
            'breakTime': 0,
            'isClockedIn': False,
            'onBreak': False,
            'onMeeting': False
        })
        user = next((user for user in user_data if user['id'] == user_id), None)
        print(user)

    if user:
        print(user)
        if not back:
            user['clockTime'] = 0

        if user['onBreak'] or user['onMeeting']:
            user['onBreak'] = False
            user['onMeeting'] = False

        user['isClockedIn'] = True
        socketio.emit('update', {'message': f'{user_name} has clocked in.'}) # type: ignore

        while user['isClockedIn']:
            await asyncio.sleep(1)
            if user['isClockedIn']:
                user['clockTime'] += 1
                socketio.emit('update', {'message': f'{user_name}\'s time updated.'}) # type: ignore

async def clock_out(interaction: discord.Interaction, log: bool = False):
    global data
    user_id = interaction.user.id
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return no_interaction_message

    today = datetime.date.today()
    day = today.day

    clockTime: int = user['clockTime']
    hours = clock_str.get_clock_hours(clockTime)
    minutes = clock_str.get_clock_minutes(clockTime)

    meetingTime: int = user['meetingTime']
    meetingHours = clock_str.get_clock_hours(meetingTime)
    meetingMinutes = clock_str.get_clock_minutes(meetingTime)

    breakTime: int = user['breakTime']
    breakHours = clock_str.get_clock_hours(breakTime)
    breakMinutes = clock_str.get_clock_minutes(breakTime)

    totalTime = clockTime + meetingTime
    weekTime = totalTime
    weekHours = clock_str.get_clock_hours(weekTime)
    weekTimeStr = clock_str.get_clock_time(weekTime)
    totalTimeStr = weekTimeStr

    weekDay = (day - 1) // 7
    weeks: list[str] = [f'00;00' for _ in range(4)]
    if weekDay > 3:
        weekDay = 3
    for i in range(4):
        if weekDay == i:
            weeks[i] = weekTimeStr
            break

    server = next((server for server in get_data() if server['id'] == interaction.guild_id), None)

    if log:
        if server:
            sheet_url = server.get('sheetUrl')
            if sheet_url:
                sheet_url_str = str(sheet_url)
                sheet = await get(sheet_url_str)
                sheetUser = next((user for user in sheet if user.get('Agent') == interaction.user.display_name), None)
                if not sheetUser:
                    try:
                        sheet_data = {
                            'Agent': interaction.user.display_name,
                            'Total / Missing hours': weekTimeStr,
                            'Week 1': weeks[0],
                            'Week 2': weeks[1],
                            'Week 3': weeks[2],
                            'Week 4': weeks[3],
                        }
                        response = await post(sheet_url_str, sheet_data)
                        print(response)
                        await get(sheet_url_str)
                    except Exception as e:
                        print(f'Error while posting data: {e}')
                else:
                    try:
                        existingWeeks = [sheetUser[f'Week {i + 1}'] for i in range(4)]

                        for i in range(4):
                            existingHours, existingMinutes = map(int, existingWeeks[i].split(';'))
                            newTime = (existingHours * (60 * 60)) + (existingMinutes * 60)
                            totalTime += newTime
                            totalTimeStr = clock_str.get_clock_time(totalTime)

                            weeks[i] = existingWeeks[i]
                            if weekDay == i:
                                weekTimeStr = clock_str.get_clock_time(weekTime + newTime)

                                weeks[i] = weekTimeStr

                        sheet_data = {
                            'Total / Missing hours': totalTimeStr,
                            'Week 1': weeks[0],
                            'Week 2': weeks[1],
                            'Week 3': weeks[2],
                            'Week 4': weeks[3],
                        }
                        response = await patch(f'{sheet_url}/Agent/{interaction.user.display_name}', sheet_data)
                        print(response)
                        await get(sheet_url_str)
                    except Exception as e:
                        print(f'Error while patching data: {e}')
            socketio.emit('update', {'message': f'{interaction.user.display_name} has clocked out.'}) # type: ignore
    return f'{today.strftime('%A %m/%d/%Y')} - {interaction.user.mention} worked a total of {weekHours} hours; Business time of {hours} hours and {minutes} minutes, and meeting time of {meetingHours} hours and {meetingMinutes} minutes.\n{interaction.user.mention} also took a break of {breakHours} hours and {breakMinutes} minutes.'

async def meeting_in(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_name = interaction.user.display_name
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return False

    user['isClockedIn'] = False
    user['onBreak'] = False
    user['onMeeting'] = True
    socketio.emit('update', {'message': f'{interaction.user.display_name} went on a meeting.'}) # type: ignore

    while user['onMeeting']:
        await asyncio.sleep(1)
        if user['onMeeting']:
            user['meetingTime'] += 1
            socketio.emit('update', {'message': f'{user_name}\'s time updated.'}) # type: ignore

async def break_in(_user: discord.Member, interaction: discord.Interaction):
    global break_time_limit, part_break_time_limit
    user_id = _user.id
    user_name = _user.display_name
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return False

    user['isClockedIn'] = False
    user['onMeeting'] = False
    user['onBreak'] = True
    socketio.emit('update', {'message': f'{interaction.user.display_name} went on a break.'}) # type: ignore

    break_limit = break_time_limit

    server = next((server for server in get_data() if server['id'] == interaction.guild_id), None)

    if server:
        if interaction.guild:
            part_agent_id = server.get('partRoleId')
            if part_agent_id:
                part_agent_role = interaction.guild.get_role(int(part_agent_id))
                if user:
                    if part_agent_role in _user.roles:
                        break_limit = part_break_time_limit

    break_time_warning = math.floor((break_limit // 60) - 2) * 60
    break_time_exceeded = math.floor((break_limit // 60) + 2) * 60

    async def send_dm(user: discord.Member, message: str):
        try:
            await user.send(message)
        except discord.Forbidden as e:
            print(f'Error while sending message to {user.display_name}: {e}')

    while user['onBreak']:
        await asyncio.sleep(1)
        if user['onBreak']:
            user['breakTime'] += 1
            socketio.emit('update', {'message': f'{user_name}\'s time updated.'}) # type: ignore

        if user['breakTime'] == break_time_warning:
            await send_dm(_user, f'{_user.mention}, you have 2 minutes left on your break.')
        elif user['breakTime'] == break_limit:
            await send_dm(_user, f'{_user.mention}, your break time is over.')
        elif user['breakTime'] == break_time_exceeded:
            await send_dm(_user, f'{_user.mention}, you have exceeded your break time.')

async def view_time(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return no_interaction_message

    clock: int = user['clockTime']
    hours = clock_str.get_clock_hours(clock)
    minutes = clock_str.get_clock_minutes(clock)
    seconds = clock_str.get_clock_seconds(clock)
    return f'You have worked {hours} hours, {minutes} minutes and {seconds} seconds.'


async def check_role(interaction: discord.Interaction):
    server = next((server for server in get_data() if server['id'] == interaction.guild_id))
    if server:
        agent_id = int(server['roleId'])
        if interaction.guild:
            agent_role = interaction.guild.get_role(agent_id)
            if agent_role:
                if isinstance(interaction.user, discord.Member):
                    if agent_role not in interaction.user.roles:
                        await interaction.followup.send('You don\'t have permission to clock in.', ephemeral=True)
                        return False
                else:
                    await interaction.followup.send('You don\'t have permission to clock in.', ephemeral=True)
                    return False
    return True

class ClockInView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # Clock In
    @discord.ui.button(label='Clock In', style=discord.ButtonStyle.green, emoji='⏰')
    async def clock_in_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if await check_role(interaction):
            user = next((user for user in user_data if user['id'] == user_id), None)
            if user:
                if user['isClockedIn']:
                    await interaction.followup.send('You are already clocked in.', ephemeral=True)
                    return
                elif user['clockTime'] > 1:
                    await interaction.followup.send('You can\'t reset your time once you\'re already clocked in.', ephemeral=True)
                    return

            server = next((server for server in get_data() if server['id'] == interaction.guild_id))
            if server:
                log_id = int(server['logId'])
                if interaction.guild:
                    log_channel = interaction.guild.get_channel(log_id)
                    if isinstance(log_channel, discord.TextChannel):
                        embed = discord.Embed(title='Clocked in', description=f'{interaction.user.mention} has clocked in.', color=discord.Color.green())
                        await log_channel.send(embed=embed)

            await interaction.followup.send('You began clocking in.', ephemeral=True)
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
            user = next((user for user in user_data if user['id'] == user_id), None)
            if not user:
                out_response = no_interaction_message
            else:
                if not user['isClockedIn']:
                    out_response = 'You are not clocked in.'
                else:
                    server = next((server for server in get_data() if server['id'] == interaction.guild_id))
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
            user = next((user for user in user_data if user['id'] == user_id), None)
            if not user:
                await interaction.followup.send(no_interaction_message, ephemeral=True)
            else:
                if not user['isClockedIn']:
                    if not user['onBreak']:
                        await interaction.followup.send('You are not clocked in.', ephemeral=True)
                    else:
                        await interaction.followup.send('You are already on break.', ephemeral=True)
                else:
                    await interaction.followup.send('You are now on break.', ephemeral=True)
                    server = next((server for server in get_data() if server['id'] == interaction.guild_id), None)
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
                        await break_in(interaction.user, interaction)

    #Clock Back
    @discord.ui.button(label='Clock Back', style=discord.ButtonStyle.grey, emoji='🔄')
    async def clock_back_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if await check_role(interaction):
            user = next((user for user in user_data if user['id'] == user_id), None)
            if user:
                if user['isClockedIn']:
                    back_response = 'You are already back in.'
                elif user['clockTime'] > 1:
                    back_response = 'You are now back in.'
                else:
                    back_response = 'You are not clocked in.'

                server = next((server for server in get_data() if server['id'] == interaction.guild_id), None)
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
                await interaction.followup.send(no_interaction_message, ephemeral=True)

    #View Time
    @discord.ui.button(label='View Your Time', style=discord.ButtonStyle.gray, emoji='🕰️')
    async def view_time_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        time_response = no_interaction_message

        user = next((user for user in user_data if user['id'] == user_id), None)
        if user:
            time_response = await view_time(interaction)

        await interaction.followup.send(time_response, ephemeral=True)

    #Meeting Start
    @discord.ui.button(label='Meeting In', style=discord.ButtonStyle.green, emoji='📅')
    async def start_meeting_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if await check_role(interaction):
            user = next((user for user in user_data if user['id'] == user_id), None)
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
                            await interaction.followup.send('You are now in a meeting.\nTo get out of a meeting, click on the "Clock Back" button.', ephemeral=True)
                            await meeting_in(interaction)
                elif user['onMeeting']:
                    await interaction.followup.send('You are already in a meeting.', ephemeral=True)
                else:
                    await interaction.followup.send('You are not clocked in.', ephemeral=True)
            else:
                await interaction.followup.send(no_interaction_message, ephemeral=True)

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
        print(server)

        if server:
            if server.get('sheetUrl'):
                sheet_url = server['sheetUrl']
                sheet_url_str = str(sheet_url)
                if sheet_url:
                    try:
                        sheet = await get(sheet_url_str)
                        print(sheet)
                        server['sheetData'] = sheet

                    except Exception as e:
                        print(f'Error while getting sheet data: {e}')
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
                        await interaction.response.send_message('You don\'t have permission to set up the clock app.', ephemeral=True)
                        return

            server['clockId'] = channel.id
            server['logId'] = logs.id
            server['roleId'] = role.id
            server['sheetUrl'] = sheet_url
            sheet = await get(sheet_url)
            server['sheetData'] = sheet

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
    socketio.run(app) # type: ignore

async def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    if BOT_TOKEN:
        await bot.start(BOT_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
