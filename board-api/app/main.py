from fastapi import FastAPI
from app.api.v1.router import api_router

# --- NEW: create tables on startup ---
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="Bharathi Canvas API", version="1.0", debug=True)

@app.on_event("startup")
def create_db_tables() -> None:
    # This will create any missing tables based on your SQLAlchemy models
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
