from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class User(Base):
    __tablename__ = "users"

    # use real UUID in DB
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name  = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    reset_password_token = Column(String, index=True, nullable=True) 
    reset_token_expires_at = Column(DateTime(timezone=True), nullable=True)