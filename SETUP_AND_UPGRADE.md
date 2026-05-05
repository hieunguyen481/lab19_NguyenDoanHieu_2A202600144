# Setup và nâng cấp Day 19 chi tiết

## 1. Các chế độ chạy

Project hiện có 4 chế độ:

| Chế độ | Lệnh | Cần API key | Cần tool nặng | Mục đích |
|---|---|---:|---:|---|
| Offline base | `python -B src/pipeline.py` | Không | Không | Demo ổn định bằng `seed_triples.json`. |
| OpenAI generate | `python -B src/pipeline.py` sau khi có `.env` | Có | Không | Dùng LLM để sinh câu trả lời từ Flat/Graph context. |
| OpenAI extract + generate | `$env:USE_LLM_EXTRACTION="1"; python -B src/pipeline.py` | Có | Không | Dùng LLM extract triples từ corpus rồi query/generate. |
| Neo4j export | `python -B src/export_neo4j.py` | Không | Neo4j nếu muốn import | Sinh Cypher để đưa graph vào Neo4j. |

Bạn cũng có thể dùng PowerShell helper:

```powershell
.\run_day19.ps1 offline
.\run_day19.ps1 openai-generate
.\run_day19.ps1 openai-extract
.\run_day19.ps1 neo4j-export
```

## 2. Cài dependencies nhẹ

```bash
cd C401_D3_Day19
pip install -r requirements.txt
```

Dependencies bắt buộc hiện tại:

- `networkx`: build graph
- `matplotlib`: vẽ `knowledge_graph.png`
- `openai`: gọi ChatGPT/OpenAI nếu có key
- `python-dotenv`: tự đọc file `.env`
- `pandas`: để tiện mở rộng report

Không cần tải model embedding, không cần Chroma/Faiss/Qdrant cho bản hiện tại.

## 3. Bật API key OpenAI

Tạo file `.env` trong `C401_D3_Day19`:

```text
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

Lưu ý:

1. Không commit `.env`.
2. `.env.example` chỉ là template, không chứa key thật.
3. Code đã tự load `.env` bằng `python-dotenv`, nên bạn không cần set biến môi trường thủ công nếu file `.env` nằm đúng folder.

Chạy:

```bash
python -B src/pipeline.py
```

Khi có API key, pipeline sẽ:

1. Vẫn dùng `seed_triples.json` để build graph ổn định.
2. Dùng OpenAI để sinh câu trả lời từ Flat RAG context.
3. Dùng OpenAI để sinh câu trả lời từ GraphRAG context.
4. Ghi token usage vào `reports/cost_report.json`.

Đây là chế độ khuyến nghị khi nộp nếu bạn muốn có answer tự nhiên hơn nhưng vẫn tránh rủi ro LLM extract thiếu triples.

## 4. Bật LLM triple extraction

Chỉ dùng khi bạn muốn chứng minh bước Entity/Relation Extraction bằng LLM.

PowerShell:

```powershell
$env:USE_LLM_EXTRACTION="1"
python -B src/pipeline.py
```

Bash:

```bash
USE_LLM_EXTRACTION=1 python -B src/pipeline.py
```

Khi bật chế độ này:

1. `src/extract_triples.py` gửi từng chunk corpus lên OpenAI.
2. Model phải trả về JSON triples theo whitelist relation.
3. Code validate relation, bỏ quan hệ ngoài whitelist.
4. Nếu LLM lỗi hoặc không trả triples, pipeline fallback về `seed_triples.json`.

Khuyến nghị thực tế:

- Khi luyện tập/explain: bật `USE_LLM_EXTRACTION=1`.
- Khi nộp demo ổn định: tắt `USE_LLM_EXTRACTION`, dùng seed triples.

## 5. Output cần kiểm tra sau khi chạy

Sau mỗi lần chạy pipeline, kiểm tra:

```text
reports/triples.json
reports/graph_stats.json
reports/knowledge_graph.graphml
reports/comparison_report.json
reports/cost_report.json
figures/knowledge_graph.png
analysis/comparison_table.md
analysis/final_report.md
```

`reports/cost_report.json` sẽ có token nếu OpenAI được dùng. Nếu chạy offline, token bằng 0.

## 6. Neo4j Desktop

Dùng Neo4j Desktop nếu bạn muốn có giao diện graph đẹp để chụp màn hình.

Các bước:

1. Tải và cài Neo4j Desktop từ trang chủ Neo4j.
2. Tạo project mới.
3. Tạo local DBMS, ví dụ:
   - name: `day19-graphrag`
   - password: `password`
4. Start DB.
5. Chạy pipeline và export Cypher:

```bash
python -B src/pipeline.py
python -B src/export_neo4j.py
```

6. Mở Neo4j Browser trong Desktop.
7. Mở file `reports/neo4j_import.cypher`, copy nội dung và paste vào Browser.
8. Chạy query kiểm tra:

```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100;
```

Query gợi ý để xem quanh OpenAI:

```cypher
MATCH p=(n {name: 'OpenAI'})-[*1..2]-(m)
RETURN p
LIMIT 50;
```

## 7. Neo4j Docker

Chỉ làm nếu máy đã có Docker Desktop.

```bash
docker run --name neo4j-day19 ^
  -p 7474:7474 -p 7687:7687 ^
  -e NEO4J_AUTH=neo4j/password ^
  neo4j:5
```

Trên PowerShell một dòng:

```powershell
docker run --name neo4j-day19 -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5
```

Mở:

```text
http://localhost:7474
```

Đăng nhập:

- user: `neo4j`
- password: `password`

Sau đó import bằng `reports/neo4j_import.cypher` như phần Neo4j Desktop.

Nếu container đã tồn tại:

```bash
docker start neo4j-day19
```

## 8. NodeRAG

NodeRAG là phần nâng cấp tùy chọn. Bài hiện đã đủ bằng NetworkX vì đề cho phép chọn NetworkX, Neo4j hoặc NodeRAG.

Chỉ nên thử NodeRAG sau khi:

1. `python -B src/pipeline.py` chạy ổn.
2. `reports/triples.json` đã có.
3. `analysis/comparison_table.md` đã có kết quả.

Cài:

```bash
pip install noderag
```

Điểm nối với project hiện tại:

- Corpus: `data/tech_company_corpus.md`
- Triples: `reports/triples.json`
- Graph schema: xem `src/extract_triples.py` và `src/graph_builder.py`
- Benchmark: `data/benchmark_questions.json`

Vì NodeRAG có thể thay đổi API theo version, không nên buộc bài nộp phụ thuộc NodeRAG. Cách an toàn là giữ NetworkX làm bản chính, NodeRAG là phần demo nâng cấp nếu cài thành công.

## 9. Dùng phần nào từ Day18

Không copy nguyên Day18 sang Day19 vì Day18 có Qdrant, sentence-transformers, reranker, RAGAS và nhiều dependency nặng.

Base Day19 đã giữ lại các ý tưởng cần thiết:

| Day18 | Day19 tương ứng |
|---|---|
| `m1_chunking.py` | `src/corpus.py` |
| `m2_search.py` Flat RAG | `src/flat_rag.py` |
| `m4_eval.py` report/eval | `src/evaluate.py` |
| group/failure report | `analysis/final_report.md`, `analysis/comparison_table.md` |

Nếu muốn Flat RAG mạnh hơn, lúc đó mới copy `m2_search.py` và setup Qdrant từ Day18.

## 10. Lệnh kiểm tra nhanh

Offline:

```bash
python -B src/pipeline.py
```

OpenAI generate:

```bash
python -B src/pipeline.py
```

OpenAI extract:

```powershell
$env:USE_LLM_EXTRACTION="1"
python -B src/pipeline.py
```

Neo4j export:

```bash
python -B src/export_neo4j.py
```

Kiểm tra file kết quả:

```powershell
Get-ChildItem reports,figures,analysis
```
