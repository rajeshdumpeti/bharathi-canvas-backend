from sqlalchemy import Column as SACol, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class BoardColumn(Base):
    __tablename__ = "columns"
    id = SACol(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = SACol(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    key = SACol(String(64), nullable=False)   # e.g., to-do, in-progress
    title = SACol(String(128), nullable=False)
    pos = SACol(Integer, nullable=False, default=0)
