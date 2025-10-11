from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from app.deps import get_db, get_current_user
from app.models.project import Project
from app.auth.models import User
from app.schemas.project import ProjectCreate, ProjectOut
from app.models.column import BoardColumn  # your column model

router = APIRouter(prefix="/projects", tags=["projects"])

DEFAULT_COLS = [
    {"id": "to_do", "title": "To Do"},
    {"id": "in_progress", "title": "In Progress"},
    {"id": "validation", "title": "Validation"},
    {"id": "done", "title": "Done"},
]

# helper to seed default columns
def _seed_default_columns(db, project_id):
    DEFAULTS = [
        ("to_do", "To Do"),
        ("in_progress", "In Progress"),
        ("validation", "Validation"),
        ("done", "Done"),
    ]

    rows = [
        BoardColumn(project_id=project_id, key=slug, title=title, pos=i)
        for i, (slug, title) in enumerate(DEFAULTS)
    ]
    db.add_all(rows)
    
@router.get("/", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Project)
        .options(joinedload(Project.columns))  # ✅ this loads related columns in one query
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

    _seed_default_columns(db, row.id)
    db.commit()

    return row


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .options(
            joinedload(Project.columns),
            joinedload(Project.tasks)  # 👈 include tasks
        )
        .filter(
            Project.id == project_id,
            Project.owner_user_id == current_user.id
        )
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # filter only current user’s tasks
    project.tasks = [t for t in project.tasks if t.user_id == current_user.id]
    return project
