import shutil

from langchain_chroma import Chroma
from langchain_core.documents import Document

from .config import CHROMA_DIR, COLLECTION_NAME
from .embeddings import get_embeddings


def create_vector_store(
    documents: list[Document],
    rebuild: bool = True,
) -> Chroma:
    if rebuild and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    CHROMA_DIR.parent.mkdir(parents=True, exist_ok=True)

    store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
    )

    for start in range(0, len(documents), 64):
        batch = documents[start:start + 64]
        ids = [f"chunk-{start + i}" for i in range(len(batch))]
        store.add_documents(batch, ids=ids)
        print(f"Indexed {min(start + len(batch), len(documents))}/{len(documents)}")

    return store


def get_vector_store() -> Chroma:
    if not CHROMA_DIR.exists():
        raise FileNotFoundError("Vector index not found. Run python ingest.py first.")

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
    )