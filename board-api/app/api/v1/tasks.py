from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from datetime import datetime
from app.deps import get_db
from app.models.project import Project
from app.models.column import BoardColumn
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut
from app.services.story_id import next_story_id

router = APIRouter()

def map_status_to_column_key(status: str) -> str:
    s = (status or "").lower()
    if s in ("to-do", "todo"): return "to-do"
    if s in ("in-progress",): return "in-progress"
    if s in ("validation",): return "validation"
    if s in ("done",): return "done"
    return "to-do"

@router.get("/{project_id}/tasks", response_model=list[TaskOut])
def list_tasks(
    project_id: UUID,
    status: str | None = Query(default=None),
    assignee: str | None = Query(default=None),
    q: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    if not db.get(Project, project_id):
        raise HTTPException(404, "Project not found")

    stmt = select(Task).where(Task.project_id == project_id)
    if status:
        stmt = stmt.where(Task.column_key == map_status_to_column_key(status))
    if assignee:
        stmt = stmt.where(Task.assignee == assignee)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(Task.title.ilike(like))
    tasks = db.execute(stmt.order_by(Task.created_at.desc())).scalars().all()

    return [
        TaskOut(
            id=str(t.id),
            project=str(t.project_id),
            title=t.title,
            description=t.description,
            acceptanceCriteria=t.acceptance_criteria,
            assignee=t.assignee,
            priority=t.priority,
            architecture=t.architecture,
            status=t.column_key,
            storyId=t.story_id,
            createdAt=t.created_at,
            dueDate=t.due_date,
            completedAt=t.completed_at,
        )
        for t in tasks
    ]

@router.post("/{project_id}/tasks", response_model=TaskOut, status_code=201)
def create_task(project_id: UUID, payload: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(Project, project_id):
        raise HTTPException(404, "Project not found")

    col_key = map_status_to_column_key(payload.status)
    if not db.query(BoardColumn).filter(BoardColumn.project_id==project_id, BoardColumn.key==col_key).first():
        raise HTTPException(400, "Invalid column/status")

    story_id = payload.storyId or next_story_id(db, project_id)
    t = Task(
        project_id=project_id,
        column_key=col_key,
        title=payload.title.strip(),
        description=payload.description,
        acceptance_criteria=payload.acceptanceCriteria,
        assignee=payload.assignee,
        priority=payload.priority,
        architecture=payload.architecture,
        story_id=story_id,
        due_date=payload.dueDate,
    )
    db.add(t); db.commit(); db.refresh(t)

    return TaskOut(
        id=str(t.id),
        project=str(t.project_id),
        title=t.title,
        description=t.description,
        acceptanceCriteria=t.acceptance_criteria,
        assignee=t.assignee,
        priority=t.priority,
        architecture=t.architecture,
        status=t.column_key,
        storyId=t.story_id,
        createdAt=t.created_at,
        dueDate=t.due_date,
        completedAt=t.completed_at,
    )

@router.patch("/{project_id}/tasks/{task_id}", response_model=TaskOut)
def update_task(project_id: UUID, task_id: UUID, payload: TaskCreate, db: Session = Depends(get_db)):
    t = db.get(Task, task_id)
    if not t or str(t.project_id) != str(project_id):
        raise HTTPException(404, "Task not found")

    if payload.status:
        t.column_key = map_status_to_column_key(payload.status)
        if t.column_key == "done" and not t.completed_at:
            t.completed_at = datetime.utcnow()

    for field, source in [
        ("title", payload.title),
        ("description", payload.description),
        ("assignee", payload.assignee),
        ("priority", payload.priority),
        ("architecture", payload.architecture),
    ]:
        if source is not None:
            setattr(t, field, source)

    if payload.acceptanceCriteria is not None:
        t.acceptance_criteria = payload.acceptanceCriteria
    if payload.dueDate is not None:
        t.due_date = payload.dueDate

    db.add(t); db.commit(); db.refresh(t)

    return TaskOut(
        id=str(t.id),
        project=str(t.project_id),
        title=t.title,
        description=t.description,
        acceptanceCriteria=t.acceptance_criteria,
        assignee=t.assignee,
        priority=t.priority,
        architecture=t.architecture,
        status=t.column_key,
        storyId=t.story_id,
        createdAt=t.created_at,
        dueDate=t.due_date,
        completedAt=t.completed_at,
    )

@router.delete("/{project_id}/tasks/{task_id}", status_code=204)
def delete_task(project_id: UUID, task_id: UUID, db: Session = Depends(get_db)):
    t = db.get(Task, task_id)
    if not t or str(t.project_id) != str(project_id):
        raise HTTPException(404, "Task not found")
    db.delete(t); db.commit()
    return
