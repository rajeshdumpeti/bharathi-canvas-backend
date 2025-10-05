from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.db.base import Base

class StorySeq(Base):
    __tablename__ = "story_seq"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True, default=uuid4)
    next_num = Column(Integer, nullable=False, default=234567)

    __table_args__ = (UniqueConstraint("project_id"),)
