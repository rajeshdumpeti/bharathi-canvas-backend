from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)  # Added index for FK
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to BoardColumn (with backref for reverse access)
    columns = relationship(
        "BoardColumn",
        backref="project",
        cascade="all, delete-orphan",
        lazy="joined"  # Eager load for performance; adjust to "select" if needed
    )

    # Relationship to ProjectHubSection (mutual back_populates for bidirectional)
    hub_sections = relationship(
        "ProjectHubSection", 
        back_populates="project", 
        cascade="all, delete-orphan",
        lazy="select"  # Default lazy; consistent with typical use
    )