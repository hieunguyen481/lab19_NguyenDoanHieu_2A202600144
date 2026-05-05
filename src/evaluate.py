"""Benchmark Flat RAG vs GraphRAG."""

from __future__ import annotations

import json
import re
from statistics import mean

from .paths import BENCHMARK_PATH, COMPARISON_REPORT_PATH, COMPARISON_TABLE_PATH
from .schema import ENTITY_VARIANTS


def load_benchmark(path=BENCHMARK_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_any(text: str, item: str) -> bool:
    text_norm = normalize(text)
    variants = ENTITY_VARIANTS.get(item, [item])
    for variant in variants:
        item_norm = normalize(variant)
        if item_norm in text_norm:
            return True
        compact_text = re.sub(r"[^a-z0-9à-ỹ]", "", text_norm)
        compact_item = re.sub(r"[^a-z0-9à-ỹ]", "", item_norm)
        if compact_item and compact_item in compact_text:
            return True
    return False


def score_answer(answer: str, required_entities: list[str], required_relations: list[str], evidence: str = "") -> dict:
    entity_hits = [entity for entity in required_entities if contains_any(answer + "\n" + evidence, entity)]
    relation_hits = [relation for relation in required_relations if contains_any(evidence, relation)]
    entity_score = len(entity_hits) / len(required_entities) if required_entities else 1.0
    relation_score = len(set(relation_hits)) / len(set(required_relations)) if required_relations else 1.0
    score = round((entity_score * 0.7) + (relation_score * 0.3), 3)
    return {
        "score": score,
        "entity_score": round(entity_score, 3),
        "relation_score": round(relation_score, 3),
        "entity_hits": entity_hits,
        "relation_hits": sorted(set(relation_hits)),
    }


def compare_results(benchmark: list[dict], flat_outputs: list[dict], graph_outputs: list[dict]) -> dict:
    rows = []
    for item, flat, graph in zip(benchmark, flat_outputs, graph_outputs):
        flat_evidence = "\n".join(flat.get("contexts", []))
        graph_evidence = graph.get("context", "")
        flat_score = score_answer(
            flat["answer"], item.get("required_entities", []), item.get("required_relations", []), flat_evidence
        )
        graph_score = score_answer(
            graph["answer"], item.get("required_entities", []), item.get("required_relations", []), graph_evidence
        )
        if graph_score["score"] > flat_score["score"]:
            winner = "GraphRAG"
        elif flat_score["score"] > graph_score["score"]:
            winner = "Flat RAG"
        else:
            winner = "Tie"
        rows.append({
            "id": item["id"],
            "question": item["question"],
            "ground_truth": item["ground_truth"],
            "flat_answer": flat["answer"],
            "graphrag_answer": graph["answer"],
            "flat_score": flat_score,
            "graphrag_score": graph_score,
            "winner": winner,
            "graph_entities": graph.get("entities", []),
        })

    return {
        "summary": {
            "num_questions": len(rows),
            "flat_avg_score": round(mean(row["flat_score"]["score"] for row in rows), 3),
            "graphrag_avg_score": round(mean(row["graphrag_score"]["score"] for row in rows), 3),
            "flat_wins": sum(row["winner"] == "Flat RAG" for row in rows),
            "graph_wins": sum(row["winner"] == "GraphRAG" for row in rows),
            "ties": sum(row["winner"] == "Tie" for row in rows),
        },
        "rows": rows,
    }


def save_comparison_report(report: dict, path=COMPARISON_REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def save_markdown_table(report: dict, path=COMPARISON_TABLE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Bảng so sánh Flat RAG vs GraphRAG",
        "",
        f"- Số câu hỏi: {report['summary']['num_questions']}",
        f"- Flat RAG average score: {report['summary']['flat_avg_score']}",
        f"- GraphRAG average score: {report['summary']['graphrag_avg_score']}",
        f"- GraphRAG thắng: {report['summary']['graph_wins']}",
        f"- Flat RAG thắng: {report['summary']['flat_wins']}",
        f"- Hòa: {report['summary']['ties']}",
        "",
        "| ID | Question | Flat | GraphRAG | Winner |",
        "|---|---|---:|---:|---|",
    ]
    for row in report["rows"]:
        q = row["question"].replace("|", "\\|")
        lines.append(
            f"| {row['id']} | {q} | {row['flat_score']['score']} | "
            f"{row['graphrag_score']['score']} | {row['winner']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize_cost(flat_outputs: list[dict], graph_outputs: list[dict], extraction_stats: dict, elapsed: float) -> dict:
    def usage_sum(outputs: list[dict]) -> dict:
        total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        for output in outputs:
            usage = output.get("usage", {})
            for key in total:
                total[key] += int(usage.get(key, 0) or 0)
        return total

    return {
        "elapsed_seconds": round(elapsed, 3),
        "triple_extraction": extraction_stats,
        "flat_rag_generation": usage_sum(flat_outputs),
        "graphrag_generation": usage_sum(graph_outputs),
        "note": "Token counts are zero when running in offline fallback mode without OPENAI_API_KEY.",
    }
