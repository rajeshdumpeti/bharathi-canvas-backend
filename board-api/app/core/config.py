from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 60

    database_url: str
    cors_origins: List[AnyHttpUrl] | List[str] = []

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }

settings = Settings(
    secret_key="change-this",
    database_url="postgresql+psycopg2://postgres:postgres@db:5432/boarddb",
)
