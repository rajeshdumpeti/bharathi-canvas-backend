from fastapi import APIRouter
from . import projects, columns, tasks
from app.auth.routes import router as auth_router

api_router = APIRouter()

# Register feature routes
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(columns.router, prefix="/projects", tags=["columns"])
api_router.include_router(tasks.router, prefix="/projects", tags=["tasks"])

# Register authentication routes
api_router.include_router(auth_router)
