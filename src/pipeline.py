"""Run the full Day 19 GraphRAG pipeline."""

from __future__ import annotations

import json
import os
import sys
import time

if __package__ in {None, ""}:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.corpus import chunk_documents, load_corpus
from src.env import load_environment, openai_enabled
from src.evaluate import compare_results, load_benchmark, save_comparison_report, save_markdown_table, summarize_cost
from src.extract_triples import extract_triples, save_triples
from src.flat_rag import LexicalSearch, answer_question as flat_answer_question
from src.graph_builder import build_graph, deduplicate_triples, draw_graph, save_graph_outputs
from src.graph_query import answer_question as graph_answer_question
from src.paths import COMPARISON_REPORT_PATH, COST_REPORT_PATH, FINAL_REPORT_PATH, GRAPH_STATS_PATH


def write_final_report(comparison: dict, graph_stats: dict, figure_created: bool) -> None:
    FINAL_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = comparison["summary"]
    graph_win_cases = [row for row in comparison["rows"] if row["winner"] == "GraphRAG"][:5]
    graph_cases_text = "\n".join(
        f"- `{row['id']}`: {row['question']} "
        f"(Flat={row['flat_score']['score']}, GraphRAG={row['graphrag_score']['score']})"
        for row in graph_win_cases
    )
    lines = [
        "# Báo cáo Lab Day 19 - GraphRAG",
        "",
        "## 1. Mục tiêu",
        "",
        "Xây dựng hệ thống GraphRAG trên Tech Company Corpus, sau đó so sánh với Flat RAG baseline "
        "trên 20 câu hỏi benchmark. Hệ thống tập trung vào các câu hỏi cần nối nhiều quan hệ như "
        "founder -> company -> product hoặc company -> parent company -> CEO.",
        "",
        "## 2. Kiến trúc",
        "",
        "Pipeline gồm các bước: load corpus, chunk documents, extract triples, deduplicate entities, "
        "build NetworkX graph, truy vấn graph 2-hop, chạy Flat RAG baseline, rồi đánh giá hai hệ thống.",
        "",
        "## 3. Thống kê graph",
        "",
        f"- Nodes: {graph_stats['num_nodes']}",
        f"- Edges: {graph_stats['num_edges']}",
        f"- Node types: {graph_stats['node_types']}",
        f"- Relation types: {graph_stats['relation_types']}",
        f"- Ảnh graph: {'figures/knowledge_graph.png' if figure_created else 'Chưa tạo được, cần kiểm tra matplotlib'}",
        "",
        "## 4. Kết quả benchmark",
        "",
        f"- Số câu hỏi: {summary['num_questions']}",
        f"- Flat RAG average score: {summary['flat_avg_score']}",
        f"- GraphRAG average score: {summary['graphrag_avg_score']}",
        f"- GraphRAG thắng: {summary['graph_wins']}",
        f"- Flat RAG thắng: {summary['flat_wins']}",
        f"- Hòa: {summary['ties']}",
        "",
        "## 5. Một số case GraphRAG tốt hơn",
        "",
        graph_cases_text or "- Không có case GraphRAG thắng trong lần chạy này.",
        "",
        "## 6. Nhận xét",
        "",
        "GraphRAG mạnh hơn ở các câu hỏi cần nối nhiều quan hệ như founder -> company -> product, "
        "company -> parent company -> CEO, hoặc competition giữa các sản phẩm/công ty. Flat RAG có thể đủ "
        "cho câu hỏi nằm gọn trong một đoạn văn, nhưng dễ thiếu bằng chứng quan hệ khi thông tin phân tán.",
        "",
        "## 7. Chi phí",
        "",
        "Chi phí token/time chi tiết nằm trong `reports/cost_report.json`. Khi chạy offline không có "
        "`OPENAI_API_KEY`, token usage bằng 0 vì hệ thống dùng seed triples và fallback answers.",
    ]
    FINAL_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    load_environment()
    start = time.time()
    print("[1/7] Loading corpus...")
    documents = load_corpus()
    chunks = chunk_documents(documents)
    print(f"  documents={len(documents)} chunks={len(chunks)}")

    print("[2/7] Extracting triples...")
    triples, extraction_stats = extract_triples(chunks)
    triples = deduplicate_triples(triples)
    save_triples(triples)
    print(f"  triples={len(triples)} mode={extraction_stats.get('mode')}")

    print("[3/7] Building NetworkX graph...")
    graph = build_graph(triples)
    save_graph_outputs(graph)
    figure_created = draw_graph(graph)
    graph_stats = {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "node_types": {},
        "relation_types": {},
    }
    if GRAPH_STATS_PATH.exists():
        graph_stats = json.loads(GRAPH_STATS_PATH.read_text(encoding="utf-8"))
    print(f"  nodes={graph.number_of_nodes()} edges={graph.number_of_edges()} figure={figure_created}")

    print("[4/7] Building Flat RAG baseline...")
    search = LexicalSearch()
    search.index(chunks)

    print("[5/7] Running 20-question benchmark...")
    benchmark = load_benchmark()
    use_llm = openai_enabled()
    print(f"  OpenAI generation={'on' if use_llm else 'off'}")
    flat_outputs = []
    graph_outputs = []
    for idx, item in enumerate(benchmark, start=1):
        flat_outputs.append(flat_answer_question(item["question"], search, use_llm=use_llm))
        graph_outputs.append(graph_answer_question(item["question"], graph, use_llm=use_llm))
        print(f"  {idx:02d}/{len(benchmark)} {item['id']}")

    print("[6/7] Evaluating and saving reports...")
    comparison = compare_results(benchmark, flat_outputs, graph_outputs)
    save_comparison_report(comparison)
    save_markdown_table(comparison)
    cost = summarize_cost(flat_outputs, graph_outputs, extraction_stats, time.time() - start)
    COST_REPORT_PATH.write_text(json.dumps(cost, ensure_ascii=False, indent=2), encoding="utf-8")
    write_final_report(comparison, graph_stats, figure_created)

    print("[7/7] Done.")
    print(f"  Flat avg: {comparison['summary']['flat_avg_score']}")
    print(f"  Graph avg: {comparison['summary']['graphrag_avg_score']}")
    print(f"  Reports: {COMPARISON_REPORT_PATH.parent}")


if __name__ == "__main__":
    main()
