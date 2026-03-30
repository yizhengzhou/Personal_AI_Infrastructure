#!/usr/bin/env python3
"""
query-graph.py — Query the memsearch knowledge graph by entity name.

Usage:
    python3 query-graph.py "search query"

Output (JSON to stdout):
    {"matched_entities": [{"name": "X", "type": "tool", "related": [{"name": "Y", "relation": "applies_to"}]}]}
"""

import sys
import json
import os

GRAPH_PATH = os.path.expanduser("~/.claude/.memsearch/knowledge-graph.json")


def load_graph():
    if not os.path.exists(GRAPH_PATH):
        return None
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def match_entities(graph, query):
    """Case-insensitive substring match against entity names."""
    query_lower = query.lower()
    entities = graph.get("entities", {})
    matched = []
    # entities is a dict: {hash: {name, type, ...}}
    for _hash, entity in entities.items():
        if not isinstance(entity, dict):
            continue
        name = entity.get("name", "")
        if query_lower in name.lower():
            matched.append(entity)
    return matched


def find_related(graph, entity_name):
    """Follow 1-hop edges from the matched entity."""
    edges = graph.get("edges", [])
    # Build name lookup from entities dict
    entities = graph.get("entities", {})
    hash_to_name = {}
    for _h, e in entities.items():
        if isinstance(e, dict):
            hash_to_name[_h] = e.get("name", "")
    related = []
    seen = set()
    for edge in edges:
        src_name = edge.get("source_name", edge.get("source", ""))
        tgt_name = edge.get("target_name", edge.get("target", ""))
        rel = edge.get("relation", "")
        if src_name == entity_name and tgt_name not in seen:
            seen.add(tgt_name)
            related.append({"name": tgt_name, "relation": rel})
        elif tgt_name == entity_name and src_name not in seen:
            seen.add(src_name)
            related.append({"name": src_name, "relation": rel})
    return related


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"matched_entities": []}))
        sys.exit(0)

    query = sys.argv[1]

    graph = load_graph()
    if graph is None:
        print(json.dumps({"matched_entities": []}))
        sys.exit(0)

    matched_entities = match_entities(graph, query)

    if not matched_entities:
        print(json.dumps({"matched_entities": []}))
        sys.exit(0)

    result = []
    for entity in matched_entities:
        name = entity.get("name", "")
        entity_type = entity.get("type", "")
        related = find_related(graph, name)
        result.append({
            "name": name,
            "type": entity_type,
            "related": related,
        })

    print(json.dumps({"matched_entities": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
