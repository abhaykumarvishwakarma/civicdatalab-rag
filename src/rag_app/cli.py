import argparse
import json
import time
from pathlib import Path

from .config import ROOT
from .pipeline import ask


def read_jsonl(path: Path) -> list[dict]:
    records = []

    with path.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                print(f"Skipping invalid JSON at line {line_number}: {error}")

    return records


def get_question(record: dict) -> str:
    for field in ("question", "query", "question_text", "prompt", "input"):
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def get_id(record: dict, index: int) -> str:
    for field in ("id", "question_id", "qid", "questionId"):
        if record.get(field) is not None:
            return str(record[field])

    return f"Q{index:02d}"


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_batch(input_file: Path, output_file: Path, delay: float) -> None:
    records = read_jsonl(input_file)
    output = []

    for index, record in enumerate(records, start=1):
        question = get_question(record)
        question_id = get_id(record, index)

        print(f"[{index}/{len(records)}] {question_id}: {question}")

        if question:
            result = ask(question)
        else:
            result = {
                "answer": "NOT_ANSWERABLE",
                "sources": [],
                "answered": False,
            }

        output.append({
            **record,
            "id": question_id,
            "answer": result.get("answer", "NOT_ANSWERABLE"),
            "sources": result.get("sources", []),
            "answered": result.get("answered", False),
        })

        if result.get("error"):
            print(f"ERROR: {result['error']}")

        # Save after every question to avoid losing completed work.
        write_jsonl(output_file, output)
        print(f"  answered={result.get('answered')}")

        if index < len(records):
            time.sleep(delay)

    print(f"Saved {len(output)} records to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="CivicDataLab Hybrid RAG")
    subparsers = parser.add_subparsers(dest="command", required=True)

    question_parser = subparsers.add_parser("ask")
    question_parser.add_argument("question")
    question_parser.add_argument("--top-k", type=int, default=5)

    batch_parser = subparsers.add_parser("batch")
    batch_parser.add_argument("--input", default="questions_eval.jsonl")
    batch_parser.add_argument("--output", default="answers.jsonl")
    batch_parser.add_argument("--delay", type=float, default=3)

    args = parser.parse_args()

    if args.command == "ask":
        print(json.dumps(
            ask(args.question, top_k=args.top_k),
            indent=2,
            ensure_ascii=False,
        ))
    elif args.command == "batch":
        run_batch(
            ROOT / args.input,
            ROOT / args.output,
            args.delay,
        )


if __name__ == "__main__":
    main()