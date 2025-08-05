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
- PostgreSQL
- MongoDB
- Docker (optional, but recommended)

### Installation (without Docker)

1. **Clone the repository**

   ```bash
   git clone https://github.com/Stormesh/clock-in-bot.git
   cd clock-in-bot
   ```

2. **Create a Python virtual environment and install dependencies**

   ```bash
   cd server # Move to the server directory
   python -m venv venv # Create a virtual environment
   source venv/bin/activate # Activate the virtual environment
   pip install -r requirements.txt
   cd .. # Move back to the root directory
   ```

3. **Set up the Discord bot**

   - Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Rename/copy the `.env.example` file to `.env` in the `/server/` directory.
   - Copy the bot token and add it to the `/server/.env` file like this...
     ```
     BOT_TOKEN=your_token_here
     ```
   - In your server directory, run the following command:
     ```bash
     python main.py
     ```

4. **Set up the Next.js web app**

   - Rename/copy the `.env.example` file to `.env` in the `/client/` directory.
   - Copy the auth secret if needed and add it to the `/client/.env` file like this...
     ```
     AUTH_SECRET=your_auth_secret
     ```
   - In your client directory, run the following commands:
     ```bash
     npm install # To install dependencies
     npx auth secret # To create an auth secret
     ```

5. **Set up the bot on your Discord server**

   - Create a new Discord server or use an existing one.
   - Add the bot to your server using the OAuth2 URL generated on the Discord Developer Portal.
   - Give the bot the necessary permissions to read and send messages.
   - Create a new text channel to deploy the bot.
   - Create a text channel for the bot to send status updates (logs arg).
   - Create a role for users to be able to clock in (role arg).
   - Then use the bot channel, logs channel and the role in the setup command like this:
     ```bash
     /setup channel name role logs
     ```
   - [Optional] You can add 4 more roles for clocking in, break, meeting and part time users.
   - [Optional] You can add a SheetDB API URL for Google Sheets support.

6. **Set up the PostgreSQL database**

   - Install and start PostgreSQL.
   - Make sure to change `POSTGRES_USER` and `POSTGRES_PASSWORD` in the `.env` file in the `/server/` directory to match your PostgreSQL credentials.
   - Create a new database named `clockinbot`.
   - In the server folder, after installing the required python packages, run the following command:
     ```bash
     alembic upgrade head
     ```
   - This will create the database tables and apply any pending migrations.

   **Note**: If you're having trouble setting up PostgreSQL, refer to the [PostgreSQL documentation](https://www.postgresql.org/docs/current/tutorial-start.html) for installation and setup instructions, or even better, use a Docker container for PostgreSQL.

7. **Set up the MongoDB database**

   - Install and start MongoDB.
   - Make sure to change `MONGODB_URI` in the `.env` file in the `/server/` directory to match your MongoDB connection string.
   - In the client folder, after installing the required node packages, run the following command:
     ```bash
     npm run init
     ```
   - Enter your own root user credentials to create the admin user, which will be used to log into the web app.
   - If successful, the MongoDB database will be set up and you can proceed to the next step.

8. **Run the app**
  - You can now run the flask server and the Next.js app by running the following commands from the root directory:
    ```bash
    npm install # To install dependencies
    npm run build # To build the Next.js app
    npm start # To start the Next.js app and the Flask server
    ```
   - Visit `http://localhost:3000` to see the web app in action.
   - Log into the web app with the admin user credentials.
   - The Flask server will send user data to the Next.js app for real-time monitoring.
   - You can modify the code in the `/server/` and `/client/` folders to customize the behavior of the app.

### Installation (with Docker - `Recommended`)

1. **Clone the repository**

   ```bash
   git clone https://github.com/Stormesh/clock-in-bot.git
   cd clock-in-bot
   ```

2. **Set up the Discord bot**

   - Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Rename/copy the `.env.example` file to `.env` in the `/server/` directory.
   - Copy the bot token and add it to the `/server/.env` file like this...
     ```
     BOT_TOKEN=your_token_here
     ```

3. **Set up the Next.js web app**

   - Rename/copy the `.env.example` file to `.env` in the `/client/` directory.
   - Run the following command from the client directory:
     ```bash
     npx auth secret # To create an auth secret
     ```
   - Copy the auth secret if needed and add it to the `/client/.env` file like this...
     ```
     AUTH_SECRET=your_auth_secret
     ```

4. **Set up the PostgreSQL database**

   - Run the following command:
     ```bash
     docker compose run --rm server alembic upgrade head
     ```
   - This will create the database tables and apply any pending migrations.

5. **Set up the MongoDB database**

   - Write the following command in the terminal:
     ```bash
     docker compose run --rm web npm run init
     ```
   - Enter your own root user credentials to create the admin user, which will be used to log into the web app.
   - If successful, the MongoDB database will be set up and you can proceed to the next step.

6. **Build and run the Docker containers**

   - Run the following command from the root directory:
     ```bash
     docker compose up -d --build
     ```

7. **Set up the bot on your Discord server**

   - Create a new Discord server or use an existing one.
   - Add the bot to your server using the OAuth2 URL generated on the Discord Developer Portal.
   - Give the bot the necessary permissions to read and send messages.
   - Create a new text channel to deploy the bot.
   - Create a text channel for the bot to send status updates (logs arg).
   - Create a role for users to be able to clock in (role arg).
   - Then use the bot channel, logs channel and the role in the setup command like this:
     ```bash
     /setup channel name role logs
     ```
   - [Optional] You can add 4 more roles for clocking in, break, meeting and part time users.
   - [Optional] You can add a SheetDB API URL for Google Sheets support.


8. **Access the web app**

   - Visit `http://localhost:3000` to see the web app in action.
   - Log into the web app with the admin user credentials.
   - The Flask server will send user data to the Next.js app for real-time monitoring.
   - You can modify the code in the `/server/` and `/client/` folders to customize the behavior of the app.

## Dashboard

The web app provides a dashboard for monitoring agents. It shows who is clocked in, on break, or in a meeting.

![Dashboard](/preview/dashboard.png)

### Roles

There are 4 roles for users to monitor the dashboard, each with different permissions.
| Role        | Permissions                                                                               |
| :---------- | :---------------------------------------------------------------------------------------: |
| Client      | Can only view the dashboard                                                               |
| User        | Can view and kick/warn clocked in users                                                   |
| Admin       | Same as User, but can create accounts and view admin logs                                 |
| Super Admin | Has all permissions above, but can delete accounts (including admins) and update accounts |

## Usage

1. **Clock-In/Clock-Out**

   - Users can clock in and out by pressing the `Clock In` or `Clock Out` buttons.

2. **Break Management**

   - Users can go on breaks by pressing the `Break` button.
   - Users can end their breaks by pressing the `Clock Back` button.

3. **Meeting Status**

   - Users can set their status to `In a Meeting` by pressing the `Meeting` button.
   - Users can set their status to `Not in a Meeting` by pressing the `Clock Back` button.

4. **Real-Time Monitoring**

   - The web app updates user statuses in real-time.
   - The admin can see who is clocked in, on break, or in a meeting.

## Todo

- Add tabs for different user groups to monitor their activity.
- Add a system to track users when they are actively monitoring the dashboard.


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
