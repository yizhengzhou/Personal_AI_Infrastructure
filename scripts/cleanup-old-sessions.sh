#!/bin/bash
# cleanup-old-sessions.sh — Delete Claude Code session JSONLs older than 30 days
# Safe: only touches projects/ directory, dry-run by default
#
# Usage:
#   ./cleanup-old-sessions.sh          # dry-run (show what would be deleted)
#   ./cleanup-old-sessions.sh --delete  # actually delete

PROJECTS_DIR="$HOME/.claude/projects"
DAYS=30
DRY_RUN=true

if [ "$1" = "--delete" ]; then
  DRY_RUN=false
fi

if [ ! -d "$PROJECTS_DIR" ]; then
  echo "ERROR: $PROJECTS_DIR not found"
  exit 1
fi

# Find JSONL files older than $DAYS days
OLD_FILES=$(find "$PROJECTS_DIR" -type f -name "*.jsonl" -mtime +${DAYS} 2>/dev/null)
# Also find orphaned tool-result images/PDFs
OLD_MEDIA=$(find "$PROJECTS_DIR" -type f \( -name "*.jpg" -o -name "*.png" -o -name "*.pdf" \) -mtime +${DAYS} 2>/dev/null)

ALL_FILES=$(printf '%s\n%s' "$OLD_FILES" "$OLD_MEDIA" | grep -v '^$')

if [ -z "$ALL_FILES" ]; then
  echo "No files older than ${DAYS} days found."
  exit 0
fi

COUNT=$(echo "$ALL_FILES" | wc -l | tr -d ' ')
SIZE=$(echo "$ALL_FILES" | xargs du -ch 2>/dev/null | tail -1 | awk '{print $1}')

if $DRY_RUN; then
  echo "=== DRY RUN ==="
  echo "Would delete $COUNT files, freeing $SIZE"
  echo ""
  echo "Oldest 10 files:"
  echo "$ALL_FILES" | xargs ls -lt 2>/dev/null | tail -10
  echo ""
  echo "Run with --delete to actually remove these files."
else
  echo "Deleting $COUNT files older than ${DAYS} days ($SIZE)..."
  echo "$ALL_FILES" | xargs rm -f 2>/dev/null

  # Remove empty subdirectories left behind
  find "$PROJECTS_DIR" -type d -empty -delete 2>/dev/null

  echo "Done. Freed $SIZE."
fi
