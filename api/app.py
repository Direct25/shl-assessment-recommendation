from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
FAISS_INDEX_PATH = BASE_DIR / "embeddings" / "shl_faiss.index"
METADATA_PATH = BASE_DIR / "embeddings" / "shl_metadata.pkl"

# Load model and index at startup
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index(str(FAISS_INDEX_PATH))  # ✅ FIX HERE

print("Loading metadata...")
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

# FastAPI app
app = FastAPI(title="SHL Assessment Recommendation API")

# Request schema
class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5

# Health check endpoint
@app.get("/")
def health():
    return {"status": "API is running"}

# Recommendation endpoint
@app.post("/recommend")
def recommend_assessments(request: RecommendationRequest):
    query_embedding = model.encode([request.query]).astype("float32")

    distances, indices = index.search(query_embedding, request.top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        meta = metadata[idx]
        results.append({
            "title": meta["title"],
            "url": meta["url"],
            "score": float(dist)
        })

    results = sorted(results, key=lambda x: x["score"])

    return {
        "query": request.query,
        "recommendations": results
    }
