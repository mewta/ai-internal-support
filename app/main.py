from fastapi import FastAPI
from app.api import auth

app = FastAPI(title="AI Internal Support Engineer")

app.include_router(auth.router, prefix="/auth")

@app.get("/health")
def health():
    return {"status": "ok"}

