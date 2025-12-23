from fastapi import FastAPI
from app.api import auth, documents

app = FastAPI(title="AI Internal Support Engineer")

# Register routers
app.include_router(auth.router, prefix="/auth")
app.include_router(documents.router, prefix="/documents")

@app.get("/health")
def health():
    return {"status": "ok"}


