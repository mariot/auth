import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Auth API"
    database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./auth.db")
