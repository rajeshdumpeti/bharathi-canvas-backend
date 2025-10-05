from fastapi import APIRouter
from . import projects, columns, tasks

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(columns.router, prefix="/projects", tags=["columns"])
api_router.include_router(tasks.router, prefix="/projects", tags=["tasks"])

