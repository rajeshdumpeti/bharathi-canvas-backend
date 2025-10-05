from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List, Union

class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 60

    # Database credentials
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str

    # SQLAlchemy database URL (auto-generated)
    database_url: str | None = None

    # CORS
    cors_origins: List[AnyHttpUrl] | List[str] = []

    @field_validator("database_url", mode="before")
    def assemble_db_url(cls, v, values):
        if v:
            return v
        user = values.get("postgres_user", "canvas")
        password = values.get("postgres_password", "canvas")
        host = values.get("postgres_host", "db")
        port = values.get("postgres_port", "5432")
        db = values.get("postgres_db", "canvas")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }

settings = Settings()
