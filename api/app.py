import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
FAISS_INDEX_PATH = BASE_DIR / "embeddings" / "shl_faiss.index"
METADATA_PATH = BASE_DIR / "embeddings" / "shl_metadata.pkl"

# Lazy model load
model = None

print("Loading FAISS index...")
index = faiss.read_index(str(FAISS_INDEX_PATH))

print("Loading metadata...")
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

app = FastAPI(title="SHL Assessment Recommendation API")

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/")
def health():
    return {"status": "API is running"}

@app.post("/recommend")
def recommend_assessments(request: RecommendationRequest):
    global model
    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    query_embedding = model.encode(
        [request.query],
        normalize_embeddings=True
    ).astype("float32")

    distances, indices = index.search(query_embedding, request.top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        meta = metadata[idx]
        results.append({
            "title": meta["title"],
            "url": meta["url"],
            "score": float(dist)
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {
        "query": request.query,
        "recommendations": results
    }
