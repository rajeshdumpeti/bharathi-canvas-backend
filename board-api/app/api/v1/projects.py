from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.deps import get_db, get_current_user
from app.models.project import Project
from app.auth.models import User
from app.schemas.project import ProjectCreate, ProjectOut
from app.models.column import BoardColumn  # your column model

router = APIRouter(prefix="/projects", tags=["projects"])

DEFAULT_COLS = [
    {"id": "to-do", "title": "To Do"},
    {"id": "in-progress", "title": "In Progress"},
    {"id": "validation", "title": "Validation"},
    {"id": "done", "title": "Done"},
]

@router.get("/", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Project)
        .filter(Project.owner_user_id == current_user.id)
        .order_by(Project.created_at.desc())
        .all()
    )
    return rows

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    body: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = Project(name=body.name, owner_user_id=current_user.id)
    db.add(row)
    db.commit()
    db.refresh(row)

    # Seed default columns if none exist for this project
    existing = db.query(BoardColumn).filter(BoardColumn.project_id == row.id).count()
    if existing == 0:
        for c in DEFAULT_COLS:
            db.add(BoardColumn(
                id=c["id"],    # if your model uses string id; if UUID, generate instead
                title=c["title"],
                project_id=row.id
            ))
        db.commit()

    return row

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    row = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_user_id == current_user.id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return row