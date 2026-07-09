from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import threading

_embed_model = None
_lock = threading.Lock()

# In-memory FAISS index — holds embeddings of existing grievances for similarity search.
# In production this would be persisted/rebuilt from DB on startup; for now it's built
# incrementally as grievances are added via add_to_index().
_index = None
_id_map = []  # maps FAISS internal position -> grievance_id
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output dimension

def load_embedder():
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embed_model

def _get_index():
    global _index
    if _index is None:
        _index = faiss.IndexFlatIP(EMBEDDING_DIM)  # inner product on normalized vectors = cosine sim
    return _index

def embed_text(text: str) -> np.ndarray:
    model = load_embedder()
    vec = model.encode([text], normalize_embeddings=True)
    return vec.astype("float32")

def add_to_index(grievance_id: int, text: str):
    """Call this after a grievance is saved, to make it searchable for future duplicate checks."""
    with _lock:
        index = _get_index()
        vec = embed_text(text)
        index.add(vec)
        _id_map.append(grievance_id)

def find_duplicates(text: str, threshold: float = 0.75, top_k: int = 5):
    """
    Returns a list of (grievance_id, similarity_score) for existing grievances
    similar enough to be considered potential duplicates.
    """
    with _lock:
        index = _get_index()
        if index.ntotal == 0:
            return []
        vec = embed_text(text)
        scores, positions = index.search(vec, min(top_k, index.ntotal))

    results = []
    for score, pos in zip(scores[0], positions[0]):
        if pos == -1:
            continue
        if score >= threshold:
            results.append({
                "grievance_id": _id_map[pos],
                "similarity": round(float(score), 4)
            })
    return results