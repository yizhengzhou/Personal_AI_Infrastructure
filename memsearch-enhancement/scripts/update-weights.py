#!/usr/bin/env python3
"""
update-weights.py — Process memsearch access-log and update chunk weights.

Reads access-log.jsonl, increments access_count/usefulness signals for each
expanded hash, writes updated chunk-weights.json, then truncates the log.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path.home() / ".claude" / ".memsearch"
ACCESS_LOG = BASE_DIR / "access-log.jsonl"
CHUNK_WEIGHTS = BASE_DIR / "chunk-weights.json"


def load_access_log():
    """Return list of parsed log entries. Empty list if file missing or empty."""
    if not ACCESS_LOG.exists():
        return []
    entries = []
    with ACCESS_LOG.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"update-weights: skipping malformed line {lineno}: {exc}", file=sys.stderr)
    return entries


def load_weights():
    """Return weights dict. Empty dict if file missing."""
    if not CHUNK_WEIGHTS.exists():
        return {}
    with CHUNK_WEIGHTS.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as exc:
            print(f"update-weights: corrupt chunk-weights.json: {exc}", file=sys.stderr)
            sys.exit(1)


def save_weights(weights):
    CHUNK_WEIGHTS.write_text(json.dumps(weights, indent=2, ensure_ascii=False), encoding="utf-8")


def process(entries, weights):
    """Apply all log entries to weights in place."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for entry in entries:
        hashes = entry.get("expanded_hashes", [])
        if not hashes:
            continue

        # Use the entry's timestamp date when available, fall back to today.
        ts = entry.get("timestamp", "")
        if ts:
            try:
                accessed_date = datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d")
            except ValueError:
                accessed_date = today
        else:
            accessed_date = today

        for h in hashes:
            if h not in weights:
                weights[h] = {
                    "access_count": 0,
                    "last_accessed": accessed_date,
                    "usefulness_sum": 0.0,
                    "usefulness_count": 0,
                    "sentiment_boost": 0.0,
                }
            rec = weights[h]
            rec["access_count"] = rec.get("access_count", 0) + 1
            rec["last_accessed"] = accessed_date
            rec["usefulness_sum"] = rec.get("usefulness_sum", 0.0) + 1.0
            rec["usefulness_count"] = rec.get("usefulness_count", 0) + 1


def truncate_log():
    ACCESS_LOG.write_text("", encoding="utf-8")


def main():
    entries = load_access_log()

    if not entries:
        # Nothing to process — exit silently.
        return

    weights = load_weights()
    process(entries, weights)
    save_weights(weights)
    truncate_log()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"update-weights: unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)
