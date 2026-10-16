import csv
from pathlib import Path

from langchain_core.documents import Document
from pypdf import PdfReader

from .config import CORPUS_DIR


def load_pdf(path: Path) -> list[Document]:
    documents = []
    reader = PdfReader(str(path))

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(path.relative_to(CORPUS_DIR)),
                        "page": page_number,
                        "file_type": "pdf",
                    },
                )
            )
    return documents


def load_csv(path: Path) -> list[Document]:
    documents = []

    with path.open(
        "r", encoding="utf-8-sig", errors="replace", newline=""
    ) as file:
        sample = file.read(4096)
        file.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel

        reader = csv.DictReader(file, dialect=dialect)

        for row_number, row in enumerate(reader, start=2):
            content = " | ".join(
                f"{key}: {value}"
                for key, value in row.items()
                if key and value is not None and str(value).strip()
            )
            if content.strip():
                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": str(path.relative_to(CORPUS_DIR)),
                            "row": row_number,
                            "file_type": "csv",
                        },
                    )
                )

    return documents


def load_excel(path: Path) -> list[Document]:
    import pandas as pd

    documents = []
    sheets = pd.read_excel(path, sheet_name=None, header=None)

    for sheet_name, frame in sheets.items():
        for index, row in frame.iterrows():
            values = [
                str(value).strip()
                for value in row.tolist()
                if pd.notna(value) and str(value).strip()
            ]

            if values:
                documents.append(
                    Document(
                        page_content=" | ".join(values),
                        metadata={
                            "source": str(path.relative_to(CORPUS_DIR)),
                            "sheet": str(sheet_name),
                            "row": int(index) + 1,
                            "file_type": path.suffix.lower().lstrip("."),
                        },
                    )
                )

    return documents


def load_text(path: Path) -> list[Document]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return []

    return [
        Document(
            page_content=text,
            metadata={
                "source": str(path.relative_to(CORPUS_DIR)),
                "file_type": path.suffix.lower().lstrip("."),
            },
        )
    ]


def load_corpus() -> list[Document]:
    if not CORPUS_DIR.exists():
        raise FileNotFoundError(f"Corpus directory not found: {CORPUS_DIR}")

    documents = []

    for path in sorted(CORPUS_DIR.rglob("*")):
        if not path.is_file() or path.name.startswith("~$"):
            continue

        suffix = path.suffix.lower()

        try:
            if suffix == ".pdf":
                documents.extend(load_pdf(path))
            elif suffix == ".csv":
                documents.extend(load_csv(path))
            elif suffix in {".xls", ".xlsx"}:
                documents.extend(load_excel(path))
            elif suffix in {".txt", ".md"}:
                documents.extend(load_text(path))
        except Exception as error:
            print(f"WARNING: Could not read {path.name}: {error}")

    if not documents:
        raise RuntimeError("No text extracted. Check corpus files and dependencies.")

    return documents