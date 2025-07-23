# Quart
from modules.api import app

# Bot Properties
from modules.env import load_env
from modules.bot_init import bot
from modules import bot as discord_bot_module # Ensures bot commands and events from modules.bot are registered

# Systematic imports
import asyncio, os
import uvicorn

load_env()
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = os.getenv("FLASK_PORT", 7546)


async def run_quart():
    if not (FLASK_HOST and FLASK_PORT):
        print("FLASK_HOST and/or FLASK_PORT environment variables are not set.")
        return
    config_uvicorn = uvicorn.Config(
        app, host=FLASK_HOST, port=int(FLASK_PORT), log_level="info"
    )
    server = uvicorn.Server(config_uvicorn)
    await server.serve()


async def main():
    quart_task = asyncio.create_task(run_quart())
    discord_task = asyncio.create_task(bot.start(BOT_TOKEN))

    await asyncio.gather(quart_task, discord_task)


if __name__ == "__main__":
    asyncio.run(main())
