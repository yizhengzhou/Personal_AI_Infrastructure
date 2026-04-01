# PAI System Update: Claude Code Alignment v1

**Date:** 2026-04-01
**Trigger:** Claude Code v2.1.88 source code leak via npm sourcemap (2026-03-31)
**PAI Version:** 4.0.3 → 4.0.4-alignment
**Scope:** System-level changes based on Claude Code internal architecture analysis

---

## Context

Claude Code's full source code (512,000 lines, 1,900 files) was accidentally published via a .map file in npm package v2.1.88. Analysis of this code revealed internal systems that PAI can better align with, since PAI runs on top of Claude Code.

Two rounds of verification tests were conducted on Claude Code v2.1.87 to confirm assumptions before making changes.

---

## Changes Made

### 1. Memory System Alignment (autoDream)

**What:** Aligned PAI's memory files with Claude Code's autoDream format requirements.

| File | Change |
|------|--------|
| `memory/notebooklm-techniques.md` | Added YAML frontmatter (name, description, type) |
| `memory/notebooklm-setup.md` | Added YAML frontmatter |
| `memory/user_telos_core.md` | **New** — YZ's core beliefs and life goals |
| `memory/project_july_agent.md` | **New** — july agent design summary |
| `memory/MEMORY.md` | Updated index with Telos and july sections |

**Why:** autoDream (Claude Code's background memory consolidation system) requires markdown files with YAML frontmatter containing `name`, `description`, and `type` (user/feedback/project/reference) fields. Files without frontmatter may be ignored during automatic consolidation.

**Setting:** `"auto_dream": true` added to `settings.json`

**Verification:** T1 confirmed autoDream code exists in v2.1.87 binary. Activation status depends on server-side feature flag (under observation).

### 2. Context Compaction Hooks (PreCompact / PostCompact)

**What:** Added hooks for context compaction events.

```json
"PreCompact": [{
  "hooks": [{
    "type": "command",
    "command": "echo \"$(date) PRE_COMPACT\" >> ~/.claude/MEMORY/STATE/events.jsonl",
    "timeout": 5,
    "statusMessage": "Saving state before compaction..."
  }]
}],
"PostCompact": [{
  "hooks": [{
    "type": "command",
    "command": "echo \"$(date) POST_COMPACT\" >> ~/.claude/MEMORY/STATE/events.jsonl",
    "timeout": 5
  }]
}]
```

**Why:** Long conversations trigger context compaction, which can lose Algorithm state. These hooks provide observability into when compaction happens.

**Verification:** T7 discovered PreCompact/PostCompact in the hook event whitelist (13 events total, 6 previously unknown).

### 3. CLAUDE.md Compaction Recovery

**What:** Added a recovery hint at the top of CLAUDE.md.

```
> **Compaction Recovery:** If context was compressed mid-conversation,
> read `MEMORY/STATE/current-work.json` to restore current work context.
> Algorithm state is auto-saved in MEMORY/STATE/algorithms/.
```

**Why:** After compaction, CLAUDE.md is re-injected but conversation context is summarized. This hint tells the model where to find preserved state.

### 4. july Telos Reflection (Prompt Hook)

**What:** Added a `prompt` type hook on the `Stop` event.

```json
{
  "type": "prompt",
  "prompt": "Analyze the conversation... Did it touch on Telos topics?...",
  "timeout": 15,
  "statusMessage": "july is reflecting on this conversation..."
}
```

**Why:** july is a companion agent focused on long-term meaning (parallel to june's efficiency focus). This hook uses a small LLM to evaluate whether each conversation touched on Telos-relevant topics. It does NOT auto-write to Telos — it only evaluates.

**Verification:** T4 confirmed `type: "prompt"` hooks are fully supported in v2.1.87.

### 5. july Agent Definition

**What:** Created `~/.claude/agents/july.md` — a named agent with distinct personality.

**Role:** Curious explorer, long-term thinker. Activated when conversations touch meaning, direction, creative ideas.

**Relationship to june:** Parallel, not hierarchical. june handles efficiency; july handles meaning.

### 6. Telos System Population

**What:** Created `PAI/USER/TELOS/BELIEFS.md` and `PAI/USER/TELOS/GOALS.md`.

**Why:** Telos was previously an empty directory. Now contains YZ's core beliefs and life goals, enabling july and other systems to reference them.

---

## Verification Tests Conducted

| Test | Result | Key Finding |
|------|--------|-------------|
| T1: autoDream existence | ⚠️ Code exists, not yet triggered | `autoDreamEnabled`, `tengu_auto_dream_*` found in binary |
| T4: Prompt hook | ✅ Fully supported | Schema confirmed, no errors |
| T5: Agent hook | ✅ Fully supported | Default model: Haiku |
| T6: HTTP hook | ✅ Fully supported | Includes `allowedEnvVars` security |
| T7: Hook events | ✅ 13 events found | +6 unknown: PreCompact, PostCompact, SubagentStop, TaskCreated, TaskCompleted, TeammateIdle |
| T10: Feature flags | ⚠️ CronCreate enabled | KAIROS = CronCreate tool group, default true |
| T11: Coordinator | ❌ Not a subagent_type | Architecture role, configurable via agents |

Full test results: `~/.claude/MEMORY/WORK/2026-04-01_PAI-claude-code-alignment/`

---

## Hook System Discovery: Complete Event Whitelist

Previously known (7):
`SessionStart`, `SessionEnd`, `Stop`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Notification`

Newly discovered (6):
`SubagentStop`, `PreCompact`, `PostCompact`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`

Hook types available (4):
`command`, `prompt`, `http`, `agent`

---

## Rollback

```bash
# Full rollback
cp ~/.claude/settings.json.pre-alignment-backup ~/.claude/settings.json
cp -r ~/.claude/projects/-Users-zhyz--claude/memory.pre-alignment-backup/ ~/.claude/projects/-Users-zhyz--claude/memory/
```

---

## Observation Period

The following need monitoring over 2 weeks:
1. Does autoDream actually trigger? (Check memory/ for non-manual modifications)
2. Does the july prompt hook produce useful output? (Check Stop event behavior)
3. Do PreCompact/PostCompact events fire during long conversations? (Check events.jsonl)
4. Any performance impact from the new hooks?

---

## Next Steps (Not Yet Implemented)

| Item | Depends On |
|------|-----------|
| CronCreate for july autonomous exploration | Confirming CronCreate doesn't require persistent Claude Code process |
| HTTP hook for Telegram notifications | Stable after observation period |
| Agent hook for Telos auto-suggestions | Confirming agent hook file access permissions |
| Builder/Validator pattern (community idea) | After core alignment is stable |
