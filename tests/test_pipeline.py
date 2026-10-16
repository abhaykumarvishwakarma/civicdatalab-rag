from langchain_core.documents import Document

from src.rag_app import pipeline


class FakeRetriever:
    def retrieve(self, question, k=5):
        return [
            Document(
                page_content="The documented scheme allocation is 100.",
                metadata={"source": "example.pdf", "page": 1},
            )
        ]


def test_pipeline_returns_answer(monkeypatch):
    def fake_generate(question, documents):
        return {
            "answer": "The allocation is 100. [S1]",
            "sources": [{"citation": "S1", "source": "example.pdf", "page": 1}],
            "answered": True,
        }

    monkeypatch.setattr(pipeline, "generate_answer", fake_generate)

    result = pipeline.ask("What is the allocation?", retriever=FakeRetriever())

    assert result["answered"] is True
    assert "[S1]" in result["answer"]
    assert result["sources"][0]["source"] == "example.pdf"


def test_empty_question():
    result = pipeline.ask("   ")

    assert result["answered"] is False
    assert result["answer"] == "NOT_ANSWERABLE"