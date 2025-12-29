import faiss
import pickle
from pathlib import Path

FAISS_DIR = Path("data/faiss")
INDEX_PATH = FAISS_DIR / "index.bin"
META_PATH = FAISS_DIR / "metadata.pkl"


class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: list[dict] = []

    def add(self, embeddings, metadata):
        self.index.add(embeddings)
        self.metadata.extend(metadata)

    def save(self):
        FAISS_DIR.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(INDEX_PATH))
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        if not INDEX_PATH.exists():
            return False

        self.index = faiss.read_index(str(INDEX_PATH))
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)
        return True

    def search(self, query_embedding, top_k: int = 5):
        scores, indices = self.index.search(query_embedding, top_k)
        results = []

        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])

        return results
