import json

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNKS_FILE, DATA_DIR



def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "।", ". ", "; ", " ", ""],
    )

    units_by_source = {}

    # Discover units stated in each PDF.
    for document in documents:
        source = str(document.metadata.get("source", ""))
        if (
            "gender_budget" in source.lower()
            and "IN THOUSANDS" in document.page_content.upper()
        ):
            units_by_source[source] = "(IN THOUSANDS)"

    chunks = []

    for document in documents:
        source = str(document.metadata.get("source", ""))
        file_type = document.metadata.get("file_type")

        if file_type in {"csv", "xls", "xlsx"}:
            chunks.append(document)
            continue

        split_docs = splitter.split_documents([document])

        unit = units_by_source.get(source)
        if unit and "gender_budget" in source.lower():
            for chunk in split_docs:
                chunk.page_content = (
                    f"Table unit: {unit}\n"
                    f"{chunk.page_content}"
                )

        chunks.extend(split_docs)

    return chunks


def save_chunks(chunks: list[Document]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with CHUNKS_FILE.open("w", encoding="utf-8") as file:
        for chunk in chunks:
            row = {
                "text": chunk.page_content,
                "metadata": chunk.metadata,
            }
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_chunks() -> list[Document]:
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("Chunks not found. Run python ingest.py first.")

    documents = []

    with CHUNKS_FILE.open("r", encoding="utf-8-sig") as file:
        for line in file:
            if not line.strip():
                continue
            row = json.loads(line)
            documents.append(
                Document(
                    page_content=row["text"],
                    metadata=row.get("metadata", {}),
                )
            )

    return documents