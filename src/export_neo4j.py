"""Export Day19 triples to Neo4j Cypher.

Run after pipeline:
    python -B src/export_neo4j.py

Then paste reports/neo4j_import.cypher into Neo4j Browser, or run it with
cypher-shell when Neo4j is available.
"""

from __future__ import annotations

import json
import os
import re
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.paths import NEO4J_CYPHER_PATH, TRIPLES_REPORT_PATH


def cypher_escape(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("'", "\\'")


def label_for(node_type: str) -> str:
    label = re.sub(r"[^A-Za-z0-9_]", "", node_type or "Entity")
    if not label:
        return "Entity"
    return label[0].upper() + label[1:]


def relation_for(relation: str) -> str:
    rel = re.sub(r"[^A-Z0-9_]", "_", (relation or "RELATED_TO").upper())
    return rel or "RELATED_TO"


def generate_cypher(triples: list[dict]) -> str:
    lines = [
        "// Neo4j import script generated from Day19 GraphRAG triples",
        "// Safe to run multiple times because nodes and relationships use MERGE.",
        "",
        "CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;",
        "",
    ]

    for triple in triples:
        subject = cypher_escape(triple["subject"])
        obj = cypher_escape(triple["object"])
        source_id = cypher_escape(triple.get("source_id", "unknown"))
        confidence = float(triple.get("confidence", 1.0) or 1.0)
        subject_label = label_for(triple.get("subject_type", "Entity"))
        object_label = label_for(triple.get("object_type", "Entity"))
        relation = relation_for(triple.get("relation", "RELATED_TO"))

        lines.extend([
            f"MERGE (s:Entity:{subject_label} {{name: '{subject}'}})",
            f"  ON CREATE SET s.type = '{cypher_escape(triple.get('subject_type', 'Entity'))}'",
            f"MERGE (o:Entity:{object_label} {{name: '{obj}'}})",
            f"  ON CREATE SET o.type = '{cypher_escape(triple.get('object_type', 'Entity'))}'",
            f"MERGE (s)-[r:{relation}]->(o)",
            f"  ON CREATE SET r.sources = '{source_id}', r.confidence = {confidence}",
            f"  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS '{source_id}' THEN r.sources ELSE r.sources + ',' + '{source_id}' END;",
            "",
        ])
    return "\n".join(lines)


def main() -> None:
    if not TRIPLES_REPORT_PATH.exists():
        raise SystemExit(f"Missing {TRIPLES_REPORT_PATH}. Run python -B src/pipeline.py first.")
    triples = json.loads(TRIPLES_REPORT_PATH.read_text(encoding="utf-8"))
    NEO4J_CYPHER_PATH.parent.mkdir(parents=True, exist_ok=True)
    NEO4J_CYPHER_PATH.write_text(generate_cypher(triples), encoding="utf-8")
    print(f"Exported {len(triples)} triples to {NEO4J_CYPHER_PATH}")


if __name__ == "__main__":
    main()
