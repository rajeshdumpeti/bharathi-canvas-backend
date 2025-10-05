from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Bharathi Canvas API", version="1.0", debug=True)

# ✅ include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
