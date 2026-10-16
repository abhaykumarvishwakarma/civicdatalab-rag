from src.rag_app.ingestion import load_corpus
from src.rag_app.chunking import chunk_documents, save_chunks
from src.rag_app.vector_store import create_vector_store


def main():
    print("Loading source documents...")
    documents = load_corpus()
    print(f"Extracted {len(documents)} source units.")

    print("Creating chunks...")
    chunks = chunk_documents(documents)
    save_chunks(chunks)
    print(f"Saved {len(chunks)} chunks.")

    print("Building local Chroma index...")
    create_vector_store(chunks, rebuild=True)
    print("Ingestion complete.")


if __name__ == "__main__":
    main()