from langchain_core.documents import Document

from src.rag_app.hybrid_retriever import reciprocal_rank_fusion
from src.rag_app.lexical_retriever import tokenize


def test_tokenize_keeps_year_and_scheme_terms():
    result = tokenize("Delhi Ladli Yojna 2022-23")
    assert "delhi" in result
    assert "ladli" in result
    assert any("2022" in token for token in result)


def test_rrf_combines_rankings():
    shared = Document(
        page_content="Delhi Ladli Yojna",
        metadata={"source": "budget.pdf", "page": 2},
    )
    other = Document(
        page_content="Other scheme",
        metadata={"source": "other.pdf", "page": 1},
    )

    result = reciprocal_rank_fusion([
        [shared, other],
        [shared],
    ])

    assert result[0].page_content == "Delhi Ladli Yojna"
    assert len(result) == 2