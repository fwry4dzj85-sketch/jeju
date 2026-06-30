from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .classify import GPTClassifier
from .extract import extract_sentences_for_paper
from .models import Paper
from .storage import JsonStore


def setup_logging() -> None:
    Path("logs").mkdir(exist_ok=True)
    logging.basicConfig(
        filename="logs/tpwa.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def import_papers(path: Path, store: JsonStore) -> None:
    pdfs = [path] if path.is_file() and path.suffix.lower() == ".pdf" else sorted(path.glob("*.pdf"))
    papers = [Paper.from_pdf_path(pdf) for pdf in pdfs]
    store.save_papers(papers)
    print(f"Imported {len(papers)} paper(s).")


def extract_command(store: JsonStore) -> None:
    papers = [Paper(**paper) for paper in store.load_papers()]
    all_sentences = []
    failed = 0
    for paper in papers:
        try:
            sentences = extract_sentences_for_paper(paper)
            all_sentences.extend(sentences)
            print(f"Extracted {len(sentences)} sentence(s) from {paper.title}.")
        except Exception as exc:
            failed += 1
            logging.exception("Failed to extract %s", paper.pdf_path)
            print(f"Skipped {paper.pdf_path}: {exc}")
    store.replace_sentences_for_papers({paper.paper_id for paper in papers}, all_sentences)
    print(f"Saved {len(all_sentences)} sentence(s); failed paper(s): {failed}.")


def classify_command(store: JsonStore, model: str) -> None:
    classifier = GPTClassifier(model=model)
    rows = store.load_sentences()
    for row in rows:
        if row.get("category"):
            continue
        result = classifier.classify(row["clean_sentence"])
        row.update(result.as_dict())
    store.save_sentences(rows)
    print(f"Classified {len(rows)} sentence record(s).")


def search_command(store: JsonStore, query: str | None, category: str | None, author: str | None, paper: str | None) -> None:
    papers = {row["paper_id"]: row for row in store.load_papers()}
    rows = store.load_sentences()
    results = []
    for row in rows:
        paper_row = papers.get(row.get("paper_id"), {})
        if query and query.lower() not in row.get("clean_sentence", "").lower():
            continue
        if category and category.lower() != row.get("category", "").lower():
            continue
        if paper and paper.lower() not in paper_row.get("title", "").lower():
            continue
        if author:
            authors = " ".join(paper_row.get("authors", []))
            if author.lower() not in authors.lower():
                continue
        results.append((row, paper_row))

    for row, paper_row in results[:50]:
        print(f"[{row.get('category') or 'Unclassified'}] {row.get('clean_sentence')}")
        print(f"  paper: {paper_row.get('title', row.get('paper_id'))}")
    print(f"Found {len(results)} result(s).")


def stats_command(store: JsonStore) -> None:
    papers = store.load_papers()
    sentences = store.load_sentences()
    counts: dict[str, int] = {}
    for sentence in sentences:
        category = sentence.get("category") or "Unclassified"
        counts[category] = counts.get(category, 0) + 1
    print(f"Papers: {len(papers)}")
    print(f"Sentences: {len(sentences)}")
    for category, count in sorted(counts.items()):
        print(f"{category}: {count}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tpwa", description="Theoretical Physics Writing Assistant")
    parser.add_argument("--database", default="database", help="Database directory for JSON files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser("import", help="Import PDF metadata from a file or directory.")
    import_parser.add_argument("path", type=Path)

    subparsers.add_parser("extract", help="Extract cleaned sentence records from imported PDFs.")

    classify_parser = subparsers.add_parser("classify", help="Classify extracted sentences.")
    classify_parser.add_argument("--model", default="gpt-4.1-mini")

    search_parser = subparsers.add_parser("search", help="Search classified sentence records.")
    search_parser.add_argument("query", nargs="?")
    search_parser.add_argument("--category")
    search_parser.add_argument("--author")
    search_parser.add_argument("--paper")

    subparsers.add_parser("stats", help="Show corpus statistics.")
    return parser


def main() -> None:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args()
    store = JsonStore(Path(args.database))

    if args.command == "import":
        import_papers(args.path, store)
    elif args.command == "extract":
        extract_command(store)
    elif args.command == "classify":
        classify_command(store, args.model)
    elif args.command == "search":
        search_command(store, args.query, args.category, args.author, args.paper)
    elif args.command == "stats":
        stats_command(store)


if __name__ == "__main__":
    main()
