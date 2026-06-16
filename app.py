import os
import streamlit as st
from src.search import RAGSearch

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚"
)

with st.sidebar:

    st.title("🎓 StudyMate AI")

    st.markdown("""
    ### Features

    ✅ PDF Upload

    ✅ Question Answering

    ✅ Short Answer

    ✅ Detailed Answer

    """)

st.title("📚 StudyMate AI")

st.write(
    "Your Personal Exam Preparation Assistant"
)
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    os.makedirs(
        "temp_uploads",
        exist_ok=True
    )

    pdf_path = os.path.join(
        "temp_uploads",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

answer_type = st.selectbox(
    "Answer Type",
    ["Short Answer", "Detailed Answer"]
)
   

query = st.text_area(
    "Ask a question from your notes",
    height=120
)

if st.button("Get Answer"):

    if not uploaded_file:
        st.warning("Please upload a PDF first.")

    elif not query.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching documents..."):

            rag_search = RAGSearch(
                pdf_path=pdf_path
            )

            answer = rag_search.search_and_summarize(
            query=query,
            answer_type=answer_type,
            top_k=7
            )

        st.success("Answer Generated")
        st.write(answer)
st.divider()

st.caption(
    "StudyMate AI • Built using LangChain, FAISS, Groq and Streamlit"
)        
