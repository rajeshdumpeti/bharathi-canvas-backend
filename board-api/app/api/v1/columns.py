from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.deps import get_db
from app.models.project import Project
from app.models.column import BoardColumn
from app.schemas.column import ColumnCreate, ColumnOut

router = APIRouter()

@router.get("/{project_id}/columns", response_model=list[ColumnOut])
def list_columns(project_id: UUID, db: Session = Depends(get_db)):
    if not db.get(Project, project_id):
        raise HTTPException(404, "Project not found")
    return db.query(BoardColumn).filter(BoardColumn.project_id == project_id).order_by(BoardColumn.pos).all()

@router.post("/{project_id}/columns", response_model=ColumnOut, status_code=201)
def create_column(project_id: UUID, payload: ColumnCreate, db: Session = Depends(get_db)):
    if not db.get(Project, project_id):
        raise HTTPException(404, "Project not found")
    key = payload.title.lower().replace(" ", "-")
    existing = db.query(BoardColumn).filter(BoardColumn.project_id==project_id, BoardColumn.key==key).first()
    if existing:
        raise HTTPException(409, "Column key already exists")
    max_pos = db.query(BoardColumn).filter(BoardColumn.project_id==project_id).count()
    c = BoardColumn(project_id=project_id, key=key, title=payload.title, pos=max_pos)
    db.add(c); db.commit(); db.refresh(c)
    return c
