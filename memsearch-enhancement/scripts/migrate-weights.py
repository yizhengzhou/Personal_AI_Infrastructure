#!/usr/bin/env python3
"""One-time migration: seed chunk-weights.json from algorithm-reflections.jsonl."""

import json
import os
import subprocess
import sys
from pathlib import Path

REFLECTIONS_PATH = Path.home() / ".claude" / "MEMORY" / "LEARNING" / "REFLECTIONS" / "algorithm-reflections.jsonl"
WEIGHTS_PATH = Path.home() / ".claude" / ".memsearch" / "chunk-weights.json"
MEMSEARCH_DIR = Path.home() / ".claude" / ".memsearch" / "memory"

def load_weights():
    try:
        with open(WEIGHTS_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_weights(weights):
    with open(WEIGHTS_PATH, "w") as f:
        json.dump(weights, f, indent=2, ensure_ascii=False)

def search_memsearch(query, collection=None):
    """Search memsearch and return chunk hashes."""
    cmd = ["memsearch", "search", query, "--top-k", "3", "--json-output"]
    if collection:
        cmd.extend(["--collection", collection])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return [r.get("chunk_hash", "") for r in data if r.get("chunk_hash")]
    except Exception:
        pass
    return []

def derive_collection():
    """Get the collection name for ~/.claude project."""
    script = Path.home() / ".claude" / "plugins" / "marketplaces" / "memsearch-plugins" / "ccplugin" / "scripts" / "derive-collection.sh"
    if not script.exists():
        return None
    try:
        result = subprocess.run(
            ["bash", str(script), str(Path.home() / ".claude")],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None

def main():
    if not REFLECTIONS_PATH.exists():
        print("No reflections file found, nothing to migrate.", file=sys.stderr)
        return

    weights = load_weights()
    collection = derive_collection()

    # Read all reflections
    reflections = []
    with open(REFLECTIONS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                reflections.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    print(f"Found {len(reflections)} reflections", file=sys.stderr)

    migrated = 0
    for ref in reflections:
        prd_id = ref.get("prd_id", "")
        sentiment = ref.get("implied_sentiment", 5)
        task_desc = ref.get("task_description", "")

        if not prd_id and not task_desc:
            continue

        # Search for chunks related to this PRD
        query = prd_id if prd_id else task_desc
        hashes = search_memsearch(query, collection)

        if not hashes:
            # Try with task description
            if task_desc and query != task_desc:
                hashes = search_memsearch(task_desc, collection)

        sentiment_normalized = sentiment / 10.0

        for h in hashes:
            if h not in weights:
                weights[h] = {
                    "access_count": 0,
                    "last_accessed": "",
                    "usefulness_sum": 0.0,
                    "usefulness_count": 0,
                    "sentiment_boost": 0.0,
                }
            # Use max sentiment if multiple reflections point to same chunk
            weights[h]["sentiment_boost"] = max(
                weights[h]["sentiment_boost"], sentiment_normalized
            )
            migrated += 1

    save_weights(weights)
    print(f"Migrated {migrated} chunk-sentiment links from {len(reflections)} reflections", file=sys.stderr)

if __name__ == "__main__":
    main()
