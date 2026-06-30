from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any

CATEGORIES = [
    "Introduction", "Motivation", "Transition", "Assumption", "Definition", "Derivation",
    "Interpretation", "Comparison", "Limitation", "Conclusion", "Future Work", "Other",
]


@dataclass(slots=True)
class Classification:
    category: str
    confidence: float
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {"category": self.category, "confidence": self.confidence, "reason": self.reason}


class RuleBasedClassifier:
    def classify(self, sentence: str) -> Classification:
        lower = sentence.lower()
        if re.search(r"\b(we now|turn to|next|finally|let us now|in the following)\b", lower):
            return Classification("Transition", 0.82, "The sentence signals a shift to a new part of the argument.")
        if re.search(r"\b(it follows|therefore|hence|thus|consequently|we find|one obtains)\b", lower):
            return Classification("Derivation", 0.84, "The sentence presents a logical consequence or derived result.")
        if re.search(r"\b(we assume|assuming|suppose|let us take|under the assumption)\b", lower):
            return Classification("Assumption", 0.82, "The sentence introduces an assumption.")
        if re.search(r"\b(is defined as|we define|definition|called|denote)\b", lower):
            return Classification("Definition", 0.82, "The sentence defines terminology or notation.")
        if re.search(r"\b(in this paper|we study|we investigate|we consider|we show)\b", lower):
            return Classification("Introduction", 0.78, "The sentence introduces the paper's topic or contribution.")
        if re.search(r"\b(motivat|important|interest|central question|aim|goal)\b", lower):
            return Classification("Motivation", 0.76, "The sentence motivates the problem or explains its importance.")
        if re.search(r"\b(on the other hand|whereas|unlike|compared with|in contrast)\b", lower):
            return Classification("Comparison", 0.8, "The sentence compares or contrasts ideas.")
        if re.search(r"\b(however|nevertheless|limitation|only valid|breaks down|fails)\b", lower):
            return Classification("Limitation", 0.78, "The sentence describes a limitation or caveat.")
        if re.search(r"\b(this means|physically|interpret|suggests|indicates)\b", lower):
            return Classification("Interpretation", 0.76, "The sentence interprets the meaning of a result.")
        if re.search(r"\b(in conclusion|to summarize|we have shown|we conclude)\b", lower):
            return Classification("Conclusion", 0.86, "The sentence summarizes or concludes the discussion.")
        if re.search(r"\b(future work|it would be interesting|remain|open question)\b", lower):
            return Classification("Future Work", 0.84, "The sentence points to future work or open questions.")
        return Classification("Other", 0.5, "No high-confidence rhetorical marker was detected.")


class GPTClassifier:
    def __init__(self, model: str = "gpt-4.1-mini", max_retries: int = 3) -> None:
        self.model = model
        self.max_retries = max_retries

    def classify(self, sentence: str) -> Classification:
        if not os.getenv("OPENAI_API_KEY"):
            return RuleBasedClassifier().classify(sentence)

        from openai import OpenAI

        client = OpenAI()
        prompt = build_user_prompt(sentence)
        last_error: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = client.responses.create(
                    model=self.model,
                    input=[
                        {"role": "system", "content": "You are an experienced editor of theoretical physics journals. Classify academic-paper sentences by rhetorical function. Return JSON only."},
                        {"role": "user", "content": prompt},
                    ],
                )
                return parse_classification(response.output_text)
            except Exception as exc:  # pragma: no cover
                last_error = exc
                time.sleep(0.5 * attempt)
        if last_error:
            raise last_error
        return Classification("Other", 0.0, "Classification failed.")


def build_user_prompt(sentence: str) -> str:
    categories = "\n".join(CATEGORIES)
    return f"""Sentence:\n{sentence}\n\nCategories:\n{categories}\n\nReturn JSON:\n{{\"category\":\"\",\"confidence\":0.0,\"reason\":\"\"}}"""


def parse_classification(text: str) -> Classification:
    data = json.loads(text)
    category = str(data.get("category", "Other"))
    if category not in CATEGORIES:
        category = "Other"
    confidence = float(data.get("confidence", 0.0))
    reason = str(data.get("reason", ""))
    return Classification(category, max(0.0, min(1.0, confidence)), reason)
