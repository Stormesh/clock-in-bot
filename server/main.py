# Quart
from modules.api import app

# Data
from modules.data.common import (
    set_server,
    get_channel,
    set_channel,
    get_channels_from_server,
    remove_channel,
)

from modules.data.models import Role

# Config
import modules.config as config

# Bot Properties
from modules.discord.clock import ClockInView
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
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = os.getenv("FLASK_PORT", 7546)


async def clock(channel: discord.TextChannel, interaction: discord.Interaction):
    embed = discord.Embed(
        title="Clock In/Out",
        description="Select an option below to clock in/out.",
        color=discord.Color.blurple(),
    )
    view = ClockInView()
    message = await channel.send(embed=embed, view=view)

    if not interaction.guild:
        return
    clock_channel = get_channel(channel.id)
    if clock_channel and clock_channel.message_id:
        old_message = await channel.fetch_message(int(clock_channel.message_id))
        if old_message:
            await old_message.delete()
    set_channel(channel.id, interaction.guild.id, message_id=message.id)


@bot.event
async def on_ready():
    try:
        print(f"Logged in as {bot.user}")

        for guild in bot.guilds:
            channels = get_channels_from_server(guild.id)
            if channels:
                for channel in channels:
                    message_id = channel.message_id
                    if message_id:
                        clock_channel = bot.get_channel(channel.id)
                        if isinstance(clock_channel, discord.TextChannel):
                            old_message = await clock_channel.fetch_message(
                                int(message_id)
                            )
                            if old_message:
                                await old_message.edit(view=ClockInView())
            else:
                set_server(guild.id, guild.name)

        try:
            synced_commands = await bot.tree.sync()
            print(f"Synced {len(synced_commands)} commands.")
        except Exception as e:
            print(f"Error syncing commands: {e}")
    except Exception as e:
        print(f"Error logging in: {e}")


async def is_verified(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message(config.no_guild_message, ephemeral=True)
        return False

    if (
        isinstance(interaction.user, discord.Member)
        and not interaction.user.guild_permissions.manage_channels
    ):
        await interaction.response.send_message(
            config.no_permission_setup_message, ephemeral=True
        )
        return False

    return True

@bot.tree.command(name="setup", description="Sets up the clock app")
async def setup(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    name: str,
    role: discord.Role,
    logs: discord.TextChannel,
    sheet_url: str,
    clock_role: Optional[discord.Role] = None,
    break_role: Optional[discord.Role] = None,
    meeting_role: Optional[discord.Role] = None,
    part_role: Optional[discord.Role] = None,
):

    if not await is_verified(interaction) or not interaction.guild:
        return

    roles_list = [Role(id=role.id, type="full")]

    if clock_role:
        roles_list.append(Role(id=clock_role.id, type="clock"))

    if break_role:
        roles_list.append(Role(id=break_role.id, type="break"))

    if meeting_role:
        roles_list.append(Role(id=meeting_role.id, type="meeting"))

    if part_role:
        roles_list.append(Role(id=part_role.id, type="part"))

    set_channel(
        channel.id,
        interaction.guild.id,
        name=name,
        sheet_url=sheet_url,
        log_id=logs.id,
        roles=roles_list,
    )

    await interaction.response.send_message(
        f"Clock app set up in {channel.mention}\nLogs channel set up in {logs.mention}\nUsers who can access the app need to have the {role.mention} role.",
        ephemeral=True,
    )
    await clock(channel, interaction)


@bot.tree.command(name="remove", description="Removes the clock app from the channel")
async def remove(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
):
    if not await is_verified(interaction):
        return

    _channel = get_channel(channel.id)
    if not _channel or not _channel.message_id:
        await interaction.response.send_message(
            "Cannot find the message for the clock app in this channel. Please make sure you have the right channel",
            ephemeral=True,
        )
        return

    message = await channel.fetch_message(int(_channel.message_id))
    if not message:
        await interaction.response.send_message(
            "Cannot find the message for the clock app in this channel. Please make sure you have the right channel",
            ephemeral=True,
        )
        return

    try:
        await message.delete()
    except discord.Forbidden:
        await interaction.response.send_message(
            "I don't have permission to delete the message for the clock app in this channel",
            ephemeral=True,
        )
        return

    remove_channel(channel.id)

    await interaction.response.send_message(f"Clock app removed from {channel.mention}", ephemeral=True)


async def run_quart():
    if not (FLASK_HOST and FLASK_PORT):
        print("FLASK_HOST and/or FLASK_PORT environment variables are not set.")
        return
    config_uvicorn = uvicorn.Config(
        app, host=FLASK_HOST, port=int(FLASK_PORT), log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


async def main():
    quart_task = asyncio.create_task(run_quart())
    discord_task = asyncio.create_task(bot.start(BOT_TOKEN))

    await asyncio.gather(quart_task, discord_task)


if __name__ == "__main__":
    asyncio.run(main())
