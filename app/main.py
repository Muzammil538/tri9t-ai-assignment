from fastapi import FastAPI

app = FastAPI(
    title="CT-200 Document Parser",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Tri9T AI Assignment API"
    }