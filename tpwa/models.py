from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from hashlib import sha256


@dataclass(slots=True)
class Paper:
    paper_id: str
    title: str
    authors: list[str]
    year: int | None
    journal: str
    pdf_path: str

    @classmethod
    def from_pdf_path(cls, pdf_path: Path) -> "Paper":
        stem = pdf_path.stem.replace("_", " ").replace("-", " ").strip()
        return cls(
            paper_id=stable_id("paper", str(pdf_path)),
            title=stem or pdf_path.name,
            authors=[],
            year=infer_year(stem),
            journal="",
            pdf_path=str(pdf_path),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SentenceRecord:
    sentence_id: str
    paper_id: str
    section: str
    raw_sentence: str
    clean_sentence: str
    category: str = ""
    confidence: float = 0.0
    reason: str = ""
    keywords: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    @classmethod
    def create(cls, paper_id: str, raw_sentence: str, clean_sentence: str, section: str = "") -> "SentenceRecord":
        return cls(
            sentence_id=stable_id("sentence", f"{paper_id}:{clean_sentence}"),
            paper_id=paper_id,
            section=section,
            raw_sentence=raw_sentence,
            clean_sentence=clean_sentence,
            keywords=extract_keywords(clean_sentence),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def stable_id(prefix: str, value: str) -> str:
    digest = sha256(value.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{digest}"


def infer_year(text: str) -> int | None:
    import re

    match = re.search(r"(?:19|20)\d{2}", text)
    return int(match.group(0)) if match else None


def extract_keywords(sentence: str, limit: int = 8) -> list[str]:
    import re

    stop_words = {
        "the", "and", "that", "with", "from", "this", "there", "where", "which", "into",
        "have", "been", "are", "for", "our", "can", "will", "may", "not", "such", "these",
    }
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z-]{2,}", sentence)]
    keywords: list[str] = []
    for word in words:
        if word not in stop_words and word not in keywords:
            keywords.append(word)
        if len(keywords) >= limit:
            break
    return keywords
