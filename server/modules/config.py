import toml
import os

config = toml.load('config.toml') if os.path.exists('config.toml') else toml.load('config.example.toml')

no_interaction_message = config['messages']['no_interaction_message'] if config else 'You have to clock in first.'

# Clock In
already_clocked_in_message = config['messages']['already_clocked_in_message'] if config else 'You have already clocked in.'
cant_reset_time_message = config['messages']['cant_reset_time_message'] if config else 'You can\'t reset your time once you\'re already clocked in.'
clock_in_message = config['messages']['clock_in_message'] if config else 'You have clocked in.'
user_clock_in_message = config['messages']['user_clock_in_message'] if config else '{user_name} has clocked in.'
not_clocked_in_message = config['messages']['not_clocked_in_message'] if config else 'You have not clocked in.'
no_permission_clock_message = config['messages']['no_permission_clock_message'] if config else 'You don\'t have permission to clock in.'

# Clock Out
clock_out_message = config['messages']['clock_out_message'] if config else '{user_name} has clocked out.'
clock_out_data_message = config['messages']['clock_out_data_message'] if config else '{date} - {user_name} has clocked out.\n**Business Hours**\n{hours} hour{hours_s} and {minutes} minute{minutes_s}\n**Break Time**\n{break_hours} hour{break_hours_s} and {break_minutes} minute{break_minutes_s}\n**Meeting Time**\n{meeting_hours} hour{break_hours_s} and {meeting_minutes} minute{meeting_minutes_s}.'

# View Time
view_time_message = config['messages']['view_time_message'] if config else '**Working time:**\n{business_hours} hour{business_hours_s}, {business_minutes} minute{business_minutes_s} and {business_seconds} second{business_seconds_s}\n**Break time:**\n{break_hours} hour{break_hours_s}, {break_minutes} minute{break_minute_s} and {break_seconds} second{break_seconds_s}.'

# Break
break_time_limit = (config['break']['break_time'] if config else 30) * 60 # 30 minutes
part_break_time_limit = (config['break']['part_break_time'] if config else 15) * 60 # 15 minutes
already_on_break_message = config['messages']['already_on_break_message'] if config else 'You are already on break.'
on_break_message = config['messages']['on_break_message'] if config else 'You are now on break.'
user_on_break_message = config['messages']['user_on_break_message'] if config else '{user_name} went on a break.'

# Back
already_back_message = config['messages']['already_back_message'] if config else 'You are already back in.'
back_message = config['messages']['back_message'] if config else 'You are now back in.'
user_back_message = config['messages']['user_back_message'] if config else '{user_name} is now back in.'
user_break_back_message = config['messages']['user_break_back_message'] if config else '{user_name} is now back in from a break of {break_hours}h {break_minutes}m.'
user_meeting_back_message = config['messages']['user_meeting_back_message'] if config else '{user_name} is now back in from a meeting of {meeting_hours}h {meeting_minutes}m.'

# Meeting
meeting_message = config['messages']['meeting_message'] if config else 'You are now in a meeting.'
user_meeting_message = config['messages']['user_meeting_message'] if config else '{user_name} went to a meeting.'
already_in_meeting_message = config['messages']['already_in_meeting_message'] if config else 'You are already in a meeting.'

# Setup
no_permission_setup_message = config['messages']['no_permission_setup_message'] if config else 'You don\'t have permission to set up the bot.'