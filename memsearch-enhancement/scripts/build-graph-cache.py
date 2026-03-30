#!/usr/bin/env python3
"""
build-graph-cache.py — Build knowledge-graph.json from entities.md and relations.md.

Reads:
  ~/.claude/MEMORY/GRAPH/entities.md
  ~/.claude/MEMORY/GRAPH/relations.md

Writes:
  ~/.claude/.memsearch/knowledge-graph.json

Entity hash = first 12 chars of SHA-256 of lowercase entity name.

Format expected in entities.md:
  ## Entity Name
  - type: project|tool|pattern|concept
  - projects: A, B, C
  - first_seen: YYYY-MM-DD
  - last_seen: YYYY-MM-DD

Format expected in relations.md:
  ## EntityA ←relation→ EntityB
  - reason: ...
  - evidence: ...
"""

import hashlib
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HOME = Path.home()
ENTITIES_MD  = HOME / ".claude" / "MEMORY" / "GRAPH" / "entities.md"
RELATIONS_MD = HOME / ".claude" / "MEMORY" / "GRAPH" / "relations.md"
OUTPUT_JSON  = HOME / ".claude" / ".memsearch" / "knowledge-graph.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def entity_hash(name: str) -> str:
    """Return first 12 hex chars of SHA-256 of lowercase entity name."""
    return hashlib.sha256(name.lower().encode("utf-8")).hexdigest()[:12]


def parse_kv_block(lines: list[str]) -> dict:
    """Parse a block of '- key: value' lines into a dict. Skips comments and blanks."""
    result = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("<!--") or line.startswith("---"):
            continue
        # Match lines like:  - key: value  or  - key: value with spaces
        m = re.match(r"^-\s+(\w[\w_-]*):\s*(.*)", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            result[key] = val
    return result


def parse_entities(path: Path) -> dict:
    """
    Parse entities.md.
    Returns dict keyed by entity_hash: {name, type, projects, first_seen, last_seen, ...}
    """
    if not path.exists():
        print(f"[build-graph-cache] WARNING: {path} not found — skipping entities.", file=sys.stderr)
        return {}

    entities = {}
    current_name = None
    current_lines = []

    def flush(name, lines):
        if not name:
            return
        kv = parse_kv_block(lines)
        h = entity_hash(name)
        projects_raw = kv.get("projects", "")
        projects = [p.strip() for p in projects_raw.split(",") if p.strip()] if projects_raw else []
        entities[h] = {
            "name":       name,
            "type":       kv.get("type", ""),
            "projects":   projects,
            "first_seen": kv.get("first_seen", ""),
            "last_seen":  kv.get("last_seen", ""),
            "description": kv.get("description", ""),
        }

    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        # Heading lines: ## Some Entity Name
        m = re.match(r"^##\s+(.+)", line)
        if m:
            flush(current_name, current_lines)
            current_name = m.group(1).strip()
            current_lines = []
        else:
            if current_name is not None:
                current_lines.append(line)

    flush(current_name, current_lines)
    return entities


def parse_relations(path: Path, entities: dict) -> list:
    """
    Parse relations.md.
    Returns list of edge dicts.
    Supports both arrow formats:
      ## EntityA ←relation→ EntityB    (canonical)
      ## EntityA → EntityB             (legacy, no relation type)
      ## EntityA →[relation]→ EntityB  (alternative)
    """
    if not path.exists():
        print(f"[build-graph-cache] WARNING: {path} not found — skipping relations.", file=sys.stderr)
        return []

    # Build name → hash lookup (case-insensitive)
    name_to_hash = {v["name"].lower(): k for k, v in entities.items()}

    def lookup_hash(name: str):
        name = name.strip()
        h = name_to_hash.get(name.lower())
        if h is None:
            # Not in entities yet — generate a hash anyway so the edge is preserved
            h = entity_hash(name)
        return h, name

    edges = []
    current_heading = None
    current_lines = []

    def flush(heading, lines):
        if not heading:
            return
        # Pattern 1: ## EntityA ←relation→ EntityB
        m = re.match(r"^(.+?)\s+←([^→]+)→\s+(.+)$", heading)
        if m:
            src_name  = m.group(1).strip()
            relation  = m.group(2).strip()
            tgt_name  = m.group(3).strip()
        else:
            # Pattern 2: ## EntityA → EntityB  (legacy)
            m2 = re.match(r"^(.+?)\s+→\s+(.+)$", heading)
            if m2:
                src_name = m2.group(1).strip()
                tgt_name = m2.group(2).strip()
                relation = "applies_to"
            else:
                # Unrecognised heading format — skip
                return

        kv = parse_kv_block(lines)
        src_hash, src_name = lookup_hash(src_name)
        tgt_hash, tgt_name = lookup_hash(tgt_name)

        # Prefer 'relation' key in body over heading-parsed relation
        relation = kv.get("relation", relation)

        edges.append({
            "source_hash": src_hash,
            "source_name": src_name,
            "target_hash": tgt_hash,
            "target_name": tgt_name,
            "relation":    relation,
            "reason":      kv.get("reason", ""),
            "evidence":    kv.get("evidence", kv.get("first_seen", "")),
        })

    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+)", line)
        if m:
            flush(current_heading, current_lines)
            current_heading = m.group(1).strip()
            current_lines = []
        else:
            if current_heading is not None:
                current_lines.append(line)

    flush(current_heading, current_lines)
    return edges


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    entities = parse_entities(ENTITIES_MD)
    edges    = parse_relations(RELATIONS_MD, entities)

    graph = {
        "entities": entities,
        "edges":    edges,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"[build-graph-cache] Written {OUTPUT_JSON}: "
        f"{len(entities)} entities, {len(edges)} edges."
    )


if __name__ == "__main__":
    main()
