from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .models import Paper, SentenceRecord


class JsonStore:
    def __init__(self, database_dir: Path = Path("database")) -> None:
        self.database_dir = database_dir
        self.database_dir.mkdir(parents=True, exist_ok=True)
        self.papers_path = self.database_dir / "papers.json"
        self.sentences_path = self.database_dir / "sentences.json"

    def load_papers(self) -> list[dict[str, Any]]:
        return self._load_list(self.papers_path)

    def load_sentences(self) -> list[dict[str, Any]]:
        return self._load_list(self.sentences_path)

    def save_papers(self, papers: Iterable[Paper | dict[str, Any]]) -> None:
        merged = {item["paper_id"]: item for item in self.load_papers()}
        for paper in papers:
            data = paper.to_dict() if isinstance(paper, Paper) else paper
            merged[data["paper_id"]] = data
        self._save_list(self.papers_path, merged.values())

    def save_sentences(self, sentences: Iterable[SentenceRecord | dict[str, Any]]) -> None:
        merged = {item["sentence_id"]: item for item in self.load_sentences()}
        for sentence in sentences:
            data = sentence.to_dict() if isinstance(sentence, SentenceRecord) else sentence
            merged[data["sentence_id"]] = data
        self._save_list(self.sentences_path, merged.values())

    def replace_sentences_for_papers(self, paper_ids: set[str], sentences: Iterable[SentenceRecord]) -> None:
        existing = [s for s in self.load_sentences() if s.get("paper_id") not in paper_ids]
        existing.extend(sentence.to_dict() for sentence in sentences)
        self._save_list(self.sentences_path, existing)

    def _load_list(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError(f"Expected a JSON list in {path}")
        return data

    def _save_list(self, path: Path, rows: Iterable[dict[str, Any]]) -> None:
        with path.open("w", encoding="utf-8") as file:
            json.dump(list(rows), file, ensure_ascii=False, indent=2)
            file.write("\n")
