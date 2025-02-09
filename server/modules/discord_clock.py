import discord
import modules.config as config

from modules.clock_funcs import check_role, clock_in, clock_out, meeting_in, break_in, view_time
from modules.general_data import user_data, get_user, get_server
from modules.dis_data import remove_role, add_role
import modules.clock_str as clock_str

class LogManager:
    @staticmethod
    def get_log_channel(guild: discord.Guild):
        server = get_server(guild.id)
        if not server or not guild:
            return None
        
        log_id = int(server['logId'])
        log_channel = guild.get_channel(log_id)
        
        if not isinstance(log_channel, discord.TextChannel):
            return None
        
        return log_channel
    
    @staticmethod
    async def send_log_message(guild: discord.Guild, embed: discord.Embed):
        log_channel = LogManager.get_log_channel(guild)
        if isinstance(log_channel, discord.TextChannel):
            await log_channel.send(embed=embed)
        

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

        server = get_server(interaction.guild_id)
        if not server or not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return
        
        user_clock_in_message = config.user_clock_in_message.format(user_name=interaction.user.mention)
        embed = discord.Embed(title='Clocked in', description=user_clock_in_message, color=discord.Color.green())
        await LogManager.send_log_message(interaction.guild, embed)

        if not isinstance(interaction.user, discord.Member):
            return
        
        clockInId = server.get('clockRoleId')
        await add_role(interaction.user, interaction.guild, clockInId)

        await interaction.followup.send(config.clock_in_message, ephemeral=True)
        await clock_in(interaction, interaction.user)
        

    #Clock Out
    @discord.ui.button(label='Clock Out', style=discord.ButtonStyle.red, emoji='🛑')
    async def clock_out_view(self, interaction: discord.Interaction, button: discord.ui.Button[discord.ui.View]):
        await interaction.response.defer()

        if not await check_role(interaction):
            return

        user_id = interaction.user.id
        user = get_user(user_id)
        if not user or not user['isClockedIn']:
            await interaction.followup.send(config.not_clocked_in_message, ephemeral=True)
            return
        
        server = get_server(interaction.guild_id)
        if not server or not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return
        
        embed = discord.Embed(title='Clocked out', description=await clock_out(interaction), color=discord.Color.red())
        await LogManager.send_log_message(interaction.guild, embed)
        out_response = await clock_out(interaction, log=True)

        try:
            user_data.remove(user)
        except ValueError:
            print('User not found in user_data.')

        if isinstance(interaction.user, discord.Member):
            clock_in_id = server.get('clockRoleId')
            break_id = server.get('breakRoleId')
            meeting_id = server.get('meetingRoleId')

            await remove_role(interaction.user, clock_in_id)
            await remove_role(interaction.user, break_id)
            await remove_role(interaction.user, meeting_id)

        await interaction.followup.send(out_response, ephemeral=True)

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
                                         config.already_on_break_message) if not user['isClockedIn'] else 
                                         config.on_break_message, ephemeral=True)

        if not user['isClockedIn']:
            return

        server = get_server(interaction.guild_id)
        if not server or not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return
        
        user_on_break_message = config.user_on_break_message.format(user_name=interaction.user.mention)
        embed = discord.Embed(title='Break', description=user_on_break_message, color=discord.Color.blurple())
        await LogManager.send_log_message(interaction.guild, embed)

        if isinstance(interaction.user, discord.Member):
            clock_in_id = server.get('clockRoleId')
            break_id = server.get('breakRoleId')

            await remove_role(interaction.user, clock_in_id)
            await add_role(interaction.user, interaction.guild, break_id)

            await break_in(interaction, interaction.user)



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

        server = get_server(interaction.guild_id)
        if not server or not interaction.guild:
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

        await remove_role(interaction.user, break_id)
        await remove_role(interaction.user, meeting_id)
        await add_role(interaction.user, interaction.guild, clock_in_id)

        await clock_in(interaction, interaction.user, True)
        

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

        if not user['isClockedIn']:
            await interaction.followup.send(config.not_clocked_in_message, ephemeral=True)
            return
        
        server = get_server(interaction.guild_id)
        if not server or not interaction.guild:
            await interaction.followup.send(config.no_guild_message, ephemeral=True)
            return

        user_meeting_message = config.user_meeting_message.format(user_name=interaction.user.mention)
        embed = discord.Embed(title='In meeting', description=user_meeting_message, color=discord.Color.green())
        await LogManager.send_log_message(interaction.guild, embed)
        await interaction.followup.send(config.meeting_message, ephemeral=True)

        if not isinstance(interaction.user, discord.Member):        
            return

        clock_role_id = server.get('clockRoleId')
        meeting_role_id = server.get('meetingRoleId')

        await remove_role(interaction.user, clock_role_id)
        await add_role(interaction.user, interaction.guild, meeting_role_id)

        await meeting_in(interaction, interaction.user)