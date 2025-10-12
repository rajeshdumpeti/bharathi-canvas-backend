from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.feature import Feature
from app.models.project import Project
from app.schemas.feature import FeatureCreate, FeatureOut
from uuid import UUID
from app.schemas.task import TaskOut
from app.models.task import Task

router = APIRouter(prefix="/features", tags=["features"])


@router.post("/", response_model=FeatureOut, status_code=status.HTTP_201_CREATED)
def create_feature(
    body: FeatureCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == body.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_feature = Feature(
        name=body.name,
        details=body.details,
        user_story=body.user_story,
        core_requirements=body.core_requirements,
        acceptance_criteria=body.acceptance_criteria,
        technical_notes=body.technical_notes,
        project_id=body.project_id,
        user_id=current_user.id,
    )

    db.add(new_feature)
    db.commit()
    db.refresh(new_feature)
    return new_feature


@router.get("/project/{project_id}", response_model=list[FeatureOut])
def get_features_for_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(Feature)
        .filter(Feature.project_id == project_id, Feature.user_id == current_user.id)
        .order_by(Feature.created_at.desc())
        .all()
    )


@router.patch("/{feature_id}", response_model=FeatureOut)
def update_feature(
    feature_id: UUID,
    body: FeatureCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    feature = (
        db.query(Feature)
        .filter(Feature.id == feature_id, Feature.user_id == current_user.id)
        .first()
    )
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    for field in [
        "name",
        "details",
        "user_story",
        "core_requirements",
        "acceptance_criteria",
        "technical_notes",
    ]:
        setattr(feature, field, getattr(body, field, getattr(feature, field)))

    db.add(feature)
    db.commit()
    db.refresh(feature)
    return feature


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feature(
    feature_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    feature = (
        db.query(Feature)
        .filter(Feature.id == feature_id, Feature.user_id == current_user.id)
        .first()
    )
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    db.delete(feature)
    db.commit()
    return {"message": "Deleted"}


@router.get("/feature/{feature_id}", response_model=list[TaskOut])
def get_stories_for_feature(
    feature_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    rows = (
        db.query(Task)
        .filter(Task.feature_id == feature_id, Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .all()
    )
    return rows