import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.utils.file_utils import is_allowed_file
from app.core.security import get_current_user
from app.rag.loader import load_text
from app.rag.chunker import chunk_text
from app.rag.embeddings import embed_texts
from app.rag.vector_store import VectorStore
from app.rag.retriever import retrieve_chunks

UPLOAD_DIR = "data/uploads"

router = APIRouter()


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    role_access: str = "engineering",
    user=Depends(get_current_user),
):
    # 1. Validate file type
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type",
        )

    # 2. Save file to disk
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # 3. Extract text
    raw_text = load_text(file_path)
    if not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty document",
        )

    # 4. Chunk text
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

    # 5. Embed chunks
    texts = [c["content"] for c in chunk_payload]
    metadata = [c["metadata"] for c in chunk_payload]

    embeddings = embed_texts(texts)

    # 6. Store in FAISS
    vector_store = VectorStore(dim=len(embeddings[0]))
    vector_store.load()
    vector_store.add(embeddings, metadata)
    vector_store.save()

    return {
        "message": "Document uploaded and embedded",
        "chunks_created": len(chunk_payload),
    }


# -------- DAY 3 TEST ENDPOINT (TEMPORARY) --------

@router.post("/search")
def search_documents(
    query: str,
    user=Depends(get_current_user),
):
    results = retrieve_chunks(
        query=query,
        user_role=user["role"],
    )

    return {
        "count": len(results),
        "results": results,
    }

