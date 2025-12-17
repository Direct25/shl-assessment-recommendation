import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Paths
CATALOG_PATH = "data/raw/shl_catalog_raw.csv"
FAISS_INDEX_PATH = "embeddings/shl_faiss.index"
METADATA_PATH = "embeddings/shl_metadata.pkl"

def build_embeddings():
    print("Loading SHL catalog...")
    df = pd.read_csv(CATALOG_PATH)

    print("Total assessments:", len(df))

    # Create text for embedding
    if "name" in df.columns:
        texts = df["name"].fillna("") + " " + df.get("description", "").fillna("")
    else:
        texts = df["url"].fillna("")

    texts = texts.tolist()

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print("FAISS index size:", index.ntotal)

    # Save index
    faiss.write_index(index, FAISS_INDEX_PATH)

    # Save metadata
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(df.to_dict(orient="records"), f)

    print("Embeddings & index saved successfully")

if __name__ == "__main__":
    build_embeddings()
