import discord
import asyncio
import datetime
import modules.clock_str as clock_str
from modules.dis_data import get_data
from modules.rest import get, post, patch
from modules.user_data import user_data
import math
import modules.config as config
import modules.socket as socket

sio = socket.get_socket()

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

    if user:
        if not back:
            user['clockTime'] = 0

        if user['onBreak'] or user['onMeeting']:
            user['onBreak'] = False
            user['onMeeting'] = False

        user['isClockedIn'] = True
        sio.emit('update', {'message': f'{user_name} has clocked in.'}) # type: ignore

        while user['isClockedIn']:
            await asyncio.sleep(1)
            if user['isClockedIn']:
                user['clockTime'] += 1

async def clock_out(interaction: discord.Interaction, log: bool = False):
    user_id = interaction.user.id
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return config.no_interaction_message

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
            sio.emit('update', {'message': f'{interaction.user.display_name} has clocked out.'}) # type: ignore
    return f'{today.strftime('%A %m/%d/%Y')} - {interaction.user.mention} worked a total of {weekHours} hours; Business time of {hours} hours and {minutes} minutes, and meeting time of {meetingHours} hours and {meetingMinutes} minutes.\n{interaction.user.mention} also took a break of {breakHours} hours and {breakMinutes} minutes.'

async def meeting_in(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return False

    user['isClockedIn'] = False
    user['onBreak'] = False
    user['onMeeting'] = True
    sio.emit('update', {'message': f'{interaction.user.display_name} went on a meeting.'}) # type: ignore

    while user['onMeeting']:
        await asyncio.sleep(1)
        if user['onMeeting']:
            user['meetingTime'] += 1

async def break_in(interaction: discord.Interaction, _user: discord.Member):
    user_id = _user.id
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return False

    user['isClockedIn'] = False
    user['onMeeting'] = False
    user['onBreak'] = True
    sio.emit('update', {'message': f'{interaction.user.display_name} went on a break.'}) # type: ignore

    break_limit = config.break_time_limit

    server = next((server for server in get_data() if server['id'] == interaction.guild_id), None)

    if server:
        if interaction.guild:
            part_agent_id = server.get('partRoleId')
            if part_agent_id:
                part_agent_role = interaction.guild.get_role(int(part_agent_id))
                if user:
                    if part_agent_role in _user.roles:
                        break_limit = config.part_break_time_limit

    break_time_warning = math.floor((break_limit // 60) - 2) * 60
    break_time_exceeded = math.floor((break_limit // 60) + 2) * 60

    break_messages = {
        break_time_warning: 'You have 2 minutes left on your break.',
        break_limit: 'Your break time is over.',
        break_time_exceeded: 'You have exceeded your break time.'
    }

    async def send_dm(user: discord.Member, message: str):
        try:
            await user.send(message)
        except discord.Forbidden as e:
            print(f'Error while sending message to {user.display_name}: {e}')

    while user['onBreak']:
        await asyncio.sleep(1)
        if user['onBreak']:
            user['breakTime'] += 1

        message = break_messages.get(user['breakTime'])
        if message:
            await send_dm(_user, message)

async def view_time(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = next((user for user in user_data if user['id'] == user_id), None)
    if not user:
        return config.no_interaction_message

    clock: int = user['clockTime']
    hours = clock_str.get_clock_hours(clock)
    minutes = clock_str.get_clock_minutes(clock)
    seconds = clock_str.get_clock_seconds(clock)
    return f'You have worked {hours} hours, {minutes} minutes and {seconds} seconds.'


async def check_role(interaction: discord.Interaction):
    server = next((server for server in get_data() if server['id'] == interaction.guild_id))
    if server:
        agent_id = int(server['roleId'])
        part_id = int(server['partRoleId'])
        if interaction.guild:
            agent_role = interaction.guild.get_role(agent_id)
            part_role = interaction.guild.get_role(part_id)
            if agent_role or part_role:
                if isinstance(interaction.user, discord.Member):
                    if not (agent_role in interaction.user.roles or part_role in interaction.user.roles):
                        await interaction.followup.send('You don\'t have permission to clock in.', ephemeral=True)
                        return False
                else:
                    await interaction.followup.send('You don\'t have permission to clock in.', ephemeral=True)
                    return False
    return True
