import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
    SYNC_SQLALCHEMY_DATABASE_URL = os.getenv("SYNC_SQLALCHEMY_DATABASE_URL")
    TEST_SQLALCHEMY_DATABASE_URL = os.getenv("TEST_SQLALCHEMY_DATABASE_URL")
    TEST_DB_NAME = os.getenv("TEST_DB_NAME")


settings = Settings()
