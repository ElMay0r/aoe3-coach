import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

def load_index(index_path: str):
    index = faiss.read_index(index_path)
    with open(index_path + ".meta.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def query_index(index, metadata, query: str, top_k: int = 5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    q_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(q_embedding, top_k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        result = metadata[idx].copy()
        result["score"] = float(dist)
        results.append(result)
    return results

if __name__ == "__main__":
    index, meta = load_index("models/index.faiss")
    question = "How do I counter French grenadier rushes?"
    results = query_index(index, meta, question)
    for r in results:
        print(r)
