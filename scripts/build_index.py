import faiss
import json
import numpy as np
from ingest import ingest_data
from sentence_transformers import SentenceTransformer

def build_index(data_dir: str, index_path: str):
    # Load data
    records = ingest_data(data_dir)
    texts = [rec["text"] for rec in records]

    # Use a sentence transformer to get embeddings (you can swap this for OpenAI embeddings)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts)

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype="float32"))
    faiss.write_index(index, index_path)

    # Save metadata separately
    with open(index_path + ".meta.json", "w", encoding="utf-8") as f:
        json.dump([rec["metadata"] for rec in records], f, indent=2)

if __name__ == "__main__":
    build_index("data", "models/index.faiss")
