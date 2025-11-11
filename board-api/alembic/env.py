import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv  # <-- add this line

from app.db.base import Base
from app.core.config import settings
from app.auth.models import User
from app.models import column, document, feature, project, project_hub, story_seq, task
# load env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def get_url() -> str | None:
    return os.getenv("DATABASE_URL")

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = get_url()
    if not url:
        raise RuntimeError("DATABASE_URL not set in environment")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    url = get_url()
    if not url:
        raise RuntimeError("DATABASE_URL not set in environment")
    connectable = create_engine(url, poolclass=pool.NullPool, future=True)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
