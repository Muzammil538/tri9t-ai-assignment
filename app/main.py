from fastapi import FastAPI

from app.init_db import init_db

from app.api.browse import router as browse_router
from app.api.selection import router as selection_router

# Initialize database
init_db()

app = FastAPI(
    title="CT-200 Parser API",
    version="1.0"
)

# Register routers
app.include_router(browse_router)
app.include_router(selection_router)


@app.get("/")
def home():
    return {
        "message": "Tri9T AI Assignment API is running"
    }