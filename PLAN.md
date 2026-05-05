# Kế hoạch Lab Day 19: GraphRAG với Tech Company Corpus

## 1. Tóm tắt yêu cầu

Lab Day 19 tiếp nối Day 18 bằng cách nâng cấp hệ thống Production RAG từ dạng truy xuất phẳng sang GraphRAG. Mục tiêu chính là xây dựng một pipeline có đủ các bước:

1. Chuẩn bị Tech Company Corpus.
2. Trích xuất thực thể và quan hệ thành triples.
3. Khử trùng lặp thực thể và chuẩn hóa quan hệ.
4. Xây dựng knowledge graph bằng NetworkX, tùy chọn Neo4j.
5. Truy vấn đa bước bằng 2-hop graph traversal.
6. So sánh Flat RAG và GraphRAG trên bộ benchmark 20 câu hỏi.
7. Báo cáo kết quả, hình ảnh đồ thị, chi phí token/thời gian.

## 2. Liên hệ với Day 18 và phần nên tái sử dụng

Folder `C403_D3_Day18` không tồn tại trong repo hiện tại. Folder phù hợp là `C401_D3_Day18`, và có thể tái sử dụng nhiều phần cho Day 19:

| Thành phần Day 18 | File | Cách dùng trong Day 19 |
|---|---|---|
| Load tài liệu và chunking | `C401_D3_Day18/src/m1_chunking.py` | Dùng lại `load_documents`, `chunk_structure_aware`, `chunk_hierarchical` để chia corpus trước khi trích xuất triples. |
| Flat RAG baseline | `C401_D3_Day18/src/m2_search.py` | Dùng lại BM25 + Dense + RRF làm hệ thống Flat RAG để so sánh với GraphRAG. |
| Reranking | `C401_D3_Day18/src/m3_rerank.py` | Có thể dùng lại để rerank context của Flat RAG; GraphRAG có thể rerank textualized graph context nếu cần. |
| Evaluation | `C401_D3_Day18/src/m4_eval.py` | Dùng lại format benchmark, report JSON, failure analysis; bổ sung metric riêng cho Flat RAG vs GraphRAG. |
| Báo cáo lỗi | `C401_D3_Day18/analysis/failure_analysis.md` | Dùng làm mẫu phân tích case Flat RAG bị thiếu context hoặc hallucinate. |
| Group report | `C401_D3_Day18/analysis/group_report.md` | Dùng làm mẫu bảng kết quả và phần findings. |

Không nên dùng lại trực tiếp corpus Day 18 vì Day 19 yêu cầu "Tech Company Corpus". Chỉ tái sử dụng kiến trúc pipeline, style report và các module kỹ thuật.

## 3. Kiến trúc đề xuất

Ưu tiên chọn **NetworkX** làm bản nộp chính vì chạy offline, dễ kiểm thử, dễ sinh ảnh bằng Matplotlib và không phụ thuộc Neo4j Desktop/Docker. Neo4j để ở mức tùy chọn mở rộng nếu còn thời gian.

Pipeline:

```text
Tech Company Corpus
    -> chunking
    -> LLM/rule-based triple extraction
    -> entity canonicalization + dedup
    -> NetworkX graph construction
    -> 2-hop graph retrieval
    -> textualized graph context
    -> LLM answer generation
    -> benchmark against Flat RAG baseline
```

## 4. Cấu trúc folder Day 19 cần hoàn thiện

```text
C401_D3_Day19/
├── Readme.md
├── PLAN.md
├── requirements.txt
├── .env.example
├── data/
│   ├── tech_company_corpus.md
│   └── benchmark_questions.json
├── src/
│   ├── __init__.py
│   ├── corpus.py
│   ├── extract_triples.py
│   ├── graph_builder.py
│   ├── graph_query.py
│   ├── flat_rag.py
│   ├── evaluate.py
│   └── pipeline.py
├── reports/
│   ├── graph_stats.json
│   ├── comparison_report.json
│   └── cost_report.json
├── figures/
│   └── knowledge_graph.png
└── analysis/
    ├── research_answers.md
    ├── comparison_table.md
    └── final_report.md
```

## 5. Kế hoạch triển khai chi tiết

### Giai đoạn 1: Research và thiết kế schema

Deliverable: `analysis/research_answers.md`

Nội dung cần trả lời:

1. **Entity Extraction:** Node là đối tượng có danh tính ổn định như công ty, người, sản phẩm, năm, tổ chức, địa điểm. Thuộc tính là thông tin mô tả node như năm thành lập, vai trò, lĩnh vực, trụ sở, mô tả ngắn.
2. **Deduplication:** Cần chuẩn hóa các tên như `Google`, `Google LLC`, `Alphabet's Google`; nếu không graph sẽ bị vỡ thành nhiều node giả và traversal trả context thiếu.
3. **BFS vs Vector Search:** BFS đi theo cạnh quan hệ rõ ràng trong graph nên tốt cho câu hỏi multi-hop; vector search tìm đoạn giống về ngữ nghĩa nên nhanh nhưng dễ bỏ sót quan hệ gián tiếp.

Schema đề xuất:

| Node type | Ví dụ |
|---|---|
| Company | OpenAI, Google, Microsoft, Nvidia |
| Person | Sam Altman, Elon Musk, Sundar Pichai |
| Product | ChatGPT, Azure, Gemini, CUDA |
| Organization | Alphabet, Y Combinator |
| Location | San Francisco, Mountain View |
| Year | 2015, 1998 |
| Sector | AI, cloud computing, semiconductor |

Quan hệ đề xuất:

| Relation | Ý nghĩa |
|---|---|
| `FOUNDED_BY` | Công ty được sáng lập bởi người nào |
| `FOUNDED_IN` | Công ty thành lập năm nào |
| `HEADQUARTERED_IN` | Trụ sở ở đâu |
| `CEO_OF` hoặc `HAS_CEO` | Quan hệ CEO và công ty |
| `OWNS` | Công ty mẹ sở hữu công ty/con |
| `DEVELOPS` | Công ty phát triển sản phẩm |
| `COMPETES_WITH` | Hai công ty cạnh tranh |
| `PARTNERS_WITH` | Quan hệ hợp tác |
| `OPERATES_IN` | Lĩnh vực hoạt động |

### Giai đoạn 2: Chuẩn bị dữ liệu

Deliverable: `data/tech_company_corpus.md`, `data/benchmark_questions.json`

Việc cần làm:

1. Tạo corpus khoảng 15-25 đoạn ngắn về các công ty công nghệ.
2. Ưu tiên thông tin có quan hệ chéo để GraphRAG phát huy tác dụng: founder, CEO, product, parent company, investment, partnership, competition.
3. Mỗi đoạn nên có `source_id` hoặc heading riêng để trace về nguồn.
4. Tạo 20 câu hỏi benchmark, trong đó có ít nhất 8 câu multi-hop.

Ví dụ câu hỏi multi-hop:

| Câu hỏi | Lý do phù hợp GraphRAG |
|---|---|
| Công ty nào do Sam Altman đồng sáng lập phát triển ChatGPT? | Cần nối Person -> Company -> Product. |
| CEO của công ty mẹ sở hữu Google là ai? | Cần Company -> Parent Company -> CEO. |
| Những công ty nào trong corpus cạnh tranh trong mảng AI assistant? | Cần gom quan hệ cạnh tranh + lĩnh vực/sản phẩm. |
| Công ty nào vừa hoạt động trong cloud computing vừa đầu tư mạnh vào AI? | Cần kết hợp nhiều cạnh `OPERATES_IN` và `DEVELOPS/INVESTS_IN`. |

### Giai đoạn 3: Triple extraction

Deliverable: `src/extract_triples.py`

Thiết kế:

1. Input: list chunks từ corpus.
2. Output: list triples dạng JSON:

```json
{
  "subject": "OpenAI",
  "relation": "FOUNDED_BY",
  "object": "Sam Altman",
  "subject_type": "Company",
  "object_type": "Person",
  "source_id": "doc_001",
  "confidence": 0.95
}
```

Ưu tiên triển khai hai chế độ:

1. `llm` mode: gọi OpenAI để extract triples theo schema cố định.
2. `fallback` mode: dùng rule-based corpus đã biết hoặc đọc file triples thủ công để vẫn chạy được khi không có API key.

Prompt cần ép model:

1. Chỉ dùng relation trong whitelist.
2. Không suy diễn ngoài văn bản.
3. Trả JSON hợp lệ.
4. Gắn `source_id` cho từng triple.
5. Nếu không chắc, bỏ qua thay vì bịa.

### Giai đoạn 4: Dedup và canonicalization

Deliverable: nằm trong `src/graph_builder.py`

Logic:

1. Chuẩn hóa tên: lowercase để so khớp, bỏ dấu câu dư, trim khoảng trắng.
2. Alias map thủ công cho các thực thể phổ biến:
   - `Google LLC` -> `Google`
   - `Alphabet Inc.` -> `Alphabet`
   - `OpenAI, Inc.` -> `OpenAI`
   - `Microsoft Corp.` -> `Microsoft`
3. Gộp node trùng theo canonical name.
4. Nếu cùng một cạnh xuất hiện nhiều lần, tăng `weight` hoặc lưu thêm `sources`.

Kết quả cần lưu:

1. `reports/graph_stats.json`: số node, số edge, số relation type, top connected nodes.
2. `reports/triples.json`: danh sách triples sau khi dedup.

### Giai đoạn 5: Graph construction và visualization

Deliverable: `src/graph_builder.py`, `figures/knowledge_graph.png`

NetworkX implementation:

1. Dùng `nx.MultiDiGraph()` để hỗ trợ nhiều loại cạnh giữa cùng hai node.
2. Node attributes: `name`, `type`, `aliases`, `sources`.
3. Edge attributes: `relation`, `sources`, `confidence`, `weight`.
4. Lưu graph ra `reports/knowledge_graph.gpickle` hoặc GraphML.
5. Vẽ graph bằng Matplotlib:
   - Màu node theo type.
   - Label node là canonical name.
   - Label edge là relation.
   - Nếu graph quá dày, vẽ subgraph top 25 nodes theo degree.

Neo4j tùy chọn:

1. Tạo script export Cypher.
2. Dùng `MERGE` cho node để tránh trùng.
3. Dùng `MERGE` hoặc `CREATE` cho relationships kèm `source_id`.

### Giai đoạn 6: Graph query và textualization

Deliverable: `src/graph_query.py`

Logic query:

1. Nhận câu hỏi.
2. Trích xuất entity chính bằng:
   - Exact match với canonical names.
   - Fuzzy match đơn giản nếu exact match không có.
   - Tùy chọn LLM entity extractor.
3. Với mỗi entity tìm được, BFS trong phạm vi 2-hop.
4. Gom triples liên quan.
5. Textualize thành context:

```text
OpenAI FOUNDED_BY Sam Altman.
OpenAI FOUNDED_BY Elon Musk.
OpenAI DEVELOPS ChatGPT.
ChatGPT OPERATES_IN Artificial Intelligence.
```

6. Gửi context cho LLM để trả lời, hoặc fallback bằng câu trả lời extractive nếu không có API key.

Tiêu chí query tốt:

1. Có trace: trả kèm triples/sources đã dùng.
2. Không dùng cạnh ngoài phạm vi 2-hop trừ khi cấu hình thay đổi.
3. Không trả lời nếu graph không có bằng chứng.

### Giai đoạn 7: Flat RAG baseline

Deliverable: `src/flat_rag.py`

Tái sử dụng Day 18:

1. Copy hoặc import logic chunking từ `C401_D3_Day18/src/m1_chunking.py`.
2. Tái sử dụng BM25/Dense/RRF từ `C401_D3_Day18/src/m2_search.py` nếu môi trường đã cài đủ.
3. Nếu Qdrant/Dense chưa chạy, dùng BM25 baseline để vẫn có kết quả so sánh tối thiểu.

Flat RAG flow:

```text
question -> chunk search -> top_k text chunks -> LLM/fallback answer
```

### Giai đoạn 8: Evaluation

Deliverable: `src/evaluate.py`, `reports/comparison_report.json`, `analysis/comparison_table.md`

Benchmark:

1. 20 câu hỏi theo đúng deliverables Day 19.
2. Mỗi câu có `question`, `ground_truth`, `answer_type`, `required_entities`, `required_relations`.
3. Chạy cả Flat RAG và GraphRAG.

Metric đề xuất:

| Metric | Cách tính |
|---|---|
| Exact/semantic correctness | Chấm thủ công hoặc LLM judge nếu có API key. |
| Context evidence score | Câu trả lời có dẫn được triple/source liên quan không. |
| Hallucination flag | Có thông tin không nằm trong context/triples không. |
| Retrieval coverage | GraphRAG có lấy đủ required relations không. |
| Latency | Thời gian trả lời mỗi câu. |
| Token usage | Prompt/completion tokens nếu dùng OpenAI. |

Bảng so sánh cần có:

| ID | Question | Ground truth | Flat RAG answer | GraphRAG answer | Winner | Note |
|---|---|---|---|---|---|---|

Cần ghi rõ các case Flat RAG sai nhưng GraphRAG đúng, đặc biệt với câu hỏi multi-hop.

### Giai đoạn 9: Final report

Deliverable: `analysis/final_report.md`

Cấu trúc báo cáo:

1. Mục tiêu và kiến trúc hệ thống.
2. Cách extract triples và schema graph.
3. Thống kê graph: số node, edge, relation type, top nodes.
4. Ảnh knowledge graph.
5. Bảng so sánh 20 câu hỏi Flat RAG vs GraphRAG.
6. Phân tích 3-5 failure cases.
7. Chi phí token và thời gian.
8. Kết luận: khi nào Flat RAG đủ, khi nào GraphRAG tốt hơn.

## 6. Phân công nhóm đề xuất

| Thành viên | Vai trò | Output |
|---|---|---|
| Thành viên 1 | Corpus + benchmark | `tech_company_corpus.md`, `benchmark_questions.json` |
| Thành viên 2 | Triple extraction | `extract_triples.py`, `triples.json` |
| Thành viên 3 | Graph construction + visualization | `graph_builder.py`, `knowledge_graph.png` |
| Thành viên 4 | Query engine + GraphRAG answer | `graph_query.py` |
| Thành viên 5 | Flat RAG + evaluation + report | `flat_rag.py`, `evaluate.py`, `final_report.md` |

Nếu nhóm có 4 người, gộp vai trò Corpus + Evaluation cho một người vì hai phần này liên kết chặt với benchmark.

## 7. Timeline 2 giờ trên lớp

| Thời gian | Việc cần làm |
|---|---|
| 0:00-0:15 | Đọc đề, thống nhất schema node/relation, chia task. |
| 0:15-0:35 | Chuẩn bị corpus và 20 benchmark questions. |
| 0:35-1:00 | Extract triples, dedup, build graph. |
| 1:00-1:20 | Implement graph traversal 2-hop và textualization. |
| 1:20-1:40 | Chạy Flat RAG baseline và GraphRAG trên benchmark. |
| 1:40-1:55 | Tạo graph image, comparison table, cost report. |
| 1:55-2:00 | Kiểm tra deliverables và chuẩn bị phần trình bày. |

## 8. Definition of Done

Day 19 được xem là hoàn thành khi có đủ:

1. Mã nguồn chạy được bằng một entry point như `python src/pipeline.py`.
2. Tech Company Corpus rõ ràng, có dữ liệu đủ quan hệ multi-hop.
3. Ít nhất 20 câu hỏi benchmark.
4. File triples sau dedup.
5. Knowledge graph NetworkX có node/edge attributes.
6. Ảnh graph trong `figures/knowledge_graph.png`.
7. Bảng so sánh Flat RAG vs GraphRAG trên 20 câu hỏi.
8. Ghi nhận case Flat RAG hallucinate hoặc thiếu context nhưng GraphRAG đúng.
9. Báo cáo token usage và thời gian chạy.
10. Final report ngắn gọn, có nhận xét kỹ thuật rõ ràng.

## 9. Rủi ro và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Không có API key OpenAI | Dùng triples thủ công/rule-based fallback, answer extractive từ graph context. |
| NodeRAG cài đặt lỗi | Chọn NetworkX làm implementation chính. |
| Neo4j mất thời gian setup | Chỉ export Cypher, không bắt buộc chạy Neo4j. |
| Flat RAG phụ thuộc Qdrant | Dùng BM25 baseline trước, Dense/Qdrant là nâng cấp. |
| Graph quá rối khi vẽ | Vẽ subgraph top nodes hoặc subgraph quanh query examples. |
| LLM extract sai JSON | Validate JSON, retry một lần, fallback sang parser thủ công. |

## 10. Ưu tiên triển khai

1. Bắt buộc: NetworkX graph, triples, 2-hop query, benchmark 20 câu, comparison table.
2. Nên có: LLM extraction, cost report, graph visualization đẹp.
3. Tùy chọn: Neo4j export, NodeRAG thử nghiệm, RAGAS/LLM judge nâng cao.

