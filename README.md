SHL Assessment Recommendation Engine

An AI-powered recommendation system that suggests relevant SHL assessments based on natural language hiring requirements, using semantic embeddings and vector similarity search.

This project was built as part of the SHL AI Intern – Generative AI Assignment and demonstrates an end-to-end recommender pipeline including data preparation, embeddings, similarity search, API serving, and a simple frontend UI.

📌 Problem Statement

Hiring managers often describe role requirements in free-form natural language (e.g., “Hiring Java developers with strong communication skills”).
The goal of this system is to map such descriptions to the most relevant SHL assessments in an automated, scalable, and explainable way.

🏗️ System Architecture
SHL Assessment Catalog (CSV)
        ↓
Text Cleaning & Preparation
        ↓
Sentence Embeddings (MiniLM)
        ↓
FAISS Vector Index
        ↓
FastAPI Recommendation Service
        ↓
Streamlit Web UI

🧠 Technical Approach
🔹 Text Representation

Each SHL assessment is represented using its title (instead of only URLs) to improve semantic understanding.

Embeddings are generated using:

sentence-transformers/all-MiniLM-L6-v2

🔹 Vector Search

FAISS is used for efficient similarity search over embedding vectors.

Lower cosine distance indicates higher relevance.

🔹 Recommendation Logic

User query is embedded and compared against all assessment embeddings.

Top-K most similar assessments are returned.

Results are sorted by relevance score for better interpretability.

📂 Project Structure
shl-assessment-recommendation/
│
├── api/                # FastAPI backend
│   └── app.py
│
├── data/
│   ├── raw/             # SHL catalog CSV
│   ├── processed/
│   └── evaluation/
│
├── embeddings/          # FAISS index & embedding scripts
│   ├── build_embeddings.py
│   ├── shl_faiss.index
│   └── shl_metadata.pkl
│
├── frontend/            # Streamlit UI
│   └── app.py
│
├── scraping/            # Dataset conversion utilities
│
├── requirements.txt
└── README.md

🚀 How to Run the Project
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Build Embeddings
python embeddings/build_embeddings.py

3️⃣ Start the API
python -m uvicorn api.app:app --reload


API Docs: http://127.0.0.1:8000/docs

Health Check: http://127.0.0.1:8000/

4️⃣ Launch Frontend
python -m streamlit run frontend/app.py


UI: http://localhost:8501

## 📸 Application Screenshots

### Streamlit User Interface – Input
![Streamlit Input UI](docs/screenshots/ui_input.jpeg)

### Streamlit User Interface – Recommendations
![Streamlit Results](docs/screenshots/ui_results.jpeg)
![Streamlit Results](docs/screenshots/ui_results_2.jpeg)

### API Health Check
![Health Check](docs/screenshots/health_check.jpeg)

### FastAPI Swagger Documentation
![Swagger API](docs/screenshots/api_swagger_recommend.jpeg)
![Swagger API](docs/screenshots/api_swagger_response.jpeg)

🔌 API Example

Endpoint: POST /recommend

Request Body:

{
  "query": "Hiring Java developers with strong communication skills",
  "top_k": 5
}


Response:

{
  "query": "...",
  "recommendations": [
    {
      "title": "Core Java – Advanced Level",
      "url": "https://www.shl.com/...",
      "score": 0.42
    }
  ]
}

🧪 Validation & Testing

The recommendation system was validated using multiple realistic hiring scenarios
(e.g., software engineering, content writing, sales, and administrative roles).

A dedicated script (evaluation/test_queries.py) was used to verify:

Semantic relevance of recommendations

Ranking behavior across different domains

API stability and response consistency

Manual testing was also performed via:

Swagger UI (/docs)

Streamlit frontend with varied queries and recommendation sizes

📊 Evaluation Methodology (Planned)

The recommended evaluation metric for this task is Mean Recall@K, using the provided labeled training dataset.

Due to time constraints, a full Recall@K computation pipeline was not finalized.
However, the system is designed to support this evaluation by:

Separating catalog data from queries

Supporting batch evaluation

Returning ranked recommendations suitable for Recall@K analysis

⚠️ Known Limitations & Assumptions

The current catalog is a subset of SHL assessments used to validate correctness and architecture.

Full-scale crawling (377+ assessments) is supported by the pipeline but was limited for this implementation.

Recommendation balancing across multiple assessment categories is handled implicitly via semantic similarity rather than explicit rule-based weighting.

These trade-offs were made to prioritize robust system design, clarity, and correctness.

✅ Key Strengths

Clean, modular architecture

Strong use of semantic embeddings (not keyword matching)

Scalable FAISS-based retrieval

Fully working API + frontend

Clear separation of concerns

Transparent assumptions and limitations

🔮 Future Improvements

Full SHL catalog ingestion (377+ assessments)

Automated Recall@K evaluation

Explicit balancing across assessment types

Caching and performance optimization

Deployment using Docker / cloud services

📌 Conclusion

This project demonstrates a production-ready foundation for an AI-driven assessment recommendation system.
The focus was on sound engineering principles, explainability, and extensibility, with clear paths for further enhancement.
