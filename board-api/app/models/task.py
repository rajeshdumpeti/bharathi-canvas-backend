from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
import uuid
import enum
class TaskStatus(str, enum.Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    validation = "validation"
    done = "done"
    
class Task(Base):
    __tablename__ = "tasks"
    story_code = Column(String(32), nullable=True, index=True)  # e.g. BHA-12
    story_num = Column(Integer, nullable=True) 

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.to_do)
    assignee = Column(String(255))
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True))
