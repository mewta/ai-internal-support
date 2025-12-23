import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.utils.file_utils import is_allowed_file
from app.core.security import get_current_user
from app.rag.loader import load_text
from app.rag.chunker import chunk_text

UPLOAD_DIR = "data/uploads"

router = APIRouter()

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    role_access: str = "engineering",
    user=Depends(get_current_user),
):
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type",
        )

    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    raw_text = load_text(file_path)
    if not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty document",
        )

    chunks = chunk_text(raw_text)

    chunk_payload = [
        {
            "content": chunk,
            "metadata": {
                "file": file.filename,
                "role": role_access,
            },
        }
        for chunk in chunks
    ]

    return {
        "message": "Document uploaded and processed",
        "chunks_created": len(chunk_payload),
    }
