from fastapi import APIRouter
from . import projects, columns, tasks
from app.auth.routes import router as auth_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router)
api_router.include_router(columns.router, prefix="/projects", tags=["columns"])
api_router.include_router(tasks.router, prefix="/projects", tags=["tasks"])

