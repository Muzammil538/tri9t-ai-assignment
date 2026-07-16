from fastapi import FastAPI

from app.database import Base, engine

from app.models import Document, Node


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CT-200 Parser API"
)


@app.get("/")
def home():
    return {
        "message": "API Running"
    }