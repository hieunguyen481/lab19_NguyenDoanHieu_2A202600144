# Research Answers - Day 19

## 1. Entity Extraction

LLM phân biệt node và thuộc tính bằng cách dựa vào vai trò của thông tin trong câu. Node là thực thể có thể đứng trong nhiều quan hệ khác nhau, ví dụ `OpenAI`, `Sam Altman`, `ChatGPT`, `Microsoft`, `Azure`. Thuộc tính là thông tin mô tả node hoặc cạnh, ví dụ `source_id`, `confidence`, `node_type`, `năm thành lập`.

Trong pipeline này, các node chính gồm `Company`, `Person`, `Product`, `Location`, `Year`, `Sector`. Các quan hệ được giới hạn trong whitelist như `FOUNDED_BY`, `HAS_CEO`, `DEVELOPS`, `COMPETES_WITH`, `PARTNERS_WITH`.

## 2. Graph Construction và Deduplication

Deduplication quan trọng vì cùng một thực thể có thể xuất hiện dưới nhiều tên:

- `Amazon Web Services` và `AWS`
- `Microsoft Azure` và `Azure`
- `Llama models` và `Llama`

Nếu không gộp alias, graph sẽ bị tách thành nhiều node giả. Khi đó 2-hop traversal có thể bỏ sót cạnh quan trọng, làm GraphRAG trả lời thiếu thông tin.

Pipeline hiện dùng `canonical_name()` trong `src/graph_builder.py` để chuẩn hóa alias trước khi build graph.

## 3. BFS Graph Traversal vs Vector Search

Vector search tìm đoạn văn giống câu hỏi về mặt ngữ nghĩa. Cách này tốt cho câu hỏi có đáp án nằm trong một chunk rõ ràng, nhưng dễ yếu khi câu hỏi cần nối nhiều sự kiện ở nhiều đoạn khác nhau.

BFS graph traversal đi theo cạnh quan hệ trong graph. Ví dụ câu hỏi "Công ty nào do Sam Altman đồng sáng lập phát triển ChatGPT?" cần nối:

```text
Sam Altman <- FOUNDED_BY - OpenAI - DEVELOPS -> ChatGPT
```

Đây là dạng multi-hop mà GraphRAG xử lý tự nhiên hơn Flat RAG.

## 4. Lý do chọn NetworkX làm bản chính

NetworkX phù hợp cho bài lab vì:

1. Chạy offline và nhẹ.
2. Dễ debug node/edge/triples.
3. Dễ xuất ảnh graph bằng Matplotlib.
4. Không cần Neo4j Desktop, Docker hoặc NodeRAG ngay từ đầu.

Neo4j và NodeRAG được giữ làm hướng nâng cấp khi cần trực quan hóa hoặc tích hợp framework chuyên biệt.
