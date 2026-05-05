"""Build and export a NetworkX knowledge graph."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import asdict

import networkx as nx

from .extract_triples import Triple
from .paths import GRAPHML_PATH, GRAPH_STATS_PATH, GRAPH_FIGURE_PATH
from .schema import SYMMETRIC_RELATIONS, canonical_name


def deduplicate_triples(triples: list[Triple]) -> list[Triple]:
    merged: dict[tuple[str, str, str], Triple] = {}
    sources: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    confidences: dict[tuple[str, str, str], list[float]] = defaultdict(list)

    for triple in triples:
        subject = canonical_name(triple.subject)
        obj = canonical_name(triple.object)
        if subject == obj and triple.relation == "ALIAS_OF":
            continue
        key = (subject, triple.relation, obj)
        sources[key].add(triple.source_id)
        confidences[key].append(triple.confidence)
        if key not in merged:
            merged[key] = Triple(
                subject=subject,
                relation=triple.relation,
                object=obj,
                subject_type=triple.subject_type,
                object_type=triple.object_type,
                source_id=triple.source_id,
                confidence=triple.confidence,
            )

    result: list[Triple] = []
    for key, triple in merged.items():
        result.append(Triple(
            subject=triple.subject,
            relation=triple.relation,
            object=triple.object,
            subject_type=triple.subject_type,
            object_type=triple.object_type,
            source_id=",".join(sorted(sources[key])),
            confidence=round(sum(confidences[key]) / len(confidences[key]), 3),
        ))
    return sorted(result, key=lambda t: (t.subject, t.relation, t.object))


def build_graph(triples: list[Triple]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for triple in triples:
        for node, node_type in [(triple.subject, triple.subject_type), (triple.object, triple.object_type)]:
            if node not in graph:
                graph.add_node(node, name=node, type=node_type, sources=triple.source_id)
            else:
                existing = set(str(graph.nodes[node].get("sources", "")).split(","))
                existing.update(triple.source_id.split(","))
                graph.nodes[node]["sources"] = ",".join(sorted(s for s in existing if s))

        graph.add_edge(
            triple.subject,
            triple.object,
            key=triple.relation,
            relation=triple.relation,
            sources=triple.source_id,
            confidence=triple.confidence,
            weight=1,
        )
        if triple.relation in SYMMETRIC_RELATIONS:
            graph.add_edge(
                triple.object,
                triple.subject,
                key=triple.relation,
                relation=triple.relation,
                sources=triple.source_id,
                confidence=triple.confidence,
                weight=1,
            )
    return graph


def graph_stats(graph: nx.MultiDiGraph) -> dict:
    relation_counts = Counter(data["relation"] for _, _, data in graph.edges(data=True))
    type_counts = Counter(data.get("type", "Entity") for _, data in graph.nodes(data=True))
    top_nodes = sorted(graph.degree, key=lambda item: item[1], reverse=True)[:10]
    return {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "node_types": dict(type_counts),
        "relation_types": dict(relation_counts),
        "top_connected_nodes": [{"node": node, "degree": degree} for node, degree in top_nodes],
    }


def save_graph_outputs(graph: nx.MultiDiGraph) -> None:
    GRAPH_STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_STATS_PATH.write_text(json.dumps(graph_stats(graph), ensure_ascii=False, indent=2), encoding="utf-8")

    serializable = nx.MultiDiGraph()
    serializable.add_nodes_from(graph.nodes(data=True))
    for u, v, key, data in graph.edges(keys=True, data=True):
        serializable.add_edge(u, v, key=key, **{k: str(vv) for k, vv in data.items()})
    nx.write_graphml(serializable, GRAPHML_PATH)


def draw_graph(graph: nx.MultiDiGraph, path=GRAPH_FIGURE_PATH, max_nodes: int = 35) -> bool:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    nodes = [node for node, _ in sorted(graph.degree, key=lambda item: item[1], reverse=True)[:max_nodes]]
    subgraph = graph.subgraph(nodes).copy()
    pos = nx.spring_layout(subgraph, seed=42, k=0.8)
    type_palette = {
        "Company": "#4C78A8",
        "Person": "#F58518",
        "Product": "#54A24B",
        "Location": "#E45756",
        "Year": "#B279A2",
        "Sector": "#72B7B2",
    }
    colors = [type_palette.get(subgraph.nodes[n].get("type", "Entity"), "#9D9D9D") for n in subgraph.nodes]

    plt.figure(figsize=(18, 12))
    nx.draw_networkx_nodes(subgraph, pos, node_color=colors, node_size=950, alpha=0.9)
    nx.draw_networkx_edges(subgraph, pos, arrows=True, arrowstyle="-|>", arrowsize=12, alpha=0.35)
    nx.draw_networkx_labels(subgraph, pos, font_size=8)

    edge_labels = {}
    for u, v, data in subgraph.edges(data=True):
        edge_labels[(u, v)] = data.get("relation", "")
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=6)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return True


def triples_to_dicts(triples: list[Triple]) -> list[dict]:
    return [asdict(t) for t in triples]
