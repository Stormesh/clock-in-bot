import os
from dotenv import load_dotenv


def load_env():
    load_dotenv(".env")
    if os.getenv("IS_DOCKER") == "true":
        load_dotenv(".env.docker")
