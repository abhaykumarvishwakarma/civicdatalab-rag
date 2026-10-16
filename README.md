# CivicDataLab RAG

A retrieval-augmented generation (RAG) application for answering questions using a corpus of government gender-budget documents.

## Features

- Ingests supported source documents and creates searchable chunks.
- Uses lexical and semantic retrieval to find relevant evidence.
- Combines retrieval rankings to improve candidate selection.
- Generates evidence-grounded answers using an LLM.
- Returns source citations and document metadata.
- Supports single-question queries and batch evaluation.
- Includes an evaluation question set and JSONL answer output.

## Project structure

- `corpus/` — source documents.
- `src/rag_app/` — ingestion, chunking, retrieval, vector-store and generation modules.
- `ingest.py` — ingestion/index preparation entry point.
- `rag.py` — question-answering and batch CLI.
- `questions_eval.jsonl` — evaluation questions.
- `answers.jsonl` — generated evaluation answers, when produced.
- `BUILD_SCOPE.md` — scope and limitations.
- `DESIGN.md` — architecture and design decisions.

## Setup

Use Python 3.11+ if supported by the installed dependencies. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file with the required model-provider credentials and configuration. For example:

```text
GROQ_API_KEY=your_api_key
GROQ_MODEL=your_supported_model_name
```

Use the model configuration expected by `src/rag_app/config.py`. Never commit `.env` or API keys.

## Run

Prepare the document index:

```powershell
python ingest.py
```

Ask a question:

```powershell
python rag.py ask "Delhi Ladli Yojna allocation 2024-25"
```

Run the evaluation set:

```powershell
python rag.py batch --input questions_eval.jsonl --output answers.jsonl --delay 4
```

## Tests

```powershell
python -m compileall src
python -m py_compile ingest.py rag.py
python -m pytest tests -v
```

The test suite previously completed with four passing tests. Re-run it against the final code before submission.

## Output and citations

Answers include source references where available. Depending on the source type, metadata can identify the source document and PDF page, spreadsheet sheet/row, or other available location information. Batch output is JSON Lines: one JSON object per line.

## Limitations

- Retrieval quality depends on document extraction, chunking, and query wording.
- Complex tables and legacy-font Hindi text may not extract cleanly.
- Generated answers can be incomplete or incorrectly interpret units; verify important figures against cited source passages.
- Questions without sufficient evidence should not be answered as established facts.
- Model-provider access, rate limits, and network availability can affect generation.

## Security

Keep API credentials in local environment configuration. Do not commit secrets, virtual environments, caches, or unnecessary generated model files.
