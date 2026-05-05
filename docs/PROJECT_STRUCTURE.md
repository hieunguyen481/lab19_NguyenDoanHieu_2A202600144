# Project Structure

Tài liệu này mô tả vai trò từng nhóm file trong `C401_D3_Day19`.

## Root files

| File | Vai trò |
|---|---|
| `Readme.md` | Trang điều hướng chính để chạy và hiểu project. |
| `PLAN.md` | Kế hoạch triển khai ban đầu, dùng để giải thích approach. |
| `SETUP_AND_UPGRADE.md` | Hướng dẫn OpenAI, Neo4j, NodeRAG, Docker. |
| `requirements.txt` | Dependencies nhẹ cho bản NetworkX. |
| `.env.example` | Template biến môi trường, không chứa key thật. |
| `run_day19.ps1` | Helper script cho Windows PowerShell. |

## Source modules

| File | Vai trò |
|---|---|
| `src/pipeline.py` | Entry point chạy toàn bộ lab. |
| `src/schema.py` | Nơi định nghĩa relation whitelist, alias, canonicalization. |
| `src/corpus.py` | Load và chunk corpus Markdown. |
| `src/extract_triples.py` | Lấy triples từ seed hoặc OpenAI. |
| `src/graph_builder.py` | Dedup triples, build NetworkX graph, vẽ graph, export GraphML. |
| `src/graph_query.py` | Tìm entity trong query, duyệt graph 2-hop, sinh GraphRAG answer. |
| `src/flat_rag.py` | Flat RAG baseline bằng lexical retrieval. |
| `src/evaluate.py` | Chấm benchmark và sinh bảng so sánh. |
| `src/export_neo4j.py` | Sinh Cypher import cho Neo4j. |
| `src/env.py` | Load `.env`. |
| `src/paths.py` | Quản lý đường dẫn dùng chung. |

## Data and outputs

| Folder | Vai trò |
|---|---|
| `data/` | Input cố định: corpus, seed triples, benchmark. |
| `reports/` | Output machine-readable: JSON, GraphML, Cypher. |
| `figures/` | Output hình ảnh graph. |
| `analysis/` | Output đọc/nộp: research answers, comparison table, final report. |

## Generated or local-only files

Các mục sau không phải bài nộp:

- `.env`
- `.venv*`
- `__pycache__/`
- `.pytest_cache/`
- `*.pyc`
