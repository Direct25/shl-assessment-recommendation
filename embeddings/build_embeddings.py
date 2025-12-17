# import pandas as pd
# import numpy as np
# import faiss
# import pickle
# from sentence_transformers import SentenceTransformer

# # Paths
# CATALOG_PATH = "data/raw/shl_catalog_raw.csv"
# FAISS_INDEX_PATH = "embeddings/shl_faiss.index"
# METADATA_PATH = "embeddings/shl_metadata.pkl"

# def build_embeddings():
#     print("Loading SHL catalog...")
#     df = pd.read_csv(CATALOG_PATH)

#     print("Total assessments:", len(df))

#     # Create text for embedding
#     if "name" in df.columns:
#         texts = df["name"].fillna("") + " " + df.get("description", "").fillna("")
#     else:
#         texts = df["url"].fillna("")

#     texts = texts.tolist()

#     print("Loading embedding model...")
#     model = SentenceTransformer("all-MiniLM-L6-v2")

#     print("Generating embeddings...")
#     embeddings = model.encode(texts, show_progress_bar=True)

#     embeddings = np.array(embeddings).astype("float32")

#     # Create FAISS index
#     dim = embeddings.shape[1]
#     index = faiss.IndexFlatL2(dim)
#     index.add(embeddings)

#     print("FAISS index size:", index.ntotal)

#     # Save index
#     faiss.write_index(index, FAISS_INDEX_PATH)

#     # Save metadata
#     with open(METADATA_PATH, "wb") as f:
#         pickle.dump(df.to_dict(orient="records"), f)

#     print("Embeddings & index saved successfully")

# if __name__ == "__main__":
#     build_embeddings()


import os
import pandas as pd
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# -------------------------------
# Paths
# -------------------------------
CATALOG_PATH = "data/raw/shl_catalog_raw.csv"
INDEX_PATH = "embeddings/shl_faiss.index"
METADATA_PATH = "embeddings/shl_metadata.pkl"

# -------------------------------
# Load catalog
# -------------------------------
print("Loading SHL catalog...")
df = pd.read_csv(CATALOG_PATH)

if "title" not in df.columns or "url" not in df.columns:
    raise ValueError("CSV must contain 'title' and 'url' columns")

print(f"Total assessments: {len(df)}")

# -------------------------------
# Prepare text & metadata
# -------------------------------
texts = df["title"].astype(str).tolist()          # ✅ embed hiring intent text
metadata = df.to_dict(orient="records")           # ✅ keep title + url

# -------------------------------
# Load embedding model
# -------------------------------
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -------------------------------
# Generate embeddings
# -------------------------------
print("Generating embeddings...")
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True
)

# -------------------------------
# Build FAISS index
# -------------------------------
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # cosine similarity (because normalized)
index.add(embeddings)

print(f"FAISS index size: {index.ntotal}")

# -------------------------------
# Save index & metadata
# -------------------------------
os.makedirs("embeddings", exist_ok=True)

faiss.write_index(index, INDEX_PATH)

with open(METADATA_PATH, "wb") as f:
    pickle.dump(metadata, f)

print("Embeddings & index saved successfully")
print(f"Index path: {INDEX_PATH}")
print(f"Metadata path: {METADATA_PATH}")
