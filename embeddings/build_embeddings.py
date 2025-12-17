import os
import pandas as pd
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Paths
CATALOG_PATH = "data/raw/shl_catalog_raw.csv"
INDEX_PATH = "embeddings/shl_faiss.index"
METADATA_PATH = "embeddings/shl_metadata.pkl"

# Load catalog
print("Loading SHL catalog...")
df = pd.read_csv(CATALOG_PATH)

if "title" not in df.columns or "url" not in df.columns:
    raise ValueError("CSV must contain 'title' and 'url' columns")

print(f"Total assessments: {len(df)}")

# Prepare text & metadata
texts = df["title"].astype(str).tolist()          
metadata = df.to_dict(orient="records")          

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True
)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # cosine similarity (because normalized)
index.add(embeddings)

print(f"FAISS index size: {index.ntotal}")

# Save index & metadata
os.makedirs("embeddings", exist_ok=True)

faiss.write_index(index, INDEX_PATH)

with open(METADATA_PATH, "wb") as f:
    pickle.dump(metadata, f)

print("Embeddings & index saved successfully")
print(f"Index path: {INDEX_PATH}")
print(f"Metadata path: {METADATA_PATH}")
