"""Shared paths for Day 19."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = ROOT_DIR / "figures"
ANALYSIS_DIR = ROOT_DIR / "analysis"

CORPUS_PATH = DATA_DIR / "tech_company_corpus.md"
SEED_TRIPLES_PATH = DATA_DIR / "seed_triples.json"
BENCHMARK_PATH = DATA_DIR / "benchmark_questions.json"

TRIPLES_REPORT_PATH = REPORTS_DIR / "triples.json"
GRAPH_STATS_PATH = REPORTS_DIR / "graph_stats.json"
GRAPHML_PATH = REPORTS_DIR / "knowledge_graph.graphml"
NEO4J_CYPHER_PATH = REPORTS_DIR / "neo4j_import.cypher"
COMPARISON_REPORT_PATH = REPORTS_DIR / "comparison_report.json"
COST_REPORT_PATH = REPORTS_DIR / "cost_report.json"

GRAPH_FIGURE_PATH = FIGURES_DIR / "knowledge_graph.png"
COMPARISON_TABLE_PATH = ANALYSIS_DIR / "comparison_table.md"
FINAL_REPORT_PATH = ANALYSIS_DIR / "final_report.md"
