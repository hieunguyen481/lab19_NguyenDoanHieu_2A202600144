# Báo cáo Lab Day 19 - GraphRAG

## 1. Mục tiêu

Xây dựng hệ thống GraphRAG trên Tech Company Corpus, sau đó so sánh với Flat RAG baseline trên 20 câu hỏi benchmark. Hệ thống tập trung vào các câu hỏi cần nối nhiều quan hệ như founder -> company -> product hoặc company -> parent company -> CEO.

## 2. Kiến trúc

Pipeline gồm các bước: load corpus, chunk documents, extract triples, deduplicate entities, build NetworkX graph, truy vấn graph 2-hop, chạy Flat RAG baseline, rồi đánh giá hai hệ thống.

## 3. Thống kê graph

- Nodes: 67
- Edges: 94
- Node types: {'Product': 22, 'Company': 13, 'Person': 16, 'Location': 9, 'Year': 4, 'Sector': 3}
- Relation types: {'COMPETES_WITH': 20, 'PARTNERS_WITH': 8, 'HAS_CEO': 9, 'PARENT_OF': 1, 'DEVELOPS': 21, 'FOUNDED_BY': 12, 'FOUNDED_IN': 3, 'HEADQUARTERED_IN': 10, 'INVESTS_IN': 3, 'OPERATES': 1, 'OPERATES_IN': 4, 'ACQUIRED': 1, 'ACQUIRED_IN': 1}
- Ảnh graph: figures/knowledge_graph.png

## 4. Kết quả benchmark

- Số câu hỏi: 20
- Flat RAG average score: 0.903
- GraphRAG average score: 1.0
- GraphRAG thắng: 11
- Flat RAG thắng: 0
- Hòa: 9

## 5. Một số case GraphRAG tốt hơn

- `q01`: Công ty nào do Sam Altman đồng sáng lập phát triển ChatGPT? (Flat=0.85, GraphRAG=1.0)
- `q02`: Công ty mẹ của Google là công ty nào và CEO là ai? (Flat=0.7, GraphRAG=1.0)
- `q03`: Những công ty nào cạnh tranh với OpenAI trong mảng AI assistant? (Flat=0.86, GraphRAG=1.0)
- `q05`: CEO của Nvidia là ai và Nvidia phát triển nền tảng nào cho AI computing? (Flat=0.85, GraphRAG=1.0)
- `q07`: Công ty nào phát triển Claude và được Amazon cùng Google đầu tư? (Flat=0.85, GraphRAG=1.0)

## 6. Nhận xét

GraphRAG mạnh hơn ở các câu hỏi cần nối nhiều quan hệ như founder -> company -> product, company -> parent company -> CEO, hoặc competition giữa các sản phẩm/công ty. Flat RAG có thể đủ cho câu hỏi nằm gọn trong một đoạn văn, nhưng dễ thiếu bằng chứng quan hệ khi thông tin phân tán.

## 7. Chi phí

Chi phí token/time chi tiết nằm trong `reports/cost_report.json`. Khi chạy offline không có `OPENAI_API_KEY`, token usage bằng 0 vì hệ thống dùng seed triples và fallback answers.
