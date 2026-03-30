#!/usr/bin/env bash
# rollback.sh — Remove all memsearch/memory-recall components.
# Run intentionally. No confirmation prompt. Each action is printed before it happens.

set -euo pipefail

SKILL_DIR="$HOME/.claude/skills/memory-recall"
SCRIPTS_DIR="$HOME/.claude/.memsearch/scripts"
CHUNK_WEIGHTS="$HOME/.claude/.memsearch/chunk-weights.json"
ACCESS_LOG="$HOME/.claude/.memsearch/access-log.jsonl"
KNOWLEDGE_GRAPH="$HOME/.claude/.memsearch/knowledge-graph.json"
GRAPH_DIR="$HOME/.claude/MEMORY/GRAPH"

echo "=== memsearch rollback ==="
echo ""

echo "Removing: $SKILL_DIR"
rm -rf "$SKILL_DIR"

echo "Removing: $CHUNK_WEIGHTS"
rm -f "$CHUNK_WEIGHTS"

echo "Removing: $ACCESS_LOG"
rm -f "$ACCESS_LOG"

echo "Removing: $KNOWLEDGE_GRAPH"
rm -f "$KNOWLEDGE_GRAPH"

echo "Removing: $GRAPH_DIR"
rm -rf "$GRAPH_DIR"

echo ""
echo "=== Manual step required ==="
echo "Open ~/.claude/settings.json and remove the 2 Stop hooks added by memsearch."
echo "Look for hook entries referencing memsearch scripts (e.g. update-weights.py, build-graph.py)."
echo "This file was NOT auto-edited — remove those entries by hand."
echo ""

# Remove scripts dir last (this script lives inside it)
echo "Removing: $SCRIPTS_DIR"
rm -rf "$SCRIPTS_DIR"

echo ""
echo "Rollback complete."
