#!/usr/bin/env python3
"""Link a sentiment score from algorithm reflection to related chunks."""

import json
import subprocess
import sys
from pathlib import Path

WEIGHTS_PATH = Path.home() / ".claude" / ".memsearch" / "chunk-weights.json"

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--prd-id", required=True)
    parser.add_argument("--sentiment", type=float, required=True)
    parser.add_argument("--collection", default=None)
    args = parser.parse_args()

    # Load weights
    try:
        with open(WEIGHTS_PATH) as f:
            weights = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        weights = {}

    sentiment_normalized = args.sentiment / 10.0

    # Search for chunks mentioning this PRD
    cmd = ["memsearch", "search", args.prd_id, "--top-k", "5", "--json-output"]
    if args.collection:
        cmd.extend(["--collection", args.collection])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0 or not result.stdout.strip():
            return
        data = json.loads(result.stdout)
    except Exception:
        return

    linked = 0
    for r in data:
        h = r.get("chunk_hash", "")
        if not h:
            continue
        if h not in weights:
            weights[h] = {
                "access_count": 0,
                "last_accessed": "",
                "usefulness_sum": 0.0,
                "usefulness_count": 0,
                "sentiment_boost": 0.0,
            }
        weights[h]["sentiment_boost"] = max(
            weights[h]["sentiment_boost"], sentiment_normalized
        )
        linked += 1

    with open(WEIGHTS_PATH, "w") as f:
        json.dump(weights, f, indent=2, ensure_ascii=False)

    print(f"Linked sentiment {args.sentiment} to {linked} chunks for {args.prd_id}", file=sys.stderr)

if __name__ == "__main__":
    main()
