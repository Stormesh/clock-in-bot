import toml

config = toml.load('config.toml')


no_interaction_message = config['messages']['no_interaction_message'] if config else 'You have to clock in first.'

# Clock
already_clocked_in_message = config['messages']['already_clocked_in_message'] if config else 'You have already clocked in.'
cant_reset_time_message = config['messages']['cant_reset_time_message'] if config else 'You can\'t reset your time once you\'re already clocked in.'
clock_in_message = config['messages']['clock_in_message'] if config else 'You have clocked in.'
not_clocked_in_message = config['messages']['not_clocked_in_message'] if config else 'You have not clocked in.'

# Break
break_time_limit = (config['break']['break_time'] if config else 30) * 60 # 30 minutes
part_break_time_limit = (config['break']['part_break_time'] if config else 15) * 60 # 15 minutes
already_on_break_message = config['messages']['already_on_break_message'] if config else 'You are already on break.'
on_break_message = config['messages']['on_break_message'] if config else 'You are now on break.'

# Back
already_back_message = config['messages']['already_back_message'] if config else 'You are already back in.'
back_message = config['messages']['back_message'] if config else 'You are now back in.'

# Meeting
meeting_message = config['messages']['meeting_message'] if config else 'You are now in a meeting.'
already_in_meeting_message = config['messages']['already_in_meeting_message'] if config else 'You are already in a meeting.'

# Setup
no_permission_setup_message = config['messages']['no_permission_setup_message'] if config else 'You don\'t have permission to set up the bot.'