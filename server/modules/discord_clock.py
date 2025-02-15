import discord
import asyncio
import modules.config as config

from modules.clock_funcs import check_role, clock_in, clock_out, meeting_in, break_in, view_time
from modules.general_data import get_user, remove_user, get_server
from modules.dis_data import remove_role, add_role
from modules.bot_init import bot
from modules.log_manager import LogManager
import modules.clock_str as clock_str

async def perform_clock_out(user_id: int, guild_id: int, kick: bool = False):
    user = get_user(user_id)
    if not user or not user['clockTime'] > 1:
        return False

    guild = bot.get_guild(guild_id)
    if not guild:
        return False

    member = guild.get_member(user_id)
    if not member:
        return False

    server = get_server(guild_id)
    if not server:
        return False


    # Send log message
    embed = discord.Embed(
        title='Clocked out',
        description=await clock_out(user_id, guild_id, kick=kick),
        color=discord.Color.red()
    )
    await LogManager.send_log_message(guild, embed)
    out_response = await clock_out(user_id, guild_id, log=True, kick=kick)

    # Update user data
    try:
        remove_user(user_id)
    except ValueError:
        pass

    # Remove roles
    clock_in_id = server.get('clockRoleId')
    break_id = server.get('breakRoleId')
    meeting_id = server.get('meetingRoleId')
    # await remove_role(member, clock_in_id)
    # await remove_role(member, break_id)
    # await remove_role(member, meeting_id)
    remove_clock = asyncio.create_task(remove_role(member, clock_in_id))
    remove_break = asyncio.create_task(remove_role(member, break_id))
    remove_meeting = asyncio.create_task(remove_role(member, meeting_id))

    await remove_clock
    await remove_break
    await remove_meeting

    return out_response

async def clock_out_discord(interaction: discord.Interaction):
        await interaction.response.defer()

        if not await check_role(interaction):
            return

        if not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return

        user_id = interaction.user.id
        guild_id = interaction.guild.id
        success = await perform_clock_out(user_id, guild_id)
        if not success:
            await interaction.followup.send(config.no_interaction_message, ephemeral=True)
            return

        await interaction.followup.send(success, ephemeral=True)

class ClockInView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # Clock In
    @discord.ui.button(label='Clock In', style=discord.ButtonStyle.green, emoji='⏰')
    async def clock_in_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()

        if not await check_role(interaction):
            return
        
        user_id = interaction.user.id
        user = get_user(user_id)
        if user:
            if user['isClockedIn']:
                await interaction.followup.send(config.already_clocked_in_message, ephemeral=True)
                return
            elif user['clockTime'] > 1:
                await interaction.followup.send(config.cant_reset_time_message, ephemeral=True)
                return

        if not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return
        
        server = get_server(interaction.guild.id)
        if not server:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return
        
        user_clock_in_message = config.user_clock_in_message.format(user_name=interaction.user.mention)
        embed = discord.Embed(title='Clocked in', description=user_clock_in_message, color=discord.Color.green())
        await LogManager.send_log_message(interaction.guild, embed)

        if not isinstance(interaction.user, discord.Member):
            return
        
        clockInId = server.get('clockRoleId')
        add_clock_role = asyncio.create_task(add_role(interaction.user, interaction.guild, clockInId))
        reply_clock = asyncio.create_task(interaction.followup.send(config.clock_in_message, ephemeral=True))
        clock_in_task = asyncio.create_task(clock_in(interaction, interaction.user))

        await add_clock_role
        await reply_clock
        await clock_in_task
        # await add_role(interaction.user, interaction.guild, clockInId)

        # await interaction.followup.send(config.clock_in_message, ephemeral=True)
        # await clock_in(interaction, interaction.user)
        

    #Clock Out
    @discord.ui.button(label='Clock Out', style=discord.ButtonStyle.red, emoji='🛑')
    async def clock_out_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await clock_out_discord(interaction)

    #Clock Break
    @discord.ui.button(label='Break', style=discord.ButtonStyle.blurple, emoji='🍔')
    async def clock_break_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()

        if not await check_role(interaction):
            return

        user_id = interaction.user.id
        user = get_user(user_id)
        if not user:
            await interaction.followup.send(config.no_interaction_message, ephemeral=True)
            return

        await interaction.followup.send((config.not_clocked_in_message if not user['onBreak'] else 
                                         config.already_on_break_message) if user['onBreak'] else 
                                         config.on_break_message, ephemeral=True)

        if not user['clockTime'] > 1 or user['onBreak']:
            return

        if not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return

        server = get_server(interaction.guild.id)
        if not server:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return
        
        user_on_break_message = config.user_on_break_message.format(user_name=interaction.user.mention)
        embed = discord.Embed(title='Break', description=user_on_break_message, color=discord.Color.blurple())
        await LogManager.send_log_message(interaction.guild, embed)

        if not isinstance(interaction.user, discord.Member):
            return
        
        clock_in_id = server.get('clockRoleId')
        meeting_id = server.get('meetingRoleId')
        break_id = server.get('breakRoleId')

        remove_clock_role = asyncio.create_task(remove_role(interaction.user, clock_in_id))
        remove_meeting_role = asyncio.create_task(remove_role(interaction.user, meeting_id))
        add_break_role = asyncio.create_task(add_role(interaction.user, interaction.guild, break_id))
        break_in_task = asyncio.create_task(break_in(interaction, interaction.user))

        await remove_clock_role
        await remove_meeting_role
        await add_break_role
        await break_in_task
        # await remove_role(interaction.user, clock_in_id)
        # await remove_role(interaction.user, meeting_id)
        # await add_role(interaction.user, interaction.guild, break_id)

        # await break_in(interaction, interaction.user)



    #Clock Back
    @discord.ui.button(label='Clock Back', style=discord.ButtonStyle.grey, emoji='🔄')
    async def clock_back_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if not await check_role(interaction):
            return

        user = get_user(user_id)
        if not user:
            await interaction.followup.send(config.no_interaction_message, ephemeral=True)
            return

        if not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return

        server = get_server(interaction.guild.id)
        if not server:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return

        back_response = (config.already_back_message if user['isClockedIn'] else 
                         config.back_message if user['clockTime'] > 1 else 
                         config.not_clocked_in_message)

        await interaction.followup.send(back_response, ephemeral=True)

        if user['clockTime'] <= 1 or user['isClockedIn']:
            return

        meeting_time: int = user['meetingTime']
        meeting_hours = clock_str.get_clock_hours(meeting_time)
        meeting_minutes = clock_str.get_clock_minutes(meeting_time)

        break_time: int = user['breakTime']
        break_hours = clock_str.get_clock_hours(break_time)
        break_minutes = clock_str.get_clock_minutes(break_time)

        back_text = {
            user['onMeeting']: config.user_meeting_back_message.format(
                user_name=interaction.user.mention,
                meeting_hours=meeting_hours,
                meeting_minutes=meeting_minutes
            ),
            user['onBreak']: config.user_break_back_message.format(
                user_name=interaction.user.mention,
                break_hours=break_hours,
                break_minutes=break_minutes
            )
        }
        desc = (back_text.get(user['onMeeting']) if user['onMeeting'] else 
                back_text.get(user['onBreak']) if user['onBreak'] else 
                config.user_back_message.format(user_name=interaction.user.mention))
        embed = discord.Embed(title='Back in', description=desc, color=discord.Color.light_gray())
        await LogManager.send_log_message(interaction.guild, embed)
        
        if not isinstance(interaction.user, discord.Member):
            return
        
        break_id = server.get('breakRoleId')
        meeting_id = server.get('meetingRoleId')
        clock_in_id = server.get('clockRoleId')

        add_clock_role = asyncio.create_task(add_role(interaction.user, interaction.guild, clock_in_id))
        remove_break_role = asyncio.create_task(remove_role(interaction.user, break_id))
        remove_meeting_role = asyncio.create_task(remove_role(interaction.user, meeting_id))
        clock_in_task = asyncio.create_task(clock_in(interaction, interaction.user, True))

        await add_clock_role
        await remove_break_role
        await remove_meeting_role
        await clock_in_task
        # await remove_role(interaction.user, break_id)
        # await remove_role(interaction.user, meeting_id)
        # await add_role(interaction.user, interaction.guild, clock_in_id)

        # await clock_in(interaction, interaction.user, True)
        

    #View Time
    @discord.ui.button(label='View Your Time', style=discord.ButtonStyle.gray, emoji='🕰️')
    async def view_time_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()

        user_id = interaction.user.id
        user = get_user(user_id)
        if not user:
            await interaction.followup.send(config.no_interaction_message, ephemeral=True)
            return

        await interaction.followup.send(view_time(interaction), ephemeral=True)

    #Meeting Start
    @discord.ui.button(label='Meeting', style=discord.ButtonStyle.green, emoji='📅')
    async def start_meeting_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()
        user_id = interaction.user.id

        if not await check_role(interaction):
            return
        
        user = get_user(user_id)
        if not user:
            await interaction.followup.send(config.no_interaction_message, ephemeral=True)
            return
        
        if user['onMeeting']:
            await interaction.followup.send(config.already_in_meeting_message, ephemeral=True)
            return

        if not user['clockTime'] > 1:
            await interaction.followup.send(config.not_clocked_in_message, ephemeral=True)
            return
        
        if not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return
        
        server = get_server(interaction.guild.id)
        if not server:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return

        user_meeting_message = config.user_meeting_message.format(user_name=interaction.user.mention)
        embed = discord.Embed(title='In meeting', description=user_meeting_message, color=discord.Color.green())
        await LogManager.send_log_message(interaction.guild, embed)
        await interaction.followup.send(config.meeting_message, ephemeral=True)

        if not isinstance(interaction.user, discord.Member):        
            return

        clock_role_id = server.get('clockRoleId')
        break_role_id = server.get('breakRoleId')
        meeting_role_id = server.get('meetingRoleId')

        add_meeting_role = asyncio.create_task(add_role(interaction.user, interaction.guild, meeting_role_id))
        remove_break_role = asyncio.create_task(remove_role(interaction.user, break_role_id))
        remove_clock_role = asyncio.create_task(remove_role(interaction.user, clock_role_id))
        meeting_in_task = asyncio.create_task(meeting_in(interaction, interaction.user))

        await add_meeting_role
        await remove_break_role
        await remove_clock_role
        await meeting_in_task
        # await remove_role(interaction.user, clock_role_id)
        # await remove_role(interaction.user, break_role_id)
        # await add_role(interaction.user, interaction.guild, meeting_role_id)

        # await meeting_in(interaction, interaction.user)