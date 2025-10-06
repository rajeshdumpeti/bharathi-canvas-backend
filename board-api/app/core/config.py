from typing import List, Any
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import os


class Settings(BaseSettings):
    # Environment
    app_env: str = os.getenv("APP_ENV", "development")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "local_dev_secret")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Database - for local dev, Docker, or Render
    postgres_user: str = os.getenv("POSTGRES_USER", "canvas")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "canvas")
    postgres_db: str = os.getenv("POSTGRES_DB", "canvas")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")

    database_url: str | None = os.getenv("DATABASE_URL")

    # CORS
    cors_origins: List[AnyHttpUrl] | List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,https://bharathi-canvas-frontend.onrender.com"
    )

    @field_validator("database_url", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str | None, info):
        if v:
            return v
        data = info.data if hasattr(info, "data") else {}
        user = data.get("postgres_user", "canvas")
        password = data.get("postgres_password", "canvas")
        host = data.get("postgres_host", "db")
        port = data.get("postgres_port", "5432")
        db = data.get("postgres_db", "canvas")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors(cls, v: Any) -> List[str] | List[AnyHttpUrl]:
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            if s.startswith("["):
                import json
                return json.loads(s)
            return [item.strip() for item in s.split(",") if item.strip()]
        return v

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()