from __future__ import annotations

import logging
import re
from pathlib import Path

from .models import Paper, SentenceRecord

LOGGER = logging.getLogger(__name__)


def read_pdf_text(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pypdf is required for PDF extraction. Install requirements.txt.") from exc

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            pages.append(page.extract_text() or "")
        except Exception as exc:  # pragma: no cover
            LOGGER.warning("Failed to extract page %s from %s: %s", page_number, pdf_path, exc)
    return "\n".join(pages)


def remove_references(text: str) -> str:
    marker = re.search(r"(?im)^\s*(references|bibliography)\s*$", text)
    return text[: marker.start()] if marker else text


def clean_text(text: str) -> str:
    text = remove_references(text)
    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines: list[str] = []
    for line in lines:
        if not line:
            cleaned_lines.append("")
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if re.fullmatch(r"[-–—]?\s*\d+\s*[-–—]?", line):
            continue
        if is_likely_header_footer(line):
            continue
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)
    text = re.sub(r"\[[0-9,\-\s]+\]", "", text)
    text = re.sub(r"\(\s*see\s+Refs?\.\s*\[[^)]*\]\s*\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:Eq|Eqs|Equation|Fig|Figs)\.?(?:\s*\(?\d+(?:\.\d+)*\)?)", "", text)
    text = remove_formula_like_fragments(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_likely_header_footer(line: str) -> bool:
    if len(line) > 120:
        return False
    lower = line.lower()
    return any(token in lower for token in ("arxiv:", "prepared for", "submitted to"))


def remove_formula_like_fragments(text: str) -> str:
    text = re.sub(r"\$[^$]+\$", " ", text)
    text = re.sub(r"\\\[[\s\S]*?\\\]", " ", text)
    text = re.sub(r"\\\([\s\S]*?\\\)", " ", text)
    text = re.sub(r"\b[A-Za-z]\s*=\s*[^,.!?;:]{1,80}", " ", text)
    text = re.sub(r"[∫∑√≤≥≠≈∞∂]+", " ", text)
    return text


def split_sentences(text: str) -> list[str]:
    protected = protect_abbreviations(text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", protected)
    return [restore_abbreviations(part).strip() for part in parts if part.strip()]


def protect_abbreviations(text: str) -> str:
    abbreviations = ["e.g.", "i.e.", "cf.", "Ref.", "Refs.", "Eq.", "Eqs.", "Fig.", "Figs.", "Dr.", "Prof."]
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace(".", "<DOT>"))
    return text


def restore_abbreviations(text: str) -> str:
    return text.replace("<DOT>", ".")


def is_valid_sentence(sentence: str) -> bool:
    if len(sentence) < 20:
        return False
    if len(sentence.split()) < 4:
        return False
    if formula_density(sentence) > 0.28:
        return False
    if sentence.isupper() and len(sentence) < 100:
        return False
    if not re.search(r"[A-Za-z]{3,}", sentence):
        return False
    return True


def formula_density(sentence: str) -> float:
    if not sentence:
        return 1.0
    formula_chars = sum(1 for char in sentence if char in "=+-*/^_{}[]()<>∫∑√≤≥≠≈∞∂")
    return formula_chars / len(sentence)


def extract_sentences_for_paper(paper: Paper) -> list[SentenceRecord]:
    raw_text = read_pdf_text(Path(paper.pdf_path))
    clean = clean_text(raw_text)
    records: list[SentenceRecord] = []
    for sentence in split_sentences(clean):
        normalized = re.sub(r"\s+", " ", sentence).strip()
        if is_valid_sentence(normalized):
            records.append(SentenceRecord.create(paper.paper_id, sentence, normalized))
    return records
