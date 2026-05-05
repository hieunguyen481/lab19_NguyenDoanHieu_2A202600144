"""Import Day19 GraphRAG triples into a running Neo4j database.

Prerequisites:
    pip install -r requirements.txt

Environment variables are loaded from .env:
    NEO4J_URI=bolt://localhost:7687
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=password

Run:
    python -B src/import_neo4j.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict

if __package__ in {None, ""}:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.env import load_environment
from src.paths import TRIPLES_REPORT_PATH


def label_for(node_type: str) -> str:
    label = re.sub(r"[^A-Za-z0-9_]", "", node_type or "Entity")
    if not label:
        return "Entity"
    return label[0].upper() + label[1:]


def relation_for(relation: str) -> str:
    rel = re.sub(r"[^A-Z0-9_]", "_", (relation or "RELATED_TO").upper())
    return rel or "RELATED_TO"


def grouped_triples(triples: list[dict]) -> dict[tuple[str, str, str], list[dict]]:
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for triple in triples:
        key = (
            label_for(triple.get("subject_type", "Entity")),
            label_for(triple.get("object_type", "Entity")),
            relation_for(triple.get("relation", "RELATED_TO")),
        )
        groups[key].append({
            "subject": triple["subject"],
            "object": triple["object"],
            "subject_type": triple.get("subject_type", "Entity"),
            "object_type": triple.get("object_type", "Entity"),
            "source_id": triple.get("source_id", "unknown"),
            "confidence": float(triple.get("confidence", 1.0) or 1.0),
        })
    return groups


def merge_triple_batch(tx, subject_label: str, object_label: str, relation: str, rows: list[dict]) -> None:
    query = f"""
    UNWIND $rows AS row
    WITH row
    MERGE (s:Entity:{subject_label} {{name: row.subject}})
      ON CREATE SET s.type = row.subject_type
      ON MATCH SET s.type = coalesce(s.type, row.subject_type)
    MERGE (o:Entity:{object_label} {{name: row.object}})
      ON CREATE SET o.type = row.object_type
      ON MATCH SET o.type = coalesce(o.type, row.object_type)
    MERGE (s)-[r:{relation}]->(o)
      ON CREATE SET r.sources = row.source_id, r.confidence = row.confidence
      ON MATCH SET
        r.sources = CASE
          WHEN r.sources CONTAINS row.source_id THEN r.sources
          ELSE r.sources + ',' + row.source_id
        END,
        r.confidence = coalesce(r.confidence, row.confidence)
    """
    tx.run(query, rows=rows).consume()


def main() -> None:
    load_environment()
    if not TRIPLES_REPORT_PATH.exists():
        raise SystemExit(f"Missing {TRIPLES_REPORT_PATH}. Run python -B src/pipeline.py first.")

    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    if not password:
        raise SystemExit("Missing NEO4J_PASSWORD. Add it to .env before importing.")

    try:
        from neo4j import GraphDatabase
        from neo4j.exceptions import AuthError, ServiceUnavailable
    except ImportError as exc:
        raise SystemExit("Missing neo4j package. Run: pip install -r requirements.txt") from exc

    triples = json.loads(TRIPLES_REPORT_PATH.read_text(encoding="utf-8"))
    driver = GraphDatabase.driver(uri, auth=(username, password), connection_timeout=20)

    try:
        with driver:
            print(f"Connecting to Neo4j at {uri}...")
            driver.verify_connectivity()
            groups = grouped_triples(triples)
            imported = 0
            with driver.session() as session:
                session.run(
                    "CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE"
                ).consume()
                for (subject_label, object_label, relation), rows in sorted(groups.items()):
                    session.execute_write(merge_triple_batch, subject_label, object_label, relation, rows)
                    imported += len(rows)
                    print(f"  imported {imported}/{len(triples)} triples")
    except ServiceUnavailable as exc:
        raise SystemExit(
            f"Cannot connect to Neo4j at {uri}. Start Neo4j Desktop/Docker first, "
            "then check NEO4J_URI in .env."
        ) from exc
    except AuthError as exc:
        raise SystemExit("Neo4j authentication failed. Check NEO4J_USERNAME and NEO4J_PASSWORD in .env.") from exc

    print(f"Imported {len(triples)} triples into Neo4j at {uri}")


if __name__ == "__main__":
    main()
