#!/usr/bin/env python3
"""
extract-entities.py — Extract entities from the latest daily memory entry
and append them to the knowledge graph markdown files.

Steps:
  1. Find today's memory file in ~/.claude/.memsearch/memory/ or fallback path.
  2. Extract the last section (after the last ### HH:MM heading).
  3. Call claude via subprocess to extract entities/relations as JSON.
  4. Update ~/.claude/MEMORY/GRAPH/entities.md and relations.md.
  5. Call build-graph-cache.py to rebuild the JSON cache.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

TODAY = date.today().strftime("%Y-%m-%d")

MEMSEARCH_MEMORY = Path.home() / ".claude" / ".memsearch" / "memory" / f"{TODAY}.md"
FALLBACK_MEMORY  = None  # Set dynamically based on your Claude Code project path

GRAPH_DIR     = Path.home() / ".claude" / "MEMORY" / "GRAPH"
ENTITIES_MD   = GRAPH_DIR / "entities.md"
RELATIONS_MD  = GRAPH_DIR / "relations.md"

BUILD_CACHE   = Path.home() / ".claude" / ".memsearch" / "scripts" / "build-graph-cache.py"

# ---------------------------------------------------------------------------
# System prompt for entity extraction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are an entity extractor. Given a session summary, extract entities "
    "(projects, tools, patterns, concepts) and relationships between them.\n\n"
    "Output ONLY valid JSON, nothing else:\n"
    '{"entities": [{"name": "EntityName", "type": "project|tool|pattern|concept"}], '
    '"relations": [{"source": "EntityA", "target": "EntityB", '
    '"relation": "applies_to|similar_to|depends_on|evolved_from", "reason": "short reason"}]}\n\n'
    "Rules:\n"
    "- Entity names should be canonical (e.g., \"Playwright\" not \"playwright testing\")\n"
    "- Only extract entities that are meaningful and specific\n"
    "- Relations should only be included if clearly evidenced in the text\n"
    '- If nothing meaningful found, return {"entities": [], "relations": []}'
)


# ---------------------------------------------------------------------------
# Step 1: Find today's memory file
# ---------------------------------------------------------------------------

def find_memory_file():
    if MEMSEARCH_MEMORY.exists():
        return MEMSEARCH_MEMORY
    if FALLBACK_MEMORY.exists():
        return FALLBACK_MEMORY
    return None


# ---------------------------------------------------------------------------
# Step 2: Extract last section
# ---------------------------------------------------------------------------

def extract_last_section(text):
    """Return the content after the last ### HH:MM heading, or None."""
    # Match headings like ### 02:34 or ### 14:07
    pattern = re.compile(r"^### \d{2}:\d{2}\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return None
    last_match = matches[-1]
    return text[last_match.end():].strip()


# ---------------------------------------------------------------------------
# Step 3: Call claude to extract entities
# ---------------------------------------------------------------------------

def call_claude(content):
    """Call claude -p with the given content via stdin. Return parsed JSON or None."""
    cmd = [
        "claude",
        "-p",
        "--model", "haiku",
        "--no-session-persistence",
        "--system-prompt", SYSTEM_PROMPT,
    ]
    try:
        result = subprocess.run(
            cmd,
            input=content,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        print("extract-entities: 'claude' command not found in PATH", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("extract-entities: claude timed out after 120s", file=sys.stderr)
        return None
    except Exception as exc:
        print(f"extract-entities: subprocess error: {exc}", file=sys.stderr)
        return None

    if result.returncode != 0:
        print(
            f"extract-entities: claude exited {result.returncode}: {result.stderr.strip()}",
            file=sys.stderr,
        )
        return None

    raw = result.stdout.strip()
    if not raw:
        print("extract-entities: claude returned empty response", file=sys.stderr)
        return None

    # Strip markdown code fences if claude wraps JSON in them
    fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", raw, re.DOTALL)
    if fenced:
        raw = fenced.group(1).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"extract-entities: malformed JSON from claude: {exc}", file=sys.stderr)
        print(f"extract-entities: raw response was: {result.stdout[:500]}", file=sys.stderr)
        return None

    return data


# ---------------------------------------------------------------------------
# Step 4: Ensure GRAPH directory and markdown files exist
# ---------------------------------------------------------------------------

def ensure_graph_files():
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    if not ENTITIES_MD.exists():
        ENTITIES_MD.write_text(
            "# Entity Graph\n\n"
            "<!-- Auto-managed by extract-entities.py — do not edit headings manually -->\n\n",
            encoding="utf-8",
        )
    if not RELATIONS_MD.exists():
        RELATIONS_MD.write_text(
            "# Relation Graph\n\n"
            "<!-- Auto-managed by extract-entities.py — do not edit headings manually -->\n\n",
            encoding="utf-8",
        )


# ---------------------------------------------------------------------------
# Step 5: Update entities.md
# ---------------------------------------------------------------------------

def load_existing_entity_names(text):
    """Return a dict mapping lowercase name -> original heading line."""
    names = {}
    for match in re.finditer(r"^## (.+)$", text, re.MULTILINE):
        heading = match.group(1).strip()
        names[heading.lower()] = heading
    return names


def update_entities(entities):
    """Upsert each entity into ENTITIES_MD."""
    if not entities:
        return

    text = ENTITIES_MD.read_text(encoding="utf-8")
    existing = load_existing_entity_names(text)
    additions = []

    for entity in entities:
        name = entity.get("name", "").strip()
        etype = entity.get("type", "concept").strip()
        if not name:
            continue

        name_lower = name.lower()
        if name_lower in existing:
            # Update last_seen for the existing entry
            heading = existing[name_lower]
            # Replace last_seen line if present; otherwise leave it
            old_block_pattern = re.compile(
                r"(^## " + re.escape(heading) + r"\s*\n)(.*?)(?=^## |\Z)",
                re.MULTILINE | re.DOTALL,
            )
            def update_last_seen(m):
                block_header = m.group(1)
                block_body = m.group(2)
                if "- last_seen:" in block_body:
                    block_body = re.sub(
                        r"- last_seen: \S+",
                        f"- last_seen: {TODAY}",
                        block_body,
                    )
                else:
                    block_body = block_body.rstrip("\n") + f"\n- last_seen: {TODAY}\n\n"
                return block_header + block_body

            text = old_block_pattern.sub(update_last_seen, text, count=1)
        else:
            # New entity — queue for appending
            additions.append(
                f"## {name}\n"
                f"- type: {etype}\n"
                f"- first_seen: {TODAY}\n"
                f"- last_seen: {TODAY}\n\n"
            )
            existing[name_lower] = name

    if additions:
        text = text.rstrip("\n") + "\n\n" + "\n".join(additions)

    ENTITIES_MD.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 6: Update relations.md
# ---------------------------------------------------------------------------

def load_existing_relations(text):
    """Return a set of (source_lower, target_lower, relation_lower) tuples."""
    relations = set()
    # Each relation block looks like:
    # ## Source → Target
    # - relation: ...
    for match in re.finditer(r"^## (.+?) → (.+)$", text, re.MULTILINE):
        src = match.group(1).strip().lower()
        tgt = match.group(2).strip().lower()
        # Find relation line immediately after
        pos = match.end()
        rel_match = re.search(r"- relation: (\S+)", text[pos:pos + 200])
        rel = rel_match.group(1).lower() if rel_match else ""
        relations.add((src, tgt, rel))
    return relations


def update_relations(relations):
    """Append each new relation to RELATIONS_MD."""
    if not relations:
        return

    text = RELATIONS_MD.read_text(encoding="utf-8")
    existing = load_existing_relations(text)
    additions = []

    for rel in relations:
        source = rel.get("source", "").strip()
        target = rel.get("target", "").strip()
        relation = rel.get("relation", "").strip()
        reason = rel.get("reason", "").strip()
        if not source or not target or not relation:
            continue

        key = (source.lower(), target.lower(), relation.lower())
        if key not in existing:
            additions.append(
                f"## {source} → {target}\n"
                f"- relation: {relation}\n"
                f"- reason: {reason}\n"
                f"- first_seen: {TODAY}\n\n"
            )
            existing.add(key)

    if additions:
        text = text.rstrip("\n") + "\n\n" + "\n".join(additions)
        RELATIONS_MD.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Step 7: Rebuild JSON cache
# ---------------------------------------------------------------------------

def rebuild_cache():
    if not BUILD_CACHE.exists():
        # Script not yet present — skip silently
        return
    try:
        result = subprocess.run(
            ["python3", str(BUILD_CACHE)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(
                f"extract-entities: build-graph-cache exited {result.returncode}: "
                f"{result.stderr.strip()}",
                file=sys.stderr,
            )
    except subprocess.TimeoutExpired:
        print("extract-entities: build-graph-cache timed out", file=sys.stderr)
    except Exception as exc:
        print(f"extract-entities: error calling build-graph-cache: {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Step 1: Find memory file
    memory_file = find_memory_file()
    if memory_file is None:
        # No today's file — exit silently
        sys.exit(0)

    # Step 2: Extract last section
    try:
        text = memory_file.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"extract-entities: could not read {memory_file}: {exc}", file=sys.stderr)
        sys.exit(0)

    last_section = extract_last_section(text)
    if not last_section:
        sys.exit(0)

    # Step 3: Call claude
    data = call_claude(last_section)
    if data is None:
        sys.exit(0)

    entities  = data.get("entities", [])
    relations = data.get("relations", [])

    if not entities and not relations:
        sys.exit(0)

    # Step 4: Ensure graph files exist
    ensure_graph_files()

    # Step 5: Update entities
    try:
        update_entities(entities)
    except Exception as exc:
        print(f"extract-entities: error updating entities.md: {exc}", file=sys.stderr)

    # Step 6: Update relations
    try:
        update_relations(relations)
    except Exception as exc:
        print(f"extract-entities: error updating relations.md: {exc}", file=sys.stderr)

    # Step 7: Rebuild cache
    rebuild_cache()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"extract-entities: unexpected error: {exc}", file=sys.stderr)
        sys.exit(0)
