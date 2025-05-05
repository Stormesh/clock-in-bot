import discord
import asyncio
import datetime
from . import clock_str
from .rest import get, post, patch
from .data.common import (
    user_data,
    get_user,
    get_channel,
    get_current_time,
    get_role,
    get_roles_ids,
)
from .discord.data import send_dm, get_shift_time, remind_user_to_clock_out
from .bot_init import bot
import math
from . import config
from . import socket

sio = socket.get_socket()


async def clock_in(
    interaction: discord.Interaction, _user: discord.Member, back: bool = False
):
    user_id = _user.id
    user_name = _user.display_name

    if not (interaction.guild and interaction.channel):
        return

    user = get_user(user_id)
    if not user:
        user_data.append(
            {
                "id": user_id,
                "guildId": interaction.guild.id,
                "channelId": interaction.channel.id,
                "name": user_name,
                "avatar": interaction.user.display_avatar.url,
                "clockTime": 0,
                "meetingTime": 0,
                "breakTime": 0,
                "isClockedIn": False,
                "onBreak": False,
                "onMeeting": False,
            }
        )
        user = get_user(user_id)

    if not user:
        return

    if not back:
        user["clockTime"] = 0

    user["onBreak"] = False
    user["onMeeting"] = False
    user["isClockedIn"] = True
    await sio.emit("update", {"message": f"{user_name} has clocked in."})

    shift_time = get_shift_time(interaction, _user)
    while user and user["isClockedIn"]:
        if not user or not user["isClockedIn"]:
            print(f'{user["name"]} clock_in loop ended')
            break

        await asyncio.sleep(1)

        user["clockTime"] += 1

        if get_current_time(user_id) == shift_time:
            await remind_user_to_clock_out(_user)


async def clock_out(
    user_id: int, channel_id: int, log: bool = False, kick: bool = False
) -> str:
    user = get_user(user_id)
    if not user:
        return config.no_interaction_message

    channel = get_channel(channel_id)

    if not channel:
        return config.no_guild_message

    def get_time_components(time: int):
        return (clock_str.get_clock_hours(time), clock_str.get_clock_minutes(time))

    clock_time = user["clockTime"]
    meeting_time = user["meetingTime"]
    break_time = user["breakTime"]

    hours, minutes = get_time_components(clock_time)
    meeting_hours, meeting_minutes = get_time_components(meeting_time)
    break_hours, break_minutes = get_time_components(break_time)

    today = datetime.date.today()
    week_day = min((today.day - 1) // 7, 3)
    weeks = ["00;00"] * 4
    total_time = clock_time + meeting_time
    week_time = total_time
    week_time_str = clock_str.get_clock_time(week_time)
    total_time_str = week_time_str
    weeks[week_day] = week_time_str

    bot_user = await bot.fetch_user(user_id)
    if not bot_user:
        return config.no_interaction_message

    clock_out_data_message = config.clock_out_data_message.format(
        date=today.strftime("%A %m/%d/%Y"),
        user_name=bot_user.mention,
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
        break_minutes_s=clock_str.make_plural(break_minutes),
    ).replace("\\n", "\n")

    if log:
        sheet_url = channel.sheet_url
        if sheet_url:
            try:
                sheet_url_str = str(sheet_url)
                sheet_user = await get(f'{sheet_url_str}/search?Agent={user["name"]}')

                if not sheet_user:
                    sheet_data = {
                        "Agent": user["name"],
                        "Total / Missing hours": week_time_str,
                        **{f"Week {i + 1}": week_time_str for i in range(4)},
                    }
                    response = await post(sheet_url_str, sheet_data)
                    print(response)
                else:
                    sheet_user = sheet_user[0]
                    existing_weeks = [sheet_user[f"Week {i + 1}"] for i in range(4)]

                    for i in range(4):
                        existing_hours, existing_minutes = map(
                            int, existing_weeks[i].split(";")
                        )
                        new_time = (existing_hours * (60 * 60)) + (
                            existing_minutes * 60
                        )
                        total_time += new_time
                        total_time_str = clock_str.get_clock_time(total_time)

                        weeks[i] = existing_weeks[i]
                        if week_day == i:
                            week_time_str = clock_str.get_clock_time(
                                week_time + new_time
                            )

                            weeks[i] = week_time_str

                    sheet_data = {
                        "Total / Missing hours": total_time_str,
                        **{f"Week {i + 1}": weeks[i] for i in range(4)},
                    }
                    response = await patch(
                        f'{sheet_url}/Agent/{user["name"]}', sheet_data
                    )
                    print(response)
            except Exception as e:
                print(f"Error while getting data: {e}")
        await sio.emit("update", {"message": f'{user["name"]} has clocked out.'})
    return clock_out_data_message + (
        "\n\nThis user has been removed from the clock in bot." if kick else ""
    )


async def meeting_in(interaction: discord.Interaction, _user: discord.Member):
    user_id = _user.id
    user = get_user(user_id)
    if not user:
        return False

    user["isClockedIn"] = False
    user["onBreak"] = False
    user["onMeeting"] = True
    await sio.emit("update", {"message": f"{interaction.user.display_name} went to a meeting."})

    shift_time = get_shift_time(interaction, _user)
    while user and user["onMeeting"]:
        if not user or not user["onMeeting"]:
            print(f'{user["name"]} meeting_in loop ended')
            break

        await asyncio.sleep(1)

        user["meetingTime"] += 1

        if get_current_time(user_id) == shift_time:
            await remind_user_to_clock_out(_user)


async def break_in(interaction: discord.Interaction, _user: discord.Member):
    user_id = _user.id
    user = get_user(user_id)
    if not user:
        return False

    if not (
        interaction.guild
        and interaction.channel
        and isinstance(interaction.channel, discord.TextChannel)
    ):
        return False

    user["isClockedIn"] = False
    user["onMeeting"] = False
    user["onBreak"] = True
    await sio.emit("update", {"message": f"{interaction.user.display_name} went on a break."})

    break_limit = config.break_time_limit

    part_agent = get_role(interaction.channel.id, "part")
    if part_agent and part_agent.role_id:
        part_agent_role = interaction.guild.get_role(int(part_agent.role_id))
        if user:
            if part_agent_role in _user.roles:
                break_limit = config.part_break_time_limit

    break_time_warning = math.floor((break_limit // 60) - config.break_warning_offset) * 60
    break_time_exceeded = math.floor((break_limit // 60) + config.break_exceeded_offset) * 60

    break_messages = {
        break_time_warning: "You have 2 minutes left on your break.",
        break_limit: "Your break time is over.",
        break_time_exceeded: "You have exceeded your break time.",
    }

    while user and user["onBreak"]:
        await asyncio.sleep(1)
        if not user or not user["onBreak"]:
            print(f'{user["name"]} break_in loop ended')
            break

        user["breakTime"] += 1

        message = break_messages.get(user["breakTime"])
        if message:
            await send_dm(_user, message)


def view_time(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = get_user(user_id)
    if not user:
        return config.no_interaction_message

    clock: int = user["clockTime"]
    meeting: int = user["meetingTime"]
    break_time: int = user["breakTime"]
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
        break_seconds_s=clock_str.make_plural(break_seconds),
    ).replace("\\n", "\n")

    return view_time_message


async def check_role(interaction: discord.Interaction):
    if not interaction.guild or not interaction.channel or not isinstance(
        interaction.channel, discord.TextChannel
    ):
        await interaction.followup.send(config.no_guild_message, ephemeral=True)
        return False

    roles = get_roles_ids(interaction.channel.id)
    if not roles or not roles.full_id:
        await interaction.followup.send(
            config.no_permission_clock_message, ephemeral=True
        )
        return False

    agent_role = interaction.guild.get_role(roles.full_id)
    if not agent_role:
        await interaction.followup.send(
            config.no_permission_clock_message, ephemeral=True
        )
        return False

    part_role = None
    if roles.part_id:
        part_role = interaction.guild.get_role(roles.part_id)

    if not isinstance(interaction.user, discord.Member):
        await interaction.followup.send(
            config.no_permission_clock_message, ephemeral=True
        )
        return False

    if not (agent_role in interaction.user.roles or part_role in interaction.user.roles):
        await interaction.followup.send(
            config.no_permission_clock_message, ephemeral=True
        )
        return False

    return True
