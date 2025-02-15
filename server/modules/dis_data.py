import discord
import logging
from modules.general_data import get_server
import modules.config as config
from typing import Optional

async def remove_role(user: discord.Member, role_id: Optional[str | int]):
    if not role_id:
        logging.warning(f'User {user.display_name} does not have a role to remove')
        return
    
    try:
        role = user.get_role(int(role_id))
        if not role:
            return
        
        await user.remove_roles(role)
    except Exception as e:
        logging.error(e)

async def add_role(user: discord.Member, guild: discord.Guild, role_id: Optional[str | int]):
    if not role_id:
        logging.warning(f'User {user.display_name} does not have a role to add')
        return

    try:
        role = guild.get_role(int(role_id))
        if not role:
            logging.error(f'Role {role_id} not found')
            return

        if role in user.roles:
            logging.warning(f'User {user.display_name} already has role {role.name}')
            return    

        await user.add_roles(role)
    except Exception as e:
        logging.error(e)

async def send_dm(user: discord.Member, message: str):
    try:
        await user.send(message)
    except discord.Forbidden as e:
        print(f'Error while sending message to {user.display_name}: {e}')

def get_shift_time(interaction: discord.Interaction, _user: discord.Member) -> int:
    if not interaction.guild:
        return 0
    
    server = get_server(interaction.guild.id)

    if not server or not interaction.guild:
        return 0

    shift_time: int = config.full_time_hour_limit
    part_agent_id = server.get('partRoleId')
    if part_agent_id:
        part_role = interaction.guild.get_role(int(part_agent_id))
        if part_role in _user.roles:
            shift_time = config.part_time_hour_limit
    return shift_time

async def remind_user_to_clock_out(user: discord.Member):
    await send_dm(user, config.remind_clock_out_message)
