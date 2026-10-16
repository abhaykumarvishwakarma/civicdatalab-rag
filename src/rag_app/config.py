import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

CORPUS_DIR = ROOT / "corpus"
DATA_DIR = ROOT / "data"
CHUNKS_FILE = DATA_DIR / "chunks.jsonl"
CHROMA_DIR = DATA_DIR / "chroma_db"

COLLECTION_NAME = "civicdatalab"
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
TOP_K = int(os.getenv("TOP_K", "5"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))