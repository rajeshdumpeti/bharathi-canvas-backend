from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.deps import get_db, get_current_user
from app.auth.models import User
from app.models.project import Project
from app.schemas.document import DocumentCreate, DocumentOut
from app.services import document_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def upload_document(
    project_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a document for a specific project.
    """
    # 1️⃣ Check project ownership
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_user_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    # 2️⃣ Prepare schema
    doc_data = DocumentCreate(
        project_id=project_id,
        original_name=file.filename,
        file_type=file.content_type,
        file_size=None,
    )

    # 3️⃣ Save and persist
    doc = document_service.create_document(db, doc_data, file)
    return doc


@router.get("/project/{project_id}", response_model=list[DocumentOut])
def list_project_documents(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all documents belonging to a given project.
    """
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.owner_user_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    return document_service.list_documents(db, project_id)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a document by ID.
    """
    # Ownership check via join
    doc = (
        db.query(Project)
        .join(Project.documents)
        .filter(Project.owner_user_id == current_user.id)
        .filter(Project.documents.any(id=document_id))
        .first()
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found or access denied")

    success = document_service.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")

    return None
