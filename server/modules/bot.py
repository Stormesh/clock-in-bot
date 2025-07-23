from .env import load_env
from .bot_init import bot
from .data.common import (
    # Servers
    set_server,
    remove_server,
    # Channels
    get_channel,
    get_channels_from_server,
    set_channel,
    remove_channel,
)
from .data.models import Role
from . import config
from .discord.clock import ClockInView
from typing import Optional
import discord

load_env()


@bot.event
async def on_guild_join(guild: discord.Guild):
    """Handle guild join event by adding/updating server in database."""
    try:
        set_server(guild.id, guild.name)
    except Exception as e:
        print(f"Error setting server {guild.id} on join: {e}")


@bot.event
async def on_guild_update(guild: discord.Guild):
    """Handle guild update event by adding/updating server in database."""
    try:
        set_server(guild.id, guild.name)
    except Exception as e:
        print(f"Error setting server {guild.id} on update: {e}")


@bot.event
async def on_guild_remove(guild: discord.Guild):
    """Handle guild leave event by removing server from database."""
    try:
        remove_server(guild.id)
    except Exception as e:
        print(f"Error removing server {guild.id} on leave: {e}")


@bot.event
async def on_ready():
    """Handle bot ready event, initialize clock messages and sync commands."""
    try:
        print(f"Logged in as {bot.user}")

        for guild in bot.guilds:
            if guild:
                channels = get_channels_from_server(guild.id)
                if channels:
                    for channel in channels:
                        if channel:
                            message_id = channel.message_id
                            if message_id:
                                clock_channel = bot.get_channel(channel.id)
                                if isinstance(clock_channel, discord.TextChannel):
                                    try:
                                        old_message = await clock_channel.fetch_message(
                                            int(message_id)
                                        )
                                        if old_message:
                                            await old_message.edit(view=ClockInView())
                                    except discord.NotFound:
                                        print(
                                            f"Could not find message {message_id} in channel {clock_channel.name}"
                                        )
                else:
                    set_server(guild.id, guild.name)

        try:
            synced_commands = await bot.tree.sync()
            print(f"Synced {len(synced_commands)} commands.")
        except discord.Forbidden:
            print(
                "Missing permissions to sync commands. Make sure the bot has the `applications.commands` privilege."
            )
        except discord.HTTPException as e:
            print(f"Error syncing commands: {e.status} {e.text}")
        except Exception as e:
            print(f"Error syncing commands: {e}")
    except Exception as e:
        print(f"Error logging in: {e}")


async def is_verified(interaction: discord.Interaction) -> bool:
    """Verify user has required permissions for bot commands."""
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
    sheet_url: Optional[str] = None,
    clock_role: Optional[discord.Role] = None,
    break_role: Optional[discord.Role] = None,
    meeting_role: Optional[discord.Role] = None,
    part_role: Optional[discord.Role] = None,
):
    """Configure a new clock channel with specified settings."""

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

    try:
        set_channel(
            channel.id,
            interaction.guild.id,
            name=name,
            sheet_url=sheet_url,
            log_id=logs.id,
            roles=roles_list,
        )
    except Exception as e:
        print(f"Error setting channel {channel.id}: {e}")
        await interaction.response.send_message(
            "Failed to set up channel. Please try again later.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"Clock app set up in {channel.mention}\n"
        f"Logs channel set up in {logs.mention}\n"
        f"Users who can access the app need to have the {role.mention} role.",
        ephemeral=True,
    )
    await clock(channel, interaction)


async def clock(channel: discord.TextChannel, interaction: discord.Interaction):
    """Send clock in/out message to specified channel."""
    try:
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
    except discord.Forbidden:
        print("Missing permissions to send messages in channel")
        if interaction.response.is_done():
            await interaction.followup.send(
                "I don't have permission to send messages in this channel",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "I don't have permission to send messages in this channel",
                ephemeral=True,
            )
    except Exception as e:
        print(f"Error in clock command: {e}")
        if interaction.response.is_done():
            await interaction.followup.send(
                "An error occurred while setting up the clock message", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "An error occurred while setting up the clock message", ephemeral=True
            )


@bot.tree.command(name="remove", description="Removes the clock app from the channel")
async def remove(interaction: discord.Interaction, channel: discord.TextChannel):
    """Remove clock app from specified channel."""
    if not await is_verified(interaction):
        return

    _channel = get_channel(channel.id)
    if not _channel or not _channel.message_id:
        await interaction.response.send_message(
            "Cannot find the message for the clock app in this channel. Please make sure you have the right channel",
            ephemeral=True,
        )
        return

    try:
        message = await channel.fetch_message(int(_channel.message_id))
        await message.delete()
    except discord.Forbidden:
        await interaction.response.send_message(
            "I don't have permission to delete the message for the clock app in this channel",
            ephemeral=True,
        )
        return
    except discord.NotFound:
        print(f"Message {_channel.message_id} not found in channel {channel.id}")
        # Continue with removal even if message not found

    remove_channel(channel.id)
    await interaction.response.send_message(
        f"Clock app removed from {channel.mention}", ephemeral=True
    )
