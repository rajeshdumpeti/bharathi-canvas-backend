from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.deps import get_db
from app.models.project import Project
from app.models.column import BoardColumn
from app.schemas.column import BoardColumnOut, BoardColumnCreate

router = APIRouter(prefix="/projects", tags=["columns"])


@router.get("/{project_id}/columns", response_model=list[BoardColumnOut])
def list_columns(project_id: UUID, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    rows = (
        db.query(BoardColumn)
        .filter(BoardColumn.project_id == project_id)
        .order_by(BoardColumn.pos)
        .all()
    )
    return rows


@router.post("/{project_id}/columns", response_model=BoardColumnOut, status_code=status.HTTP_201_CREATED)
def create_column(project_id: UUID, payload: BoardColumnCreate, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    key = payload.title.lower().replace(" ", "-")

    existing = (
        db.query(BoardColumn)
        .filter(BoardColumn.project_id == project_id, BoardColumn.key == key)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Column key already exists")

    pos = db.query(BoardColumn).filter(BoardColumn.project_id == project_id).count()
    new_col = BoardColumn(project_id=project_id, key=key, title=payload.title, pos=pos)
    db.add(new_col)
    db.commit()
    db.refresh(new_col)

    return new_col
