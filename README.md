# Discord Clock-In Bot

This Discord bot helps in monitoring users' clock-in, break, and meeting statuses in real-time. The bot tracks user activity, allowing for effective time management and easy monitoring of current statuses.

## Features

- **Clock-In/Clock-Out**: Users can clock in and out of work.
- **Break Management**: Track when users go on and off breaks.
- **Meeting Status**: Monitor users when they are in meetings.
- **Real-Time Monitoring**: The web app updates user statuses in real-time with clarity, showing who is clocked in, on break, or in a meeting.
- **Flask Integration**: Sends user data to a Next.js web app for real-time monitoring of who is clocked in.
- **Login System**: Users can log in to the web app to monitor agents.

## Setup and Installation

### Prerequisites

- Python 3.x
- Node.js

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Stormesh/ClockInBot.git
   cd ClockInBot
   ```

2. **Create a Python Virtual Environment and Install Dependencies**

   ```bash
   cd server # Move to the server directory
   python -m venv venv # Create a virtual environment
   source venv/bin/activate # Activate the virtual environment
   pip install -r requirements.txt
   cd .. # Move back to the root directory
   ```

3. **Set Up Discord Bot**

   - Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Copy the bot token and add it to the `/server/.env` file like this...
     ```
     BOT_TOKEN=your_token_here
     ```

4. **Set up the bot on your Discord server**

   - Create a new Discord server or use an existing one.
   - Add the bot to your server using the OAuth2 URL generated on the Discord Developer Portal.
   - Give the bot the necessary permissions to read and send messages.
   - Create a new text channel for the bot to send messages.

6. **Set up the Next.js Web App**

   - In your client directory, run the following commands:
     ```bash
     cd client # Move to the client directory
     npm install # To install dependencies
     cd .. # Move back to the root directory
     ```

7. **Run the app**
  - You can now run the flask server and the Next.js app by running the following commands:
    ```bash
    npm install # To install dependencies
    npm run dev # To start the Next.js app
    ```
    ```bash
   - Visit `http://localhost:3000` to see the web app in action.
   - The Flask server will send user data to the Next.js app for real-time monitoring.
   - You can customize the web app to suit your needs.

## Usage

1. **Clock-In/Clock-Out**

   - Users can clock in and out by pressing the `Clock In` or `Clock Out` buttons.

2. **Break Management**

   - Users can go on breaks by pressing the `Break` button.
   - Users can end their breaks by pressing the `Clock Back` button.

3. **Meeting Status**

   - Users can set their status to `In a Meeting` by pressing the `Meeting In` button.
   - Users can set their status to `Not in a Meeting` by pressing the `Clock Back` button.

4. **Real-Time Monitoring**

   - The web app updates user statuses in real-time.
   - The admin can see who is clocked in, on break, or in a meeting.

## Todo

- Add tabs for different user groups to monitor their activity.
- Add a system to track users when they are actively monitoring the dashboard + check how many IPs are logged into this user's account.
- 


## Contributing

Feel free to contribute to this project and help make it better. You can contribute by:

- Forking the repository
- Cloning the repository to your local machine
- Creating a new branch for your changes
- Making your changes
- Pushing your changes to your fork
- Submitting a pull request

## License

This project is licensed under the MIT License.
