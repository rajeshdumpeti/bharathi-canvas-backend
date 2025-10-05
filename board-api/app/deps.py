from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.utils.security import get_current_user_optional

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(user=Depends(get_current_user_optional)):
    # Placeholder until auth UI is wired; allow anonymous in dev.
    return user
