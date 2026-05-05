"""2-hop GraphRAG querying and answer generation."""

from __future__ import annotations

import os
import re
import time
from collections import deque
from difflib import get_close_matches

import networkx as nx

from .env import load_environment


def find_entities(question: str, graph: nx.MultiDiGraph, max_entities: int = 3) -> list[str]:
    q = question.lower()
    exact = [node for node in graph.nodes if node.lower() in q]
    if exact:
        return exact[:max_entities]

    tokens = set(re.findall(r"[A-Za-z][A-Za-z0-9]+", question))
    candidates = [node for node in graph.nodes if any(tok.lower() in node.lower() for tok in tokens)]
    if candidates:
        return sorted(candidates, key=len)[:max_entities]

    matches = get_close_matches(question, list(graph.nodes), n=max_entities, cutoff=0.35)
    return matches


def collect_2hop_triples(graph: nx.MultiDiGraph, start_nodes: list[str], max_hops: int = 2) -> list[dict]:
    visited = set(start_nodes)
    queue = deque((node, 0) for node in start_nodes)
    triples: list[dict] = []
    seen_edges: set[tuple[str, str, str]] = set()

    while queue:
        node, depth = queue.popleft()
        if depth >= max_hops:
            continue

        for _, target, key, data in graph.out_edges(node, keys=True, data=True):
            edge_id = (node, data.get("relation", key), target)
            if edge_id not in seen_edges:
                triples.append({
                    "subject": node,
                    "relation": data.get("relation", key),
                    "object": target,
                    "sources": data.get("sources", ""),
                })
                seen_edges.add(edge_id)
            if target not in visited:
                visited.add(target)
                queue.append((target, depth + 1))

        for source, _, key, data in graph.in_edges(node, keys=True, data=True):
            edge_id = (source, data.get("relation", key), node)
            if edge_id not in seen_edges:
                triples.append({
                    "subject": source,
                    "relation": data.get("relation", key),
                    "object": node,
                    "sources": data.get("sources", ""),
                })
                seen_edges.add(edge_id)
            if source not in visited:
                visited.add(source)
                queue.append((source, depth + 1))

    return triples


def textualize_triples(triples: list[dict]) -> str:
    if not triples:
        return "No graph evidence found."
    return "\n".join(
        f"- {t['subject']} {t['relation']} {t['object']} (source: {t.get('sources', 'unknown')})"
        for t in triples
    )


def fallback_answer(question: str, triples: list[dict]) -> str:
    if not triples:
        return "Không tìm thấy thông tin trong knowledge graph."

    lower = question.lower()
    desired_relations: set[str] = set()
    if "trụ sở" in lower or "headquarter" in lower:
        desired_relations.add("HEADQUARTERED_IN")
    if "ceo" in lower:
        desired_relations.add("HAS_CEO")
    if "công ty mẹ" in lower or "parent" in lower:
        desired_relations.add("PARENT_OF")
    if "phát triển" in lower or "develop" in lower:
        desired_relations.add("DEVELOPS")
    if "cạnh tranh" in lower or "compete" in lower:
        desired_relations.add("COMPETES_WITH")
    if "sáng lập" in lower or "founded" in lower:
        desired_relations.update({"FOUNDED_BY", "FOUNDED_IN"})
    if "đầu tư" in lower or "invest" in lower:
        desired_relations.add("INVESTS_IN")
    if "vận hành" in lower or "operates" in lower:
        desired_relations.update({"OPERATES", "OPERATES_IN"})
    if "mua" in lower or "acquired" in lower:
        desired_relations.update({"ACQUIRED", "ACQUIRED_IN"})

    selected = [t for t in triples if t["relation"] in desired_relations] if desired_relations else triples[:8]

    if not selected:
        selected = triples[:8]
    facts = "; ".join(f"{t['subject']} {t['relation']} {t['object']}" for t in selected[:10])
    return f"Dựa trên graph context: {facts}."


def generate_answer(question: str, context: str) -> tuple[str, dict]:
    load_environment()
    if not os.getenv("OPENAI_API_KEY"):
        return "", {"used_llm": False, "reason": "missing OPENAI_API_KEY"}
    try:
        from openai import OpenAI
    except ImportError:
        return "", {"used_llm": False, "reason": "openai package not installed"}

    start = time.time()
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Bạn là trợ lý GraphRAG. Chỉ trả lời dựa trên graph context. "
                        "Nếu context không đủ, nói rõ là không tìm thấy thông tin."
                    ),
                },
                {"role": "user", "content": f"Graph context:\n{context}\n\nCâu hỏi: {question}"},
            ],
        )
    except Exception as exc:
        return "", {"used_llm": False, "error": f"{type(exc).__name__}: {exc}"}
    usage = response.usage
    return response.choices[0].message.content or "", {
        "used_llm": True,
        "seconds": round(time.time() - start, 3),
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "completion_tokens": usage.completion_tokens if usage else 0,
        "total_tokens": usage.total_tokens if usage else 0,
    }


def answer_question(question: str, graph: nx.MultiDiGraph, use_llm: bool = True) -> dict:
    entities = find_entities(question, graph)
    triples = collect_2hop_triples(graph, entities)
    context = textualize_triples(triples)
    answer = ""
    usage = {"used_llm": False}
    if use_llm:
        answer, usage = generate_answer(question, context)
    if not answer:
        answer = fallback_answer(question, triples)
    return {
        "question": question,
        "entities": entities,
        "answer": answer,
        "context": context,
        "triples": triples,
        "usage": usage,
    }
