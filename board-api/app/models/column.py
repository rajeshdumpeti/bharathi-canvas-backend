from sqlalchemy import Column as SAColumn, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class BoardColumn(Base):
    __tablename__ = "columns"

    id = SAColumn(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # <-- UUID auto
    project_id = SAColumn(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    # slug like "to-do", "in-progress", etc.
    key = SAColumn(String(64), nullable=False)                                # <-- store slug here
    title = SAColumn(String(255), nullable=False)
    pos = SAColumn(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint("project_id", "key", name="uq_columns_project_key"),  # no duplicates per project
    )