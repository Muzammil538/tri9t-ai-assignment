from fastapi import FastAPI

from app.init_db import init_db

init_db()

app = FastAPI(
    title="CT200 Parser API"
)