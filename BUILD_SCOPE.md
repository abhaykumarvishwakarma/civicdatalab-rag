# Build Scope

## 1. Objective

Build a retrieval-augmented question-answering application that searches a corpus of government gender-budget documents and responds to questions with supporting source references.

## 2. In scope

- Load and process the provided document corpus.
- Extract text and relevant metadata from supported document types.
- Split extracted content into searchable chunks while retaining source metadata.
- Build lexical and semantic retrieval components.
- Combine candidate rankings to retrieve relevant evidence.
- Generate concise answers grounded in retrieved context.
- Return citations and source metadata with answers.
- Provide a CLI for individual questions and batch evaluation.
- Write batch results as JSONL for downstream inspection.
- Provide tests for core pipeline and retrieval behavior.

## 3. Expected inputs

- Source documents located in `corpus/`.
- Individual questions entered through the CLI.
- Evaluation questions supplied through `questions_eval.jsonl`.
- Model-provider configuration supplied through environment variables where required.

## 4. Expected outputs

- Searchable chunks and associated retrieval artifacts.
- A structured answer for an individual question.
- Source citations and available document-location metadata.
- `answers.jsonl`, containing one JSON record per evaluation question when batch execution completes.

## 5. Out of scope

- A production web interface or public API unless separately required.
- Guaranteed correctness for every question or every document layout.
- Fully reliable OCR or repair of all legacy-font Hindi text.
- Automatic verification of every generated numerical calculation.
- Production-grade authentication, monitoring, scaling, and deployment infrastructure.

## 6. Known limitations and risks

- PDF table extraction may separate labels, column headings, values, and units.
- Legacy-font Hindi text may not be searchable using ordinary Devanagari queries.
- Retrieval can return relevant but insufficient evidence.
- LLM output can be truncated, misread units, or introduce unsupported interpretations.
- External model services may impose rate limits or require internet access.
- Evaluation results depend on the supplied corpus, questions, retrieval configuration, and model availability.

## 7. Acceptance checks

- [ ] Ingestion completes successfully.
- [ ] A single-question query returns structured output.
- [ ] Source references are present when supporting evidence is retrieved.
- [ ] Batch execution produces valid JSONL.
- [ ] The output record count matches the evaluation question count.
- [ ] Automated tests pass.
- [ ] Secrets and local environment files are excluded from version control.
- [ ] Limitations are documented honestly.
