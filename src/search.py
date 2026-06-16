import os
from dotenv import load_dotenv

from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()


class RAGSearch:

    def __init__(
        self,
        pdf_path=None,
        persist_dir="faiss_store",
        embedding_model="all-MiniLM-L6-v2",
        llm_model="llama-3.3-70b-versatile"
    ):

        self.vectorstore = FaissVectorStore(
            persist_dir,
            embedding_model
        )

        if pdf_path:

            docs = PyPDFLoader(
                pdf_path
            ).load()

            self.vectorstore.build_from_documents(
                docs
            )

        else:

            self.vectorstore.load()

        self.llm = ChatGroq(
            groq_api_key=os.getenv(
                "GROQ_API_KEY"
            ),
            model_name=llm_model
        )

    def search_and_summarize(
        self,
        query: str,
        answer_type="Short Answer",
        top_k: int = 5
    ) -> str:

        results = self.vectorstore.query(
            query,
            top_k=top_k
        )

        texts = [
            r["metadata"].get("text", "")
            for r in results
            if r["metadata"]
        ]

        context = "\n\n".join(texts)

        if not context:
            return "No relevant documents found."

        if answer_type == "Short Answer":

            instruction = """
            Answer in 4-5 sentences only.
            Keep it concise and direct.
            """

        else:

            instruction = """
    Provide a detailed answer using ONLY the information
    available in the context.

    Do not introduce new concepts.

    Structure the answer as:
    - Introduction
    - Main Points
    - Conclusion

    If information is missing, explicitly state that the
    uploaded PDF does not contain further details.
    """

        prompt = f"""
Answer the question using only the provided context.

Question:
{query}

Instruction:
{instruction}

Context:
{context}
"""

        response = self.llm.invoke(prompt)

        return response.content