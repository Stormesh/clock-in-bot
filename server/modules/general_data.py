from typing import TypedDict
from modules.dis_data import get_data

class UserData(TypedDict):
    id: int
    name: str
    avatar: str
    clockTime: int
    meetingTime: int
    breakTime: int
    isClockedIn: bool
    onBreak: bool
    onMeeting: bool

user_data: list[UserData] = []

def get_user(user_id: int):
    return next((user for user in user_data if user['id'] == user_id), None)

def get_server(server_id: int | None):
    return next((server for server in get_data() if server['id'] == server_id), None)
