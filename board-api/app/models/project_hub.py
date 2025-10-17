# app/models/project_hub.py
from sqlalchemy import Column, String, UUID, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class ProjectHubSection(Base):
    __tablename__ = "project_hub_sections"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(PG_UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    section_type = Column(String(100), nullable=False)  # e.g. 'setup', 'architecture', 'deployment'
    content = Column(JSON, nullable=False)  # flexible structure
    created_by = Column(String(100))
    updated_at = Column(String(50))
    created_at = Column(String(50))
    
    project = relationship("Project", back_populates="hub_sections")
