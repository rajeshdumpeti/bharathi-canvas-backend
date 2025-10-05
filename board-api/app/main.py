from fastapi import FastAPI
from app.api.v1.router import api_router

# --- NEW: create tables on startup ---
from app.db.session import engine
from app.db.base import Base
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


app = FastAPI(title="Bharathi Canvas API", version="1.0", debug=True)

def _parse_cors(origins):
    if isinstance(origins, str):
        # supports comma-separated values in .env (e.g., http://localhost:3000,http://localhost:5173)
        return [o.strip() for o in origins.split(",") if o.strip()]
    return origins or []

app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors(getattr(settings, "cors_origins", [])) or [
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Requested-With"],
    expose_headers=["*"],
)

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
