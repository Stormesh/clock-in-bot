import aiofiles, json
import discord
import logging
from typing import Optional

data: list[dict[str, str | int]] = []

async def read_data(file_path: str):
    global data
    async with aiofiles.open(file_path, 'r') as f:
        data = json.loads(await f.read())

async def save_data(file_path: str):
    async with aiofiles.open(file_path, 'w') as f:
        await f.write(json.dumps(data, indent=4))

def get_data():
    return data

async def add_data(new_data: dict[str, str | int], file_path: str):
    data.append(new_data)
    await save_data(file_path)

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