# TPWA Specification v1.0

**Project:** Theoretical Physics Writing Assistant  
**Version:** 1.0  
**Status:** Draft / MVP implementation

## 1. Project Vision

TPWA builds an extensible corpus of theoretical physics writing patterns. It analyzes classic papers, extracts useful English academic expressions, classifies sentences by rhetorical function, and stores structured records for later search.

Phase 1 focuses on theoretical physics papers in HEP, GR, QFT, and string theory.

## 2. Phase 1 Scope

Included in the current MVP:

- PDF text extraction from a directory or file.
- Basic body-text cleanup.
- Reference-section removal.
- Heuristic formula and citation cleanup.
- English sentence segmentation.
- Sentence filtering.
- GPT-based rhetorical classification when `OPENAI_API_KEY` is available.
- Deterministic rule-based fallback classification for local testing.
- JSON database storage.
- CLI search and stats.

Excluded from Phase 1:

- OCR.
- Chinese papers.
- Automatic translation.
- Automatic paper rewriting.
- AI paper generation.
- Zotero integration.
- GUI.

## 3. MVP Goal

Read PDFs from a directory, extract body sentences, classify each sentence by writing function, and save the result as structured JSON.

## 4. Categories

- Introduction
- Motivation
- Transition
- Assumption
- Definition
- Derivation
- Interpretation
- Comparison
- Limitation
- Conclusion
- Future Work
- Other

## 5. CLI

```bash
tpwa import papers/
tpwa extract
tpwa classify
tpwa search transition
tpwa stats
```

For local development without installation:

```bash
python -m tpwa.cli import papers/
python -m tpwa.cli extract
python -m tpwa.cli classify
python -m tpwa.cli search transition
python -m tpwa.cli stats
```
