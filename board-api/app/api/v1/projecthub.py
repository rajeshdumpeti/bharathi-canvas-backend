from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.deps import get_db, get_current_user
from app.auth.models import User
from app.models.project import Project
from app.schemas.project_hub import ProjectHubSectionCreate, ProjectHubSectionOut
from app.services import project_hub_service

router = APIRouter(prefix="/projects", tags=["projecthub"])


@router.get("/{project_id}/hub", response_model=List[ProjectHubSectionOut])
def list_project_hub_sections(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all Project Hub sections for a project.
    """
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_user_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    return project_hub_service.get_all_sections_for_project(db, project_id)


@router.get("/{project_id}/hub/{section_type}", response_model=ProjectHubSectionOut)
def get_project_hub_section(
    project_id: UUID,
    section_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific Project Hub section by section type.
    """
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_user_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    return project_hub_service.get_section_by_type(db, project_id, section_type)


@router.post("/{project_id}/hub", response_model=ProjectHubSectionOut, status_code=status.HTTP_201_CREATED)
def create_or_update_project_hub_section(
    project_id: UUID,
    body: ProjectHubSectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create or update a Project Hub section for a project.
    """
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_user_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    payload = body.model_dump()
    payload["project_id"] = project_id
    payload["created_by"] = str(current_user.email or current_user.id)
    body.created_by = str(current_user.email or current_user.id)
    return project_hub_service.create_or_update_section(db, ProjectHubSectionCreate(**payload))


@router.delete("/{project_id}/hub/{section_type}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_hub_section(
    project_id: UUID,
    section_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a specific Project Hub section.
    """
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_user_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    project_hub_service.delete_section(db, project_id, section_type)
    return None
