from fastapi import APIRouter
from app.auth.routes import router as auth_router
from . import projects, columns, tasks, features # Board API imports
from . import documents    # Document API


api_router = APIRouter()

# Board API
api_router.include_router(auth_router)
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router)
api_router.include_router(tasks.router)
api_router.include_router(columns.router)
api_router.include_router(features.router)

# Documents API
api_router.include_router(documents.router)


api_router.include_router(tasks.router, prefix="/projects", tags=["tasks"])

