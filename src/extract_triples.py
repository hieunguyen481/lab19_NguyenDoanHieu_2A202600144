"""Triple extraction for GraphRAG.

Default mode uses curated seed triples so the lab can run without network access.
Set USE_LLM_EXTRACTION=1 and OPENAI_API_KEY to try LLM extraction from corpus chunks.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass

from .paths import SEED_TRIPLES_PATH, TRIPLES_REPORT_PATH
from .env import load_environment
from .schema import ALLOWED_RELATIONS


@dataclass(frozen=True)
class Triple:
    subject: str
    relation: str
    object: str
    subject_type: str = "Entity"
    object_type: str = "Entity"
    source_id: str = "unknown"
    confidence: float = 1.0


def load_seed_triples(path=SEED_TRIPLES_PATH) -> list[Triple]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Triple(**item) for item in data if item.get("relation") in ALLOWED_RELATIONS]


def extract_triples_with_llm(chunks: list[dict]) -> tuple[list[Triple], dict]:
    """Extract triples with OpenAI if an API key is available."""
    load_environment()
    if not os.getenv("OPENAI_API_KEY"):
        return [], {"mode": "llm", "used": False, "reason": "missing OPENAI_API_KEY"}

    try:
        from openai import OpenAI
    except ImportError:
        return [], {"mode": "llm", "used": False, "reason": "openai package not installed"}

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    triples: list[Triple] = []
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    start = time.time()

    system = (
        "Extract knowledge graph triples from tech company text. "
        "Return only valid JSON array. Each object must have subject, relation, object, "
        "subject_type, object_type, source_id, confidence. "
        f"Allowed relations: {sorted(ALLOWED_RELATIONS)}. "
        "Do not infer facts not present in the text."
    )

    for chunk in chunks:
        source_id = chunk["metadata"]["source_id"]
        prompt = f"source_id={source_id}\nText:\n{chunk['text']}"
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content or "[]"
            content = content.strip().removeprefix("```json").removesuffix("```").strip()
            data = json.loads(content)
            for item in data:
                relation = item.get("relation", "")
                if relation not in ALLOWED_RELATIONS:
                    continue
                triples.append(Triple(
                    subject=item.get("subject", "").strip(),
                    relation=relation,
                    object=item.get("object", "").strip(),
                    subject_type=item.get("subject_type", "Entity"),
                    object_type=item.get("object_type", "Entity"),
                    source_id=item.get("source_id", source_id),
                    confidence=float(item.get("confidence", 0.8)),
                ))
            if response.usage:
                usage["prompt_tokens"] += response.usage.prompt_tokens or 0
                usage["completion_tokens"] += response.usage.completion_tokens or 0
                usage["total_tokens"] += response.usage.total_tokens or 0
        except Exception as exc:
            return triples, {"mode": "llm", "used": True, "error": str(exc), **usage}

    return triples, {"mode": "llm", "used": True, "seconds": round(time.time() - start, 3), **usage}


def extract_triples(chunks: list[dict], prefer_llm: bool = False) -> tuple[list[Triple], dict]:
    """Return triples from LLM mode or seed fallback."""
    if prefer_llm or os.getenv("USE_LLM_EXTRACTION") == "1":
        triples, stats = extract_triples_with_llm(chunks)
        if triples:
            return triples, stats

    triples = load_seed_triples()
    return triples, {"mode": "seed", "used": True, "num_triples": len(triples)}


def save_triples(triples: list[Triple], path=TRIPLES_REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([asdict(t) for t in triples], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
