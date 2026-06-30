# TPWA — Theoretical Physics Writing Assistant

TPWA is a small, extensible Python tool for building a corpus of useful English writing patterns from theoretical physics papers. It extracts sentences from PDF papers, removes common non-body text, classifies each sentence by rhetorical function, and stores the result as JSON for search.

The first version is intentionally an MVP: it is designed to run locally, be easy to test, and support later expansion to SQLite, arXiv, Zotero, GUI, and vector search.

## What it does

- Imports PDFs from a file or directory.
- Extracts text from PDF pages.
- Removes likely references, citations, equation references, and formula-heavy fragments.
- Splits text into English sentences.
- Filters very short, title-like, or formula-like lines.
- Classifies sentences into academic writing functions.
- Saves everything as JSON.
- Searches by keyword, paper, author, or category.

## Categories

`Introduction`, `Motivation`, `Transition`, `Assumption`, `Definition`, `Derivation`, `Interpretation`, `Comparison`, `Limitation`, `Conclusion`, `Future Work`, and `Other`.

## Install

Python 3.12+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Optional GPT classification

Set `OPENAI_API_KEY` to use GPT classification:

```bash
export OPENAI_API_KEY="your_api_key"
```

If no API key is configured, TPWA uses a deterministic rule-based classifier. This keeps tests and local demos runnable without network access.

## Usage

Import PDFs:

```bash
python -m tpwa.cli import papers/
```

Extract and clean sentences:

```bash
python -m tpwa.cli extract
```

Classify sentences:

```bash
python -m tpwa.cli classify
```

Search:

```bash
python -m tpwa.cli search transition
python -m tpwa.cli search "It follows that"
python -m tpwa.cli search --category Transition
python -m tpwa.cli search --author Maldacena
```

Stats:

```bash
python -m tpwa.cli stats
```

## Data files

By default TPWA writes JSON files under `database/`:

- `papers.json`
- `sentences.json`

## Suggested project workflow

1. Put PDFs in `papers/`.
2. Run `import`.
3. Run `extract`.
4. Run `classify`.
5. Search and inspect the JSON output.
6. Add more papers over time without rebuilding from scratch.
