# app/db/init_models.py
from app.db.base import Base
from app.db.session import engine

# Import models here (so they're registered before table creation)
from app.auth.models import User
from app.models.project import Project
from app.models.column import BoardColumn
from app.models.task import Task
from app.models.document import Document
from app.models.project_hub import ProjectHubSection


def init_db():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ All database tables created successfully.")