"""Lightweight Flat RAG baseline.

This intentionally avoids heavy vector databases so the lab can run with only
standard Python plus optional OpenAI.
"""

from __future__ import annotations

import math
import os
import re
import time
from collections import Counter

from .env import load_environment


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9À-ỹ]+", text.lower())


class LexicalSearch:
    def __init__(self) -> None:
        self.documents: list[dict] = []
        self.doc_freq: Counter[str] = Counter()
        self.doc_tokens: list[list[str]] = []

    def index(self, chunks: list[dict]) -> None:
        self.documents = chunks
        self.doc_tokens = [tokenize(chunk["text"]) for chunk in chunks]
        self.doc_freq.clear()
        for tokens in self.doc_tokens:
            self.doc_freq.update(set(tokens))

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        query_tokens = tokenize(query)
        query_counts = Counter(query_tokens)
        num_docs = max(len(self.documents), 1)
        scored: list[dict] = []

        for idx, tokens in enumerate(self.doc_tokens):
            token_counts = Counter(tokens)
            score = 0.0
            for token, q_count in query_counts.items():
                if token not in token_counts:
                    continue
                idf = math.log((num_docs + 1) / (self.doc_freq[token] + 1)) + 1
                score += q_count * token_counts[token] * idf
            if score > 0:
                doc = self.documents[idx]
                scored.append({
                    "text": doc["text"],
                    "score": round(score, 4),
                    "metadata": doc.get("metadata", {}),
                })

        return sorted(scored, key=lambda item: item["score"], reverse=True)[:top_k]


def generate_flat_answer(question: str, contexts: list[str]) -> tuple[str, dict]:
    load_environment()
    if not contexts:
        return "Không tìm thấy thông tin trong corpus.", {"used_llm": False}
    if not os.getenv("OPENAI_API_KEY"):
        return contexts[0], {"used_llm": False, "reason": "missing OPENAI_API_KEY"}
    try:
        from openai import OpenAI
    except ImportError:
        return contexts[0], {"used_llm": False, "reason": "openai package not installed"}

    start = time.time()
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    context_text = "\n\n".join(contexts)
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Bạn là trợ lý Flat RAG. Chỉ dùng context được cung cấp. "
                        "Nếu context thiếu bằng chứng, nói không tìm thấy thông tin."
                    ),
                },
                {"role": "user", "content": f"Context:\n{context_text}\n\nCâu hỏi: {question}"},
            ],
        )
    except Exception as exc:
        return contexts[0], {"used_llm": False, "error": f"{type(exc).__name__}: {exc}"}
    usage = response.usage
    return response.choices[0].message.content or "", {
        "used_llm": True,
        "seconds": round(time.time() - start, 3),
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "total_tokens": usage.total_tokens if usage else 0,
    }


def answer_question(question: str, search: LexicalSearch, use_llm: bool = True) -> dict:
    results = search.search(question)
    contexts = [result["text"] for result in results]
    if use_llm:
        answer, usage = generate_flat_answer(question, contexts)
    else:
        answer, usage = (contexts[0] if contexts else "Không tìm thấy thông tin trong corpus.", {"used_llm": False})
    return {
        "question": question,
        "answer": answer,
        "contexts": contexts,
        "results": results,
        "usage": usage,
    }
