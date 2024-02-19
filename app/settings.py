import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Auth API"
    database_url: str = os.environ.get("DATABASE_URL", "sqlite:///./auth.db")
    secret_key: str = os.environ.get("SECRET_KEY", "secret")
    algorithm: str = os.environ.get("ALGORITHM", "HS256")
    access_token_expire_minutes: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
