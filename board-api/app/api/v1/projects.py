from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.deps import get_db
from app.models.project import Project
from app.models.column import BoardColumn
from app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter()

DEFAULT_COLS = [
    ("to-do", "To Do", 0),
    ("in-progress", "In Progress", 1),
    ("validation", "Validation", 2),
    ("done", "Done", 3),
]

@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

@router.post("", response_model=ProjectOut, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    p = Project(name=payload.name)
    db.add(p); db.flush()
    for key, title, pos in DEFAULT_COLS:
        db.add(BoardColumn(project_id=p.id, key=key, title=title, pos=pos))
    db.commit()
    db.refresh(p)
    return p

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    p = db.get(Project, project_id)
    if not p:
        raise HTTPException(404, "Project not found")
    return p
