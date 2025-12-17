import requests
import json

API_URL = "http://127.0.0.1:8000/recommend"

test_queries = [
    "Hiring Java developers with strong communication skills",
    "Content writer required, expert in English and SEO",
    "Entry-level sales role for new graduates",
    "Technical lead with system design experience",
    "Administrative assistant with attention to detail"
]

TOP_K = 5

def run_tests():
    print("Running validation tests against SHL Recommendation API...\n")

    for i, query in enumerate(test_queries, start=1):
        payload = {
            "query": query,
            "top_k": TOP_K
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            print(f"[ERROR] Query {i} failed: {query}")
            print("Status code:", response.status_code)
            continue

        data = response.json()
        recommendations = data.get("recommendations", [])

        print(f"Test {i}: {query}")
        print(f"Top {len(recommendations)} recommendations:")

        for rank, rec in enumerate(recommendations, start=1):
            print(f"  {rank}. {rec['title']} (score={rec['score']:.4f})")

        print("-" * 60)

if __name__ == "__main__":
    run_tests()
