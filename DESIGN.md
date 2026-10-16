# Design Notes

## Architecture

The application follows a retrieval-augmented generation pipeline:

1. **Ingestion:** Load source documents from the corpus.
2. **Chunking:** Split document content into manageable passages and retain source metadata.
3. **Indexing:** Prepare lexical and semantic search representations.
4. **Retrieval:** Retrieve candidate passages using complementary retrieval methods.
5. **Rank fusion:** Combine rankings to select useful evidence.
6. **Generation:** Supply the question and retrieved evidence to the configured language model.
7. **Citation handling:** Return the answer with references to the supporting documents.
8. **Evaluation:** Process a JSONL question set and write one structured result per question.

## Design choices

### Hybrid retrieval

Lexical retrieval can match exact scheme names, years, and numeric terminology. Semantic retrieval can help match queries to passages that express similar meaning with different wording. Combining the rankings can reduce dependence on either method alone.

### Source metadata

Source identifiers and available page, sheet, or row information are retained to make answers easier to verify. Citations are useful only when they point to evidence that actually supports the answer.

### Evidence-grounded generation

The generation prompt instructs the model to answer from retrieved evidence and avoid unsupported claims. The application should preserve units and distinguish missing evidence from a confirmed zero value.

### Batch evaluation

The batch interface supports repeatable evaluation over a fixed question set. JSONL output allows each result to be checked independently for answer quality, citation quality, and answerability.

## Failure cases and trade-offs

- Incorrect extraction or chunk boundaries can separate a value from its unit or heading.
- Lexical search may struggle with Hindi queries when the PDF stores Hindi text in a legacy font encoding.
- Semantic retrieval may return related passages without the exact requested figure.
- A language model can truncate its answer or infer currency conversions not established by the source.
- External inference introduces latency, credentials, network, and rate-limit dependencies.

## Future improvements

- Improve table-aware extraction and preserve table headers with rows.
- Add cross-lingual query handling and stronger Hindi document normalization.
- Add deterministic validation for numeric answers and units.
- Evaluate retrieval separately from generation using labelled examples.
- Add structured logging, retry controls, and clearer failure states.
- Add regression tests for citations, unit preservation, and truncated responses.
