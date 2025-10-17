from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from datetime import datetime
from app.models.project_hub import ProjectHubSection
from app.schemas.project_hub import ProjectHubSectionCreate
from fastapi import HTTPException, status


def get_all_sections_for_project(db: Session, project_id: UUID):
    """Fetch all hub sections for a given project."""
    try:
        return (
            db.query(ProjectHubSection)
            .filter(ProjectHubSection.project_id == project_id)
            .all()
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching sections: {str(e)}"
        )


def get_section_by_type(db: Session, project_id: UUID, section_type: str):
    """Fetch a single section by type."""
    section = (
        db.query(ProjectHubSection)
        .filter(
            ProjectHubSection.project_id == project_id,
            ProjectHubSection.section_type == section_type,
        )
        .first()
    )
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section '{section_type}' not found for project {project_id}",
        )
    return section


def create_or_update_section(db: Session, payload: ProjectHubSectionCreate):
    """Create new section or update existing one for a project."""
    existing = (
        db.query(ProjectHubSection)
        .filter(
            ProjectHubSection.project_id == payload.project_id,
            ProjectHubSection.section_type == payload.section_type,
        )
        .first()
    )

    now = datetime.utcnow().isoformat()

    if existing:
        existing.content = payload.content
        existing.updated_at = now
    else:
        new_section = ProjectHubSection(
            project_id=payload.project_id,
            section_type=payload.section_type,
            content=payload.content,
            created_by=payload.created_by,
            created_at=now,
            updated_at=now,
        )
        db.add(new_section)

    try:
        db.commit()
        db.refresh(existing if existing else new_section)
        return existing if existing else new_section
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving section: {str(e)}"
        )


def delete_section(db: Session, project_id: UUID, section_type: str):
    """Delete a section for a given project."""
    section = (
        db.query(ProjectHubSection)
        .filter(
            ProjectHubSection.project_id == project_id,
            ProjectHubSection.section_type == section_type,
        )
        .first()
    )
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section '{section_type}' not found."
        )
    try:
        db.delete(section)
        db.commit()
        return {"message": f"Section '{section_type}' deleted successfully."}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting section: {str(e)}"
        )
