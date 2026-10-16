from src.rag_app.lexical_retriever import BM25Retriever
from src.rag_app.vector_store import get_vector_store


def _rrf_scored(rankings, c=60):
    """Combine ranked document lists using Reciprocal Rank Fusion."""
    ranked = {}

    for docs in rankings:
        for rank, doc in enumerate(docs, start=1):
            key = (
                doc.metadata.get("source"),
                doc.metadata.get("page"),
                doc.metadata.get("row"),
                doc.page_content[:150],
            )
            if key not in ranked:
                ranked[key] = [doc, 0.0]
            ranked[key][1] += 1.0 / (c + rank)

    return sorted(ranked.values(), key=lambda item: item[1], reverse=True)


def reciprocal_rank_fusion(rankings, c=60):
    """Return unique documents ordered by their combined RRF score."""
    return [doc for doc, _ in _rrf_scored(rankings, c)]


class HybridRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.lexical = BM25Retriever(documents)
        self.vector_store = get_vector_store()

    def retrieve(self, query: str, k: int = 5):
        fetch_k = max(k * 10, 50)
        lexical_docs = self.lexical.retrieve(query, k=fetch_k)
        semantic_docs = self.vector_store.similarity_search(
            query, k=fetch_k
        )

        ranked = _rrf_scored([lexical_docs, semantic_docs])
        q = query.lower()
        year = next(
            (str(y) for y in range(2000, 2031) if str(y) in q),
            None,
        )

        for item in ranked:
            doc = item[0]
            content = doc.page_content.lower()
            source = str(doc.metadata.get("source", "")).lower()

            if "ladli" in q and "ladli" in content:
                item[1] += 0.05

            if year:
                next_year = str(int(year) + 1)
                patterns = (
                    f"{year}-{next_year}",
                    f"{year}-{next_year[-2:]}",
                    f"{year[-2:]}-{next_year[-2:]}",
                )
                if any(pattern in source for pattern in patterns):
                    item[1] += 0.03

        ranked.sort(key=lambda item: item[1], reverse=True)
        return [doc for doc, _ in ranked[:k]]
