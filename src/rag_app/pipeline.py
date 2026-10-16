
from .generation import generate_answer
from .hybrid_retriever import HybridRetriever
from .chunking import load_chunks
from .config import TOP_K


def ask(
    question: str,
    top_k: int = TOP_K,
    retriever: HybridRetriever | None = None,
) -> dict:
    if not question or not question.strip():
        return {
            "question": question,
            "answer": "NOT_ANSWERABLE",
            "sources": [],
            "answered": False,
        }

    try:
        active_retriever = retriever

        if active_retriever is None:
            chunks = load_chunks()
            active_retriever = HybridRetriever(chunks)

        documents = active_retriever.retrieve(
            question.strip(), k=top_k
        )
        result = generate_answer(question.strip(), documents)

        return {
            "question": question.strip(),
            **result,
        }

    except Exception as error:
        return {
            "question": question.strip(),
            "answer": "",
            "sources": [],
            "answered": False,
            "error": str(error),
        }
