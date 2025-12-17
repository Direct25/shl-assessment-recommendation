# from fastapi import FastAPI
# from pydantic import BaseModel
# import faiss
# import pickle
# import numpy as np
# from sentence_transformers import SentenceTransformer

# # Paths
# FAISS_INDEX_PATH = "embeddings/shl_faiss.index"
# METADATA_PATH = "embeddings/shl_metadata.pkl"

# # Load model and index at startup
# print("Loading embedding model...")
# model = SentenceTransformer("all-MiniLM-L6-v2")

# print("Loading FAISS index...")
# index = faiss.read_index(FAISS_INDEX_PATH)

# print("Loading metadata...")
# with open(METADATA_PATH, "rb") as f:
#     metadata = pickle.load(f)

# app = FastAPI(title="SHL Assessment Recommendation API")

# class RecommendationRequest(BaseModel):
#     query: str
#     top_k: int = 5

# @app.post("/recommend")
# def recommend_assessments(request: RecommendationRequest):
#     # Encode query
#     query_embedding = model.encode([request.query]).astype("float32")

#     # Search FAISS
#     distances, indices = index.search(query_embedding, request.top_k)

#     results = []
#     for idx, dist in zip(indices[0], distances[0]):
#         item = metadata[idx]
#         item["score"] = float(dist)
#         results.append(item)

#     return {
#         "query": request.query,
#         "recommendations": results
#     }

from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
FAISS_INDEX_PATH = "embeddings/shl_faiss.index"
METADATA_PATH = "embeddings/shl_metadata.pkl"

# Load model and index at startup
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index(FAISS_INDEX_PATH)

print("Loading metadata...")
with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)

app = FastAPI(title="SHL Assessment Recommendation API")

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/recommend")
def recommend_assessments(request: RecommendationRequest):
    # Encode query
    query_embedding = model.encode([request.query]).astype("float32")

    # Search FAISS
    distances, indices = index.search(query_embedding, request.top_k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        meta = metadata[idx]
        results.append({
            "title": meta["title"],
            "url": meta["url"],
            "score": float(dist)
        })

    return {
        "query": request.query,
        "recommendations": results
    }
