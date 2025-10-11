from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID
from app.deps import get_db, get_current_user
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut
from app.models.project import Project
import re
router = APIRouter(prefix="/tasks", tags=["tasks"])

def _prefix_from_name(name: str) -> str:
    # take letters from words, collapse non-letters, first 3 upper
    letters = re.sub(r'[^A-Za-z]+', ' ', name).strip().split()
    base = ''.join(w[0] for w in letters) or name[:3]
    return base.upper()[:3]


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == body.project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    # 🧠 FIX: normalize the status before saving
    allowed_statuses = {"to_do", "in_progress", "validation", "done"}
    status_value = str(body.status)
    if status_value not in allowed_statuses:
        status_value = "to_do"  # fallback

    new_task = Task(
        title=body.title,
        description=body.description,
        status=status_value,
        assignee=body.assignee,
        project_id=body.project_id,
        user_id=current_user.id,
    )
    prefix = _prefix_from_name(project.name)

    # get next story number for this project
    next_num = (
        db.query(func.coalesce(func.max(Task.story_num), 0) + 1)
        .filter(Task.project_id == body.project_id)
        .scalar()
    )

    new_task.story_num = next_num
    new_task.story_code = f"{prefix}-{next_num}"
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/project/{project_id}", response_model=list[TaskOut])
def get_tasks_for_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    rows = (
        db.query(Task)
        .filter(Task.project_id == project_id, Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .all()
    )
    return rows


@router.patch("/{task_id}/status", response_model=TaskOut)
def update_task_status(
    task_id: UUID,
    body: dict,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update only the task status (used when dragging cards between columns).
    """
    new_status = body.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="Status is required")

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Normalize underscores -> hyphens for backend consistency
    status_value = str(new_status)
    allowed_statuses = {"to_do", "in_progress", "validation", "done"}
    if status_value not in allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status '{new_status}'")

    task.status = status_value
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
