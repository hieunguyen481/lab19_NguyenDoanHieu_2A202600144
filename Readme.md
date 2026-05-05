# Lab Day 19: GraphRAG với Tech Company Corpus

Day 19 xây dựng một pipeline **GraphRAG** hoàn chỉnh trên corpus công ty công nghệ. Bản chính dùng **NetworkX** để chạy nhẹ, dễ demo và không bắt buộc Neo4j/NodeRAG. OpenAI API key là tùy chọn để bật LLM extraction/generation.

## 1. Chạy nhanh

```bash
cd C401_D3_Day19
pip install -r requirements.txt
python -B src/pipeline.py
```

Sau khi chạy, kiểm tra các file chính:

| File | Nội dung |
|---|---|
| `figures/knowledge_graph.png` | Ảnh đồ thị tri thức |
| `reports/triples.json` | Triples sau khi extract + dedup |
| `reports/graph_stats.json` | Thống kê node/edge/relation |
| `reports/comparison_report.json` | Kết quả chi tiết 20 câu benchmark |
| `reports/cost_report.json` | Token/time usage |
| `analysis/comparison_table.md` | Bảng so sánh Flat RAG vs GraphRAG |
| `analysis/final_report.md` | Báo cáo ngắn để nộp |

## 2. Luồng hệ thống

```text
Tech Company Corpus
    -> chunk documents
    -> extract triples bằng seed hoặc OpenAI
    -> deduplicate/canonicalize entities
    -> build NetworkX knowledge graph
    -> GraphRAG 2-hop traversal
    -> Flat RAG lexical baseline
    -> compare 20 benchmark questions
    -> save reports + graph image
```

## 3. Cấu trúc folder

```text
C401_D3_Day19/
├── Readme.md                  # Trang chính: cách chạy và overview
├── SETUP_AND_UPGRADE.md       # OpenAI, Neo4j, NodeRAG, Docker
├── PLAN.md                    # Kế hoạch triển khai chi tiết
├── docs/
│   ├── PROJECT_STRUCTURE.md   # Giải thích vai trò từng file/folder
│   └── EVALUATION.md          # Cách chấm Flat RAG vs GraphRAG
├── requirements.txt
├── .env.example
├── run_day19.ps1              # Helper chạy nhanh trên PowerShell
├── data/
│   ├── tech_company_corpus.md
│   ├── seed_triples.json
│   └── benchmark_questions.json
├── src/
│   ├── pipeline.py            # Entry point chính
│   ├── schema.py              # Relation schema, aliases, canonical names
│   ├── corpus.py              # Load/chunk corpus
│   ├── extract_triples.py     # Seed/LLM triple extraction
│   ├── graph_builder.py       # Build/visualize/export NetworkX graph
│   ├── graph_query.py         # 2-hop GraphRAG query
│   ├── flat_rag.py            # Flat RAG lexical baseline
│   ├── evaluate.py            # Benchmark scoring + markdown report
│   ├── export_neo4j.py        # Export Cypher for Neo4j
│   ├── env.py                 # Load .env
│   └── paths.py               # Shared paths
├── analysis/
│   ├── research_answers.md
│   ├── comparison_table.md
│   └── final_report.md
├── reports/
│   ├── triples.json
│   ├── graph_stats.json
│   ├── comparison_report.json
│   ├── cost_report.json
│   ├── knowledge_graph.graphml
│   └── neo4j_import.cypher
└── figures/
    └── knowledge_graph.png
```

Nếu có `.venv_noderag` hoặc `__pycache__`, đó là file sinh ra khi chạy/cài thử, không phải phần bài nộp.

## 4. Chế độ chạy

| Chế độ | Lệnh | Ghi chú |
|---|---|---|
| Offline ổn định | `python -B src/pipeline.py` | Dùng `data/seed_triples.json`, không cần API key |
| OpenAI generate | Đặt `USE_OPENAI_GENERATION=1`, rồi chạy `python -B src/pipeline.py` | LLM sinh câu trả lời từ context |
| OpenAI extract | Đặt `USE_OPENAI_GENERATION=1` và `USE_LLM_EXTRACTION=1`, rồi chạy `python -B src/pipeline.py` | LLM extract triples từ corpus |
| Neo4j export | `python -B src/export_neo4j.py` | Sinh `reports/neo4j_import.cypher` |

PowerShell helper:

```powershell
.\run_day19.ps1 offline
.\run_day19.ps1 openai-generate
.\run_day19.ps1 openai-extract
.\run_day19.ps1 neo4j-export
```

## 5. Bật OpenAI API key

Tạo file `.env` từ `.env.example`:

```text
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
USE_OPENAI_GENERATION=1
USE_LLM_EXTRACTION=0
```

Khi có `OPENAI_API_KEY` và `USE_OPENAI_GENERATION=1`, pipeline bật LLM generation. Nếu `USE_LLM_EXTRACTION=1`, pipeline sẽ thử dùng LLM để extract triples; nếu lỗi hoặc không có triples hợp lệ, hệ thống fallback về `seed_triples.json`.

## 6. Vì sao chọn NetworkX trước

NetworkX phù hợp làm bản nộp chính vì:

1. Chạy offline, ít phụ thuộc môi trường.
2. Dễ kiểm tra triples, node, edge.
3. Dễ tạo ảnh graph bằng Matplotlib.
4. Vẫn có thể export sang Neo4j bằng Cypher.

Neo4j và NodeRAG là hướng nâng cấp, không bắt buộc để hoàn thành deliverables. Xem chi tiết trong `SETUP_AND_UPGRADE.md`.

## 7. Deliverables đã có

| Yêu cầu bài | File đáp ứng |
|---|---|
| Mã nguồn `.py` | `src/` |
| Ảnh đồ thị tri thức | `figures/knowledge_graph.png` |
| 20 câu benchmark | `data/benchmark_questions.json` |
| Bảng so sánh Flat RAG vs GraphRAG | `analysis/comparison_table.md` |
| Phân tích chi phí token/time | `reports/cost_report.json` |
| Báo cáo cuối | `analysis/final_report.md` |
| Research answers | `analysis/research_answers.md` |

## 8. Kết quả hiện tại

Lần chạy OpenAI generation gần nhất:

- Documents: 10
- Triples sau dedup: 80
- Graph nodes: 67
- Graph edges: 94
- Flat RAG average score: 0.922
- GraphRAG average score: 0.98
- Flat RAG generation tokens: 5,576
- GraphRAG generation tokens: 11,128
- Elapsed time: 59.435 seconds

Kết quả chi tiết nằm trong `reports/comparison_report.json`.
