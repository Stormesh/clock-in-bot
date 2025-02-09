import discord
import asyncio
import datetime
import modules.clock_str as clock_str
from modules.rest import get, post, patch
from modules.general_data import user_data, get_user, get_server
import math
import modules.config as config
import modules.socket as socket

sio = socket.get_socket()

async def send_dm(user: discord.Member, message: str):
    try:
        await user.send(message)
    except discord.Forbidden as e:
        print(f'Error while sending message to {user.display_name}: {e}')

async def remind_user_to_clock_out(user: discord.Member):
    await send_dm(user, config.remind_clock_out_message)

async def clock_in(interaction: discord.Interaction, _user: discord.Member, back: bool = False):
    user_id = _user.id
    user_name = _user.display_name

    user = get_user(user_id)
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
        user = get_user(user_id)

    if not user:
        return

    server = get_server(interaction.guild_id)

    if not server or not interaction.guild:
        return

    if not back:
        user['clockTime'] = 0

    if user['onBreak'] or user['onMeeting']:
        user['onBreak'] = False
        user['onMeeting'] = False

    user['isClockedIn'] = True
    await sio.emit('update', {'message': f'{user_name} has clocked in.'}) # type: ignore

    shift_time = get_shift_time(interaction, _user)
    while user['isClockedIn']:
        await asyncio.sleep(1)
        if user['isClockedIn']:
            user['clockTime'] += 1
            if user['clockTime'] == shift_time:
                await remind_user_to_clock_out(_user)

def get_shift_time(interaction: discord.Interaction, _user: discord.Member) -> int:
    server = get_server(interaction.guild_id)

    if not server or not interaction.guild:
        return 0

    shift_time: int = config.full_time_hour_limit
    part_agent_id = server.get('partRoleId')
    if part_agent_id:
        part_role = interaction.guild.get_role(int(part_agent_id))
        if part_role in _user.roles:
            shift_time = config.part_time_hour_limit
    return shift_time

async def clock_out(interaction: discord.Interaction, log: bool = False):
    user_id = interaction.user.id
    user = get_user(user_id)
    if not user:
        return config.no_interaction_message

    server = get_server(interaction.guild_id)

    if not server:
        return config.no_guild_message

    today = datetime.date.today()
    day = today.day

    clock_time: int = user['clockTime']
    hours = clock_str.get_clock_hours(clock_time)
    minutes = clock_str.get_clock_minutes(clock_time)

    meeting_time: int = user['meetingTime']
    meeting_hours = clock_str.get_clock_hours(meeting_time)
    meeting_minutes = clock_str.get_clock_minutes(meeting_time)

    break_time: int = user['breakTime']
    break_hours = clock_str.get_clock_hours(break_time)
    break_minutes = clock_str.get_clock_minutes(break_time)

    total_time = clock_time + meeting_time
    week_time = total_time
    week_time_str = clock_str.get_clock_time(week_time)
    total_time_str = week_time_str

    week_day = (day - 1) // 7
    weeks: list[str] = [f'00;00' for _ in range(4)]
    if week_day > 3:
        week_day = 3
    weeks[week_day] = week_time_str
    
    clock_out_data_message = config.clock_out_data_message.format(
        date=today.strftime('%A %m/%d/%Y'),
        user_name=interaction.user.mention, 
        hours=hours,
        hours_s=clock_str.make_plural(hours),
        minutes=minutes, 
        minutes_s=clock_str.make_plural(minutes),
        meeting_hours=meeting_hours, 
        meeting_hours_s=clock_str.make_plural(meeting_hours),
        meeting_minutes=meeting_minutes, 
        meeting_minutes_s=clock_str.make_plural(meeting_minutes),
        break_hours=break_hours, 
        break_hours_s=clock_str.make_plural(break_hours),
        break_minutes=break_minutes,
        break_minutes_s=clock_str.make_plural(break_minutes)
    ).replace('\\n', '\n')

    if log:
        sheet_url = server.get('sheetUrl')
        if sheet_url:
            sheet_url_str = str(sheet_url)
            sheet = await get(sheet_url_str)
            sheet_user = next((user for user in sheet if user.get('Agent') == interaction.user.display_name), None)
            if not sheet_user:
                try:
                    sheet_data = {
                        'Agent': interaction.user.display_name,
                        'Total / Missing hours': week_time_str,
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
                    existing_weeks = [sheet_user[f'Week {i + 1}'] for i in range(4)]

                    for i in range(4):
                        existing_hours, existing_minutes = map(int, existing_weeks[i].split(';'))
                        new_time = (existing_hours * (60 * 60)) + (existing_minutes * 60)
                        total_time += new_time
                        total_time_str = clock_str.get_clock_time(total_time)

                        weeks[i] = existing_weeks[i]
                        if week_day == i:
                            week_time_str = clock_str.get_clock_time(week_time + new_time)

                            weeks[i] = week_time_str

                    sheet_data = {
                        'Total / Missing hours': total_time_str,
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
        await sio.emit('update', {'message': f'{interaction.user.display_name} has clocked out.'}) # type: ignore
    return clock_out_data_message

async def meeting_in(interaction: discord.Interaction, _user: discord.Member):
    user_id = _user.id
    user = get_user(user_id)
    if not user:
        return False

    user['isClockedIn'] = False
    user['onBreak'] = False
    user['onMeeting'] = True
    await sio.emit('update', {'message': f'{interaction.user.display_name} went to a meeting.'}) # type: ignore

    shift_time = get_shift_time(interaction, _user)
    while user['onMeeting']:
        await asyncio.sleep(1)
        if user['onMeeting']:
            user['meetingTime'] += 1
            if user['meetingTime'] == shift_time:
                await remind_user_to_clock_out(_user)

async def break_in(interaction: discord.Interaction, _user: discord.Member):
    user_id = _user.id
    user = get_user(user_id)
    if not user:
        return False

    server = get_server(interaction.guild_id)

    if not server or not interaction.guild:
        return False
    
    user['isClockedIn'] = False
    user['onMeeting'] = False
    user['onBreak'] = True
    await sio.emit('update', {'message': f'{interaction.user.display_name} went on a break.'}) # type: ignore

    break_limit = config.break_time_limit

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

    while user['onBreak']:
        await asyncio.sleep(1)
        if user['onBreak']:
            user['breakTime'] += 1

        message = break_messages.get(user['breakTime'])
        if message:
            await send_dm(_user, message)

def view_time(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = get_user(user_id)
    if not user:
        return config.no_interaction_message

    clock: int = user['clockTime']
    meeting: int = user['meetingTime']
    break_time: int = user['breakTime']
    business_hours = clock_str.get_clock_hours(clock + meeting)
    business_minutes = clock_str.get_clock_minutes(clock + meeting)
    business_seconds = clock_str.get_clock_seconds(clock + meeting)

    break_hours = clock_str.get_clock_hours(break_time)
    break_minutes = clock_str.get_clock_minutes(break_time)
    break_seconds = clock_str.get_clock_seconds(break_time)

    view_time_message = config.view_time_message.format(
        business_hours=business_hours,
        business_hours_s=clock_str.make_plural(business_hours),
        business_minutes=business_minutes,
        business_minutes_s=clock_str.make_plural(business_minutes),
        business_seconds=business_seconds,
        business_seconds_s=clock_str.make_plural(business_seconds),
        break_hours=break_hours,
        break_hours_s=clock_str.make_plural(break_hours),
        break_minutes=break_minutes,
        break_minutes_s=clock_str.make_plural(break_minutes),
        break_seconds=break_seconds,
        break_seconds_s=clock_str.make_plural(break_seconds)
    ).replace('\\n', '\n')

    return view_time_message

async def check_role(interaction: discord.Interaction):
    server = get_server(interaction.guild_id)
    if server and interaction.guild:
        agent_id = int(server['roleId'])
        part_id = int(server['partRoleId'])
        agent_role = interaction.guild.get_role(agent_id)
        part_role = interaction.guild.get_role(part_id)
        if agent_role or part_role:
            if not isinstance(interaction.user, discord.Member):
                await interaction.followup.send(config.no_permission_clock_message, ephemeral=True)
                return False
            
            if not (agent_role in interaction.user.roles or part_role in interaction.user.roles):
                await interaction.followup.send(config.no_permission_clock_message, ephemeral=True)
                return False
    return True
