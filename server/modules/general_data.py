import aiofiles, json
from typing import TypedDict

class UserData(TypedDict):
    id: int
    guildId: int
    name: str
    avatar: str
    clockTime: int
    meetingTime: int
    breakTime: int
    isClockedIn: bool
    onBreak: bool
    onMeeting: bool

user_data: list[UserData] = []

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

def get_user(user_id: int):
    user_dict = {user['id']: user for user in user_data}
    return user_dict.get(user_id)

def remove_user(user_id: int):
    try:
        user = get_user(user_id)
        if not user:
            return

        user_data.remove(user)
    except ValueError:
        print('User not found in user_data.')

def get_server(server_id: int):
    server_dict = {server['id']: server for server in get_data()}
    return server_dict.get(server_id)

def is_clocked_in(user_id: int):
    user = get_user(user_id)
    return user and (user['isClockedIn'] or user['onBreak'] or user['onMeeting'])

def get_current_time(user_id: int):
    user = get_user(user_id)
    if not user:
        return 0
    return user['clockTime'] + user['meetingTime']
