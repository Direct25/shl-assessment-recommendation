import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.title("🧠 SHL Assessment Recommendation Engine")

query = st.text_area(
    "Describe the role / hiring requirement",
    placeholder="e.g. Hiring Java developers with good communication skills"
)

top_k = st.slider("Number of recommendations", 3, 10, 5)

if st.button("Recommend Assessments"):
    if not query.strip():
        st.warning("Please enter a query")
    else:
        with st.spinner("Finding best assessments..."):
            response = requests.post(
                API_URL,
                json={"query": query, "top_k": top_k}
            )

            if response.status_code == 200:
                data = response.json()
                st.success("Recommended Assessments")

                for i, rec in enumerate(data["recommendations"], 1):
                    st.markdown(f"### {i}. {rec['title']}")
                    st.markdown(f"🔗 [{rec['url']}]({rec['url']})")
                    st.markdown(f"📊 Score: `{rec['score']:.4f}`")
            else:
                st.error("API error")
