import toml
import os
from typing import Any

# Load configuration from the appropriate TOML file
config_file = 'config.toml' if os.path.exists('config.toml') else 'config.example.toml'
config = toml.load(config_file)

def get_config_value(section: str, key: str, default: Any):
    return config.get(section, {}).get(key, default)

# Messages
no_interaction_message = get_config_value('messages', 'no_interaction_message', 'You have to clock in first.')
already_clocked_in_message = get_config_value('messages', 'already_clocked_in_message', 'You have already clocked in.')
cant_reset_time_message = get_config_value('messages', 'cant_reset_time_message', 'You can\'t reset your time once you\'re already clocked in.')
clock_in_message = get_config_value('messages', 'clock_in_message', 'You have clocked in.')
user_clock_in_message = get_config_value('messages', 'user_clock_in_message', '{user_name} has clocked in.')
not_clocked_in_message = get_config_value('messages', 'not_clocked_in_message', 'You have not clocked in.')
no_permission_clock_message = get_config_value('messages', 'no_permission_clock_message', 'You don\'t have permission to clock in.')

clock_out_message = get_config_value('messages', 'clock_out_message', '{user_name} has clocked out.')
clock_out_data_message = get_config_value(
    'messages', 'clock_out_data_message',
    '{date} - {user_name} has clocked out.\n**Business Hours**\n{hours} hour{hours_s} and {minutes} minute{minutes_s}\n'
    '**Break Time**\n{break_hours} hour{break_hours_s} and {break_minutes} minute{break_minutes_s}\n'
    '**Meeting Time**\n{meeting_hours} hour{meeting_hours_s} and {meeting_minutes} minute{meeting_minutes_s}.'
)
remind_clock_out_message = get_config_value('messages', 'remind_clock_out_message', 'Your shift is over, please clock out.')

view_time_message = get_config_value(
    'messages', 'view_time_message',
    '**Working time:**\n{business_hours} hour{business_hours_s}, {business_minutes} minute{business_minutes_s} and '
    '{business_seconds} second{business_seconds_s}\n**Break time:**\n{break_hours} hour{break_hours_s}, '
    '{break_minutes} minute{break_minute_s} and {break_seconds} second{break_seconds_s}.'
)

# Clock
full_time_hour_limit = get_config_value('clock', 'full_time_hour_limit', 8) * 3600  # 8 hours
part_time_hour_limit = get_config_value('clock', 'part_time_hour_limit', 4) * 3600  # 4 hours

# Break
break_time_limit = get_config_value('break', 'break_time', 30) * 60  # 30 minutes
part_break_time_limit = get_config_value('break', 'part_break_time', 15) * 60  # 15 minutes
already_on_break_message = get_config_value('messages', 'already_on_break_message', 'You are already on break.')
on_break_message = get_config_value('messages', 'on_break_message', 'You are now on break.')
user_on_break_message = get_config_value('messages', 'user_on_break_message', '{user_name} went on a break.')

# Back
already_back_message = get_config_value('messages', 'already_back_message', 'You are already back in.')
back_message = get_config_value('messages', 'back_message', 'You are now back in.')
user_back_message = get_config_value('messages', 'user_back_message', '{user_name} is now back in.')
user_break_back_message = get_config_value('messages', 'user_break_back_message', '{user_name} is now back in from a break of {break_hours}h {break_minutes}m.')
user_meeting_back_message = get_config_value('messages', 'user_meeting_back_message', '{user_name} is now back in from a meeting of {meeting_hours}h {meeting_minutes}m.')

# Meeting
meeting_message = get_config_value('messages', 'meeting_message', 'You are now in a meeting.')
user_meeting_message = get_config_value('messages', 'user_meeting_message', '{user_name} went to a meeting.')
already_in_meeting_message = get_config_value('messages', 'already_in_meeting_message', 'You are already in a meeting.')

# Setup
no_permission_setup_message = get_config_value('messages', 'no_permission_setup_message', 'You don\'t have permission to set up the bot.')
no_guild_message = get_config_value('messages', 'no_guild_message', 'You must be in a server to use the bot.')
