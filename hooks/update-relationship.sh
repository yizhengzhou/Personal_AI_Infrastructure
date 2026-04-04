#!/bin/bash
# update-relationship.sh — Stop hook for June self-learning (D5)
# Reads stdin JSON from Claude Code, updates RELATIONSHIP files
# No LLM dependency. Fails silently. Timeout: 10s
#
# stdin payload: { "session_id": "...", "transcript_path": "...", ... }

# No set -e: fail silently, never block Claude Code

RELATIONSHIP_DIR="$HOME/.claude/MEMORY/RELATIONSHIP"
STATE_DIR="$HOME/.claude/MEMORY/STATE"
SESSION_LOG="$RELATIONSHIP_DIR/session-log.md"
PATTERNS="$RELATIONSHIP_DIR/interaction-patterns.md"
SUMMARY="$STATE_DIR/last-session-summary.md"
TODAY=$(date +%Y-%m-%d)
NOW=$(date "+%Y-%m-%d %H:%M")

# ─── Read stdin JSON payload (once, parse all fields) ───
INPUT=$(cat)

eval "$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    sid = data.get('session_id', '')
    tp = data.get('transcript_path', '')
    # Shell-safe: only allow alphanumeric, dash, underscore, slash, dot
    import re
    sid = re.sub(r'[^a-zA-Z0-9_-]', '', sid)
    tp = re.sub(r'[^a-zA-Z0-9_/.\-]', '', tp)
    print(f'PARSED_SESSION_ID=\"{sid}\"')
    print(f'PARSED_TRANSCRIPT=\"{tp}\"')
except:
    print('PARSED_SESSION_ID=\"\"')
    print('PARSED_TRANSCRIPT=\"\"')
" 2>/dev/null)"

SESSION_ID="${PARSED_SESSION_ID:-${CLAUDE_SESSION_ID:-unknown}}"
TRANSCRIPT_PATH="$PARSED_TRANSCRIPT"
SHORT_ID="${SESSION_ID:0:8}"

# ─── Extract topics from transcript (no LLM) ───
TOPICS="[auto-logged]"
if [ -n "$TRANSCRIPT_PATH" ] && [ -f "$TRANSCRIPT_PATH" ]; then
  TOPICS=$(python3 -c "
import sys, json, pathlib
tp = sys.argv[1]
try:
    lines = pathlib.Path(tp).read_text(errors='ignore').split('\n')
    topics = []
    for line in lines:
        try:
            entry = json.loads(line)
            if entry.get('type') != 'user':
                continue
            msg = entry.get('message', {})
            text = ''
            if isinstance(msg, dict):
                content = msg.get('content', '')
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get('type') == 'text':
                            text = c['text']
                            break
                elif isinstance(content, str):
                    text = content
            elif isinstance(msg, str):
                text = msg
            # Skip system/date prefixes, take meaningful content
            clean = text.strip().replace('\n', ' ')
            # Skip lines that are just timestamps or very short
            if len(clean) > 10 and not clean.startswith('[Current date'):
                topics.append(clean[:50])
        except:
            continue
    result = ' | '.join(topics[-3:]) if topics else '[auto-logged]'
    print(result[:150])
except:
    print('[auto-logged]')
" "$TRANSCRIPT_PATH" 2>/dev/null)
fi

if [ -z "$TOPICS" ]; then
  TOPICS="[auto-logged]"
fi

# ─── Ensure directories exist ───
mkdir -p "$RELATIONSHIP_DIR"
mkdir -p "$STATE_DIR"

# ─── Update session-log.md (deduplicate by session ID) ───
if [ -f "$SESSION_LOG" ]; then
  if grep -q "$SHORT_ID" "$SESSION_LOG" 2>/dev/null; then
    # Already logged this session, skip
    :
  else
    echo "" >> "$SESSION_LOG"
    echo "## $TODAY (session: $SHORT_ID)" >> "$SESSION_LOG"
    echo "**Topics**: $TOPICS" >> "$SESSION_LOG"
  fi
else
  # Create new session-log
  cat > "$SESSION_LOG" << HEREDOC
# Session Log

Chronological record of session themes and observations. Updated automatically by Stop hook.

---

## $TODAY (session: $SHORT_ID)
**Topics**: $TOPICS
HEREDOC
fi

# ─── Rotate session-log.md (keep last 20 entries) ───
ARCHIVE="$RELATIONSHIP_DIR/session-log-archive.md"
MAX_ENTRIES=20

if [ -f "$SESSION_LOG" ]; then
  ENTRY_COUNT=$(grep -c "^## " "$SESSION_LOG" 2>/dev/null || echo 0)
  if [ "$ENTRY_COUNT" -gt "$MAX_ENTRIES" ]; then
    python3 -c "
import pathlib, sys
log = pathlib.Path(sys.argv[1])
archive = pathlib.Path(sys.argv[2])
max_entries = int(sys.argv[3])

text = log.read_text()
# Split on '## ' at line start (each entry starts with ## DATE)
import re
parts = re.split(r'(?=\n## )', text)
header = parts[0]  # Everything before first ## entry
entries = parts[1:] if len(parts) > 1 else []

if len(entries) > max_entries:
    old = entries[:-max_entries]
    keep = entries[-max_entries:]
    # Append old entries to archive
    archive_header = '# Session Log Archive\n\nOlder entries rotated from session-log.md.\n\n---\n'
    existing = archive.read_text() if archive.exists() else archive_header
    if not existing.strip():
        existing = archive_header
    archive.write_text(existing.rstrip() + '\n' + ''.join(old))
    # Rewrite session-log with header + recent entries
    log.write_text(header.rstrip() + '\n' + ''.join(keep))
" "$SESSION_LOG" "$ARCHIVE" "$MAX_ENTRIES" 2>/dev/null
  fi
fi

# ─── Update interaction-patterns.md date ───
if [ -f "$PATTERNS" ]; then
  sed -i '' "s/^Last updated: .*/Last updated: $TODAY/" "$PATTERNS" 2>/dev/null
fi

# ─── Write last-session-summary.md (overwrite each time) ───
cat > "$SUMMARY" << HEREDOC
# Last Session Summary

**Date**: $NOW
**Session**: $SHORT_ID
**Topics**: $TOPICS

_Auto-generated by update-relationship.sh Stop hook_
HEREDOC
