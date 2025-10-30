import os
import shutil
from uuid import UUID
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate
import mimetypes

# All docs stored under this folder inside backend root
STORAGE_DIR = os.path.join(os.getcwd(), "storage", "documents")
os.makedirs(STORAGE_DIR, exist_ok=True)


def save_document_file(file: UploadFile, new_filename: str) -> str:
    """
    Save uploaded file to storage/documents and return its absolute path.
    """
    file_path = os.path.join(STORAGE_DIR, new_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


def create_document(
    db: Session,
    data: DocumentCreate,
    file: UploadFile
) -> Document:
    """
    Create a document record and save file locally.
    """
    # Extract extension safely
    ext = os.path.splitext(file.filename)[1] or ""

    # Fallback: derive extension from MIME if missing or unknown
    if not ext or ext == "":
        mime_map = {
            "application/pdf": ".pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/msword": ".doc",
            "text/plain": ".txt",
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
        }
        ext = mime_map.get(
            file.content_type,
            mimetypes.guess_extension(file.content_type or "") or ""
        )

    # Create unique stored filename (avoid collisions)
    stored_name = f"{data.project_id}_{uuid.uuid4()}{ext}"

    # ✅ Save actual file to disk
    save_document_file(file, stored_name)

    # ✅ Create DB record after successful save
    doc = Document(
        project_id=data.project_id,
        filename=stored_name,
        original_name=data.original_name,
        file_type=data.file_type or file.content_type,
        file_size=data.file_size or getattr(file, "size", None),
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def list_documents(db: Session, project_id: UUID):
    """
    List all documents under a given project.
    """
    return (
        db.query(Document)
        .filter(Document.project_id == project_id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )


def delete_document(db: Session, doc_id: UUID) -> bool:
    """
    Delete document record and file from disk.
    """
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        return False

    file_path = os.path.join(STORAGE_DIR, doc.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(doc)
    db.commit()
    return True
