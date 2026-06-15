import streamlit as st
from src.search import RAGSearch

st.set_page_config(
    page_title="RAG PDF Question Answering",
    page_icon="📚"
)

st.title("📚 RAG PDF Question Answering System")

st.write(
    "Ask questions from your PDF documents using Retrieval-Augmented Generation (RAG)."
)

query = st.text_input(
    "Enter your question:"
)

if st.button("Get Answer"):

    if query.strip():

        with st.spinner("Searching documents..."):

            rag_search = RAGSearch()

            answer = rag_search.search_and_summarize(
                query,
                top_k=3
            )

        st.success("Answer Generated")
        st.write(answer)

    else:
        st.warning("Please enter a question.")