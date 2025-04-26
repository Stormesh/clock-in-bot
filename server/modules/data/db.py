from ..env import load_env
import os
from sqlmodel import SQLModel, create_engine
from .models import *

load_env()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set")

db_engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(db_engine)
    if SQLModel.metadata.tables:
        print("Database and tables already exist.")
        return
    print("Database and tables created successfully.")


if __name__ == "__main__":
    create_db_and_tables()
