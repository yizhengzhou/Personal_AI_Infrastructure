# Reflections — Principal Self-Reflection Capture

> **PAI 4.0** — Principal thought capture, the missing half of the learning loop.

**The system learns from its own failures (LEARNING/). This module captures what the principal observes, thinks, and reflects on — the human side of the loop.**

---

## Why This Exists

PAI captures agent-side signals extensively:
- `LEARNING/SIGNALS/` — user satisfaction ratings
- `LEARNING/FAILURES/` — what went wrong and why
- `LEARNING/ALGORITHM/` — execution reflections
- `WorkCompletionLearning` — session-end learnings

But the principal's own thinking — observations, ideas, reflections, epiphanies — had no home. These thoughts are the source of direction, priorities, and creativity. Without capturing them, PAI operates on inferred intent rather than expressed thought.

---

## Architecture

```
Principal has a thought
    ↓
Trigger (any interface)
    ├── CLI: "記一下" / capture command
    ├── Telegram: intent detection → thought capture mode
    └── 9PM scheduled prompt → structured 3-point collection
    ↓
A_CAPTURE_THOUGHT (Action)
    ├── Validate & timestamp
    ├── Auto-tag (LLM-generated, max 3 tags)
    └── Write to Obsidian
    ↓
Storage: Obsidian vault (single source of truth)
    ~/Documents/Project/obsidiant-vault/XYZ-medium/idea/YYYY-MM-DD.md
    ↓
Periodic enrichment (optional, future)
    ├── Monthly theme synthesis
    └── Cross-reference with Telos/GOALS.md
```

### Design Decision: Single Storage in Obsidian

**Obsidian is the sole storage.** No dual-write to `MEMORY/`. Reasons:

1. YZ already uses Obsidian for knowledge management
2. Obsidian has search, graph view, backlinks — better than flat files
3. Dual-write creates sync headaches for zero benefit
4. PAI can read Obsidian files on demand when needed

PAI accesses reflections by reading the Obsidian vault, not by maintaining a copy.

---

## File Format

Each day gets one file: `idea/YYYY-MM-DD.md`

```markdown
---
date: 2026-03-26
entries: 3
tags: [ai-agents, writing, interface-design]
---

## 14:30
- 以前的作者將自己的書改編成一個skill，而開發大神說現在寫的文件都是未來給agent看的不是給人類看的，這二者都是對於文字的變化，重點都是文字未來真的都是給agent看而不是給人看的。

#ai-agents #writing

## 21:05
- 觀察到社區裡的人開始用 Claude Code 做非程式的事，像是寫日記、管理生活。工具的使用方式永遠超出設計者的想像。

#tool-usage #community

## 21:08
- 每天跟 June 對話的過程本身就是一種自省，只是以前沒有意識到要把這些想法系統化地留下來。

#self-reflection #pai
```

### Format Rules

- **Frontmatter:** date, entry count, aggregated tags (auto-updated)
- **Entry header:** `## HH:MM` timestamp
- **Entry body:** `-` prefixed, YZ 的原話，不改寫
- **Tags:** 每條 entry 最多 3 個 auto-generated tags（LLM 生成，YZ 可修改）
- **Separator:** entries 之間用 `## HH:MM` 自然分隔
- **Append-only:** 新 entry 追加到檔案尾端，不修改已有 entry

---

## Triggers

### 1. Anytime Capture（隨時觸發）

**Intent detection keywords:**
- 明確：「記一下」「幫我記」「寫進日記」「記到 idea」「capture this」
- 隱含：YZ 分享觀察/想法 + 要求保存（「這個幫我存起來」）

**Flow:**
```
YZ: [shares thought] + [save intent]
June: 記了。 ✅  (≤10 words, no analysis)
     → writes to idea/YYYY-MM-DD.md
     → if YZ continues with "還有" / "另外" → append mode
```

**Anti-patterns (MUST NOT):**
- Do NOT auto-save thoughts from normal conversation
- Do NOT give lengthy analysis before/after saving
- Do NOT rewrite or summarize YZ's words
- Do NOT count your own analysis as YZ's points

### 2. Scheduled Capture（9PM 排程）

**Flow:**
```
LaunchAgent fires at 21:00
    → Telegram message: "YZ，daily capture 時間。今天第一個想法？"
    → YZ replies with point 1
    → June: "收到。第二個？" (≤10 words)
    → YZ replies with point 2
    → June: "好，最後一個？" (≤10 words)
    → YZ replies with point 3 (or says "就這樣")
    → June: writes ALL points to idea/YYYY-MM-DD.md
    → June: "三點都記了 ✅" (or "兩點記了 ✅")
```

**Counting protocol:**
- 1 message from YZ with 1 core idea = 1 point
- YZ's elaboration on the same idea = still 1 point
- June's analysis/expansion = 0 points (NEVER counts)
- "就這樣" / "只有這些" / "沒了" = end collection, save immediately

### 3. CLI Capture（未來）

```bash
# Inside Claude Code session
> 記一下：今天發現 MCP 的權限模型有個根本性的設計問題...
# → saves to idea/YYYY-MM-DD.md
```

This already works — any Claude Code session with PAI loaded will recognize the intent keywords and save.

---

## Action Spec

```
A_CAPTURE_THOUGHT/
├── action.json
└── action.ts
```

### action.json

```json
{
  "name": "A_CAPTURE_THOUGHT",
  "description": "Capture principal's thought/observation to daily Obsidian file. Preserves original wording, auto-generates tags.",
  "input": {
    "thought": { "type": "string", "required": true, "description": "Principal's original wording, unmodified" },
    "tags": { "type": "array", "description": "Auto-generated tags (max 3). Optional — LLM generates if not provided." },
    "source": { "type": "string", "description": "Where captured: telegram, cli, voice" }
  },
  "output": {
    "file": { "type": "string", "description": "Path to the written file" },
    "entry_count": { "type": "integer", "description": "Total entries in today's file after write" },
    "tags_used": { "type": "array" }
  },
  "requires": ["shell"]
}
```

### Implementation (shell-based, no LLM dependency for write)

The action:
1. Determines today's date → file path
2. If file doesn't exist → create with frontmatter
3. Append entry with `## HH:MM` header + thought + tags
4. Update frontmatter `entries` count and `tags` array
5. Return confirmation

Tag generation is handled by the calling agent (Claude/June), not by the action itself. The action receives pre-generated tags.

---

## Retrieval

### Search by date
```bash
cat ~/Documents/Project/obsidiant-vault/XYZ-medium/idea/2026-03-26.md
```

### Search by keyword
```bash
grep -r "MCP" ~/Documents/Project/obsidiant-vault/XYZ-medium/idea/
```

### Search by tag
```bash
grep -r "#ai-agents" ~/Documents/Project/obsidiant-vault/XYZ-medium/idea/
```

### In Obsidian
- Graph view shows tag connections across days
- Backlinks show related entries
- Search is native and fast

---

## Telos Integration

Monthly (or on-demand), a synthesis can cross-reference:

- **GOALS.md** — are your daily thoughts aligned with stated goals?
- **BELIEFS.md** — are observations challenging or reinforcing beliefs?
- **WISDOM.md** — any thought worthy of promoting to permanent wisdom?

This is NOT automatic. It's triggered when YZ asks: "這個月我都在想什麼？" or "review my reflections."

---

## Migration from Current Setup

### What changes:

| Component | Before | After |
|-----------|--------|-------|
| Telegram bot prompt | Inline counting rules | References this spec |
| Storage format | Flat bullets | Timestamped entries with tags |
| 9PM script | Static message | Same (unchanged) |
| Anytime capture | Not supported | Intent detection in bot prompt |
| CLI capture | Not supported | PAI-aware intent detection |
| Retrieval | Manual file read | grep + Obsidian native |

### Migration steps:

1. ✅ Telegram bot prompt already updated (this session)
2. Update storage format to use `## HH:MM` headers + tags
3. Register this document in PAI architecture (CONTEXT_ROUTING.md)
4. Create A_CAPTURE_THOUGHT action spec (optional — shell commands work fine)
5. Add monthly synthesis prompt to Telos integration (future)

---

## What This Is NOT

- **Not a journal app** — no free-form long writing, just capture points
- **Not auto-capture** — only saves when YZ explicitly asks
- **Not AI-generated content** — stores YZ's original words, never rewrites
- **Not a replacement for Memory System** — Memory is for cross-session AI context; Reflections is for principal's human thinking

---

**Last Updated:** 2026-03-26
