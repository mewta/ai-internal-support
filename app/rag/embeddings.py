from sentence_transformers import SentenceTransformer

# Small, fast, high-quality model
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    return _model.encode(
        texts,
        show_progress_bar=False,
        normalize_embeddings=True,
    )
