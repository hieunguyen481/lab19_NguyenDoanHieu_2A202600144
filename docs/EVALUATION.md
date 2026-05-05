# Evaluation Notes

## Benchmark

Benchmark nằm ở `data/benchmark_questions.json`, gồm 20 câu hỏi. Mỗi câu có:

- `id`
- `question`
- `ground_truth`
- `required_entities`
- `required_relations`

Các trường `required_entities` và `required_relations` giúp chấm tự động xem câu trả lời/context có chứa đủ bằng chứng cần thiết hay không.

## Flat RAG baseline

Flat RAG dùng `src/flat_rag.py`. Đây là baseline lexical retrieval nhẹ:

```text
question -> lexical search over chunks -> top contexts -> answer
```

Nếu có OpenAI API key, answer được sinh từ context. Nếu không có key, hệ thống fallback bằng context liên quan nhất.

## GraphRAG

GraphRAG dùng `src/graph_query.py`:

```text
question -> entity matching -> 2-hop graph traversal -> textualized triples -> answer
```

Context của GraphRAG là các triples có source, ví dụ:

```text
- OpenAI FOUNDED_BY Sam Altman (source: doc_001)
- OpenAI DEVELOPS ChatGPT (source: doc_001)
```

## Scoring

`src/evaluate.py` dùng heuristic score:

- 70% dựa trên required entities.
- 30% dựa trên required relations trong evidence/context.

Điểm này không thay thế human evaluation hoặc RAGAS, nhưng đủ minh họa sự khác biệt giữa Flat RAG và GraphRAG trong bài lab.

## Output

| File | Nội dung |
|---|---|
| `reports/comparison_report.json` | Toàn bộ kết quả chi tiết. |
| `analysis/comparison_table.md` | Bảng markdown dễ đọc. |
| `analysis/final_report.md` | Báo cáo tóm tắt để nộp. |
