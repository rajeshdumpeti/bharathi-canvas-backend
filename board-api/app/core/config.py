from typing import List, Any
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator


class Settings(BaseSettings):
    # App
    app_env: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 60

    # Database (individual pieces; used to assemble DATABASE_URL if not provided)
    postgres_user: str = "canvas"
    postgres_password: str = "canvas"
    postgres_db: str = "canvas"
    postgres_host: str = "db"
    postgres_port: str = "5432"

    # Full SQLAlchemy URL (overrides the assembled one if provided)
    database_url: str | None = None

    # CORS
    cors_origins: List[AnyHttpUrl] | List[str] = []

    @field_validator("database_url", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str | None, values: Any) -> str:
        if v:
            return v
        user = values.get("postgres_user", "canvas")
        password = values.get("postgres_password", "canvas")
        host = values.get("postgres_host", "db")
        port = values.get("postgres_port", "5432")
        db = values.get("postgres_db", "canvas")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors(cls, v: Any) -> List[str] | List[AnyHttpUrl]:
        """
        Accept either:
          - JSON array string: '["http://localhost:5173","http://localhost:3000"]'
          - Comma-separated string: 'http://localhost:5173,http://localhost:3000'
          - A real python list (already parsed)
        """
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