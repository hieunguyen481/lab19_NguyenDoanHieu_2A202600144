"""Corpus loading and lightweight chunking."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .paths import CORPUS_PATH


@dataclass
class Document:
    doc_id: str
    title: str
    text: str


def load_corpus(path=CORPUS_PATH) -> list[Document]:
    """Load markdown corpus sections headed by '## doc_id: title'."""
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"^##\s+(doc_\d+):\s*(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    documents: list[Document] = []

    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        documents.append(Document(doc_id=match.group(1), title=match.group(2).strip(), text=body))

    return documents


def chunk_documents(documents: list[Document], max_chars: int = 900) -> list[dict]:
    """Split each document into paragraph chunks while keeping source metadata."""
    chunks: list[dict] = []
    for doc in documents:
        paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
        current = ""
        chunk_index = 0
        for paragraph in paragraphs:
            if current and len(current) + len(paragraph) > max_chars:
                chunks.append({
                    "text": current.strip(),
                    "metadata": {"source_id": doc.doc_id, "title": doc.title, "chunk_index": chunk_index},
                })
                chunk_index += 1
                current = ""
            current += paragraph + "\n\n"
        if current.strip():
            chunks.append({
                "text": current.strip(),
                "metadata": {"source_id": doc.doc_id, "title": doc.title, "chunk_index": chunk_index},
            })
    return chunks
