from typing import TypedDict

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