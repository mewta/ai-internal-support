from app.rag.embeddings import embed_texts
from app.rag.vector_store import VectorStore

VECTOR_DIM = 384  # all-MiniLM-L6-v2 output size


def retrieve_chunks(
    query: str,
    user_role: str,
    top_k: int = 5,
):
    # 1. Load FAISS index fresh
    store = VectorStore(dim=VECTOR_DIM)
    loaded = store.load()

    if not loaded:
        return []

    # 2. Embed query
    query_embedding = embed_texts([query])

    # 3. Search (over-fetch before filtering)
    candidates = store.search(query_embedding, top_k=top_k * 2)

    # 4. Role-based filtering
    allowed = []
    for chunk in candidates:
        role = chunk.get("role")
        if role == "admin" or role == user_role:
            allowed.append(chunk)

    return allowed[:top_k]
