from sqlmodel import Session, select
from .db import db_engine
from .models import Server, Channel, Role, ChannelRoleLink
from typing import TypedDict, Optional

from dataclasses import dataclass


class UserData(TypedDict):
    id: int
    guildId: int
    channelId: int
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
    user_dict = {user["id"]: user for user in user_data}
    return user_dict.get(user_id)


def remove_user(user_id: int):
    try:
        user = get_user(user_id)
        if not user:
            return

        user_data.remove(user)
    except ValueError:
        print("User not found in user_data.")


# Channels
def get_channel(channel_id: int):
    with Session(db_engine) as session:
        try:
            statement = select(Channel).where(Channel.id == channel_id)
            channel = session.exec(statement).one()
            return channel
        except Exception as e:
            session.rollback()
            print(f"Error getting channel {channel_id}: {e}")
            return None


def get_channel_ids_and_names_from_server(server_id: int):
    with Session(db_engine) as session:
        try:
            statement = select(Channel.id, Channel.name).where(
                Channel.server_id == server_id
            )
            channels = session.exec(statement).all()
            return channels
        except Exception as e:
            session.rollback()
            print(f"Error getting channels from server {server_id}: {e}")
            return None


def get_channels_from_server(server_id: int):
    with Session(db_engine) as session:
        try:
            statement = select(Channel).where(Channel.server_id == server_id)
            channels = session.exec(statement).all()
            return channels
        except Exception as e:
            session.rollback()
            print(f"Error getting channels from server {server_id}: {e}")
            return None


def set_channel(
    channel_id: int,
    server_id: int,
    name: Optional[str] = None,
    message_id: Optional[int] = None,
    log_id: Optional[int] = None,
    sheet_url: Optional[str] = None,
    roles: Optional[list[Role]] = None,
):
    with Session(db_engine) as session:
        try:
            statement = select(Channel).where(Channel.id == channel_id)
            channel = session.exec(statement).one_or_none()

            # Handle the roles first - check if they already exist to avoid duplicate key errors
            if roles:
                for i, role in enumerate(roles):
                    try:
                        # Check if the role already exists
                        existing_role = session.exec(select(Role).where(Role.id == role.id)).one_or_none()
                        if existing_role:
                            # Use the existing role instead
                            existing_role.type = role.type
                            roles[i] = existing_role  # Replace with existing role
                        else:
                            # If it doesn't exist, add it
                            session.add(role)
                    except Exception as role_error:
                        print(f"Error checking/adding role {role.id}: {role_error}")

            # Now handle the channel
            if not channel:
                channel = Channel(
                    id=channel_id,
                    server_id=server_id,
                    name=name,
                    log_id=log_id,
                    sheet_url=sheet_url,
                    message_id=message_id,
                    roles=roles or [],
                )
            else:
                if name is not None:
                    channel.name = name
                if log_id is not None:
                    channel.log_id = log_id
                if sheet_url is not None:
                    channel.sheet_url = sheet_url
                if message_id is not None:
                    channel.message_id = message_id
                if roles is not None:
                    channel.roles = roles

            session.add(channel)
            session.commit()
            session.refresh(channel)

            if roles:
                for role in roles:
                    try:
                        session.refresh(role)
                    except Exception as refresh_error:
                        print(f"Error refreshing role {role.id}: {refresh_error}")

            print(f"Channel setup complete: {channel}")

        except Exception as e:
            session.rollback()
            print(f"Error setting channel {channel_id}: {e}")


def remove_channel(channel_id: int):
    with Session(db_engine) as session:
        try:
            # Get channel first
            statement = select(Channel).where(Channel.id == channel_id)
            channel = session.exec(statement).one_or_none()

            if channel:
                # Keep track of role IDs before deleting the channel
                role_ids = [(role.id, role.type) for role in channel.roles]

                # Delete the channel (this should automatically remove ChannelRoleLink entries)
                session.delete(channel)
                session.commit()

                # Log the removed channel and its roles for debugging
                print(f"Removed channel {channel_id} with roles: {role_ids}")
            else:
                print(f"Channel {channel_id} not found")

        except Exception as e:
            session.rollback()
            print(f"Error removing channel {channel_id}: {e}")

# Servers
def get_server(server_id: int):
    with Session(db_engine) as session:
        try:
            statement = select(Server).where(Server.id == server_id)
            server = session.exec(statement).one()
            print(server)
            return server
        except Exception as e:
            session.rollback()
            print(f"Error getting server {server_id}: {e}")
            return None


def get_servers():
    with Session(db_engine) as session:
        try:
            statement = select(Server)
            servers = session.exec(statement).all()
            return servers
        except Exception as e:
            session.rollback()
            print(f"Error getting servers: {e}")
            return None


def set_server(server_id: int, server_name: str):
    with Session(db_engine) as session:
        try:
            statement = select(Server).where(Server.id == server_id)
            server = session.exec(statement).one_or_none()

            if not server:
                server = Server(id=server_id, name=server_name)
            else:
                server.name = server_name
            print(server)
            session.add(server)
            session.commit()
            session.refresh(server)
        except Exception as e:
            session.rollback()
            print(f"Error setting server {server_id}: {e}")


# Roles
def get_role(channel_id: int, role_type: str):
    with Session(db_engine) as session:
        try:
            statement = (
                select(ChannelRoleLink)
                .where(ChannelRoleLink.channel_id == channel_id)
                .join(Role)
                .where(Role.type == role_type)
            )
            role = session.exec(statement).one_or_none()
            return role
        except Exception as e:
            session.rollback()
            print(f"Error getting role {role_type}: {e}")
            return None


def get_roles(channel_id: int):
    with Session(db_engine) as session:
        try:
            statement = select(Channel).where(Channel.id == channel_id)
            channel = session.exec(statement).one_or_none()
            if channel:
                roles = channel.roles
                return roles
            return channel
        except Exception as e:
            session.rollback()
            print(f"Error getting roles from channel {channel_id}: {e}")
            return None


@dataclass
class RoleIds:
    clock_id: Optional[int]
    break_id: Optional[int]
    meeting_id: Optional[int]
    part_id: Optional[int]
    full_id: Optional[int]


def get_roles_ids(channel_id: int):
    roles = get_roles(channel_id)
    clock_id = break_id = meeting_id = part_id = full_id = None
    if not roles:
        return None
    for role in roles:
        if role.type == "clock":
            clock_id = role.id
        elif role.type == "break":
            break_id = role.id
        elif role.type == "meeting":
            meeting_id = role.id
        elif role.type == "part":
            part_id = role.id
        elif role.type == "full":
            full_id = role.id
    return RoleIds(clock_id, break_id, meeting_id, part_id, full_id)


def set_role(role_id: int, role_type: str, channel_id: Optional[int] = None):
    with Session(db_engine) as session:
        try:
            statement = select(Role).where(Role.id == role_id)
            role = session.exec(statement).one_or_none()
            if not role:
                role = Role(id=role_id, type=role_type)
            else:
                role.type = role_type
            if channel_id:
                channel = get_channel(channel_id)
                if channel and channel not in role.channels:
                    role.channels.append(channel)
            print(role)
            session.add(role)
            session.commit()
            session.refresh(role)
        except Exception as e:
            session.rollback()
            print(f"Error setting role {role_id}: {e}")


def is_clocked_in(user_id: int):
    user = get_user(user_id)
    return user and (user["isClockedIn"] or user["onBreak"] or user["onMeeting"])


def get_current_time(user_id: int):
    user = get_user(user_id)
    if not user:
        return 0
    return user["clockTime"] + user["meetingTime"]
