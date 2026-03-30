# PAI System

> Project-Oriented Personal AI Infrastructure — from idea to market, powered by Claude Code.

Inspired by [danielmiessler/Personal_AI_Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure), this is an evolved implementation that extends PAI from personal life management into a **full-lifecycle project development platform**.

## What is this?

PAI (Personal AI Infrastructure) is a framework for building an AI system that truly knows you — your goals, your projects, your patterns, your preferences. It runs natively on [Claude Code](https://claude.ai/claude-code) and manages everything from ideation to shipping.

This repo is a **production implementation** that has been running daily since early 2026, managing 40+ projects simultaneously.

## How it differs from upstream PAI

The original PAI focuses on augmenting an individual's capabilities. This implementation evolves it into a **project-oriented system** that manages multiple concurrent projects while maintaining the TELOS (personal goals) philosophy at its core.

### Core Framework (from upstream PAI v4.0.3)

| Component | Description |
|-----------|-------------|
| **The Algorithm** | 7-phase execution engine: Observe → Think → Plan → Build → Execute → Verify → Learn |
| **Ideal State Criteria (ISC)** | Atomic, verifiable criteria that define "done" |
| **Skill System** | CODE → CLI → PROMPT → SKILL deterministic execution chain |
| **Hook System** | Event-driven automation (SessionStart, Stop, PreToolUse, PostToolUse) |
| **PRD Format** | Single source of truth for work metadata, criteria, decisions |
| **TELOS** | Goal-oriented personal context layer |

### What we added

#### 1. Knowledge Graph + Weighted Memory Search

PAI's memory system (via [memsearch](https://github.com/zilliztech/memsearch)) treats all memories equally. We added two layers on top:

**Feedback Weights** — Memories that are frequently accessed and associated with high-quality work (Algorithm sentiment ratings) rank higher in search results. Uses EMA-based weight updates with recency decay (14-day half-life).

**Knowledge Graph** — Lightweight entity-relationship graph stored as Markdown (source of truth) with a derived JSON cache for fast querying. Enables cross-project learning: "What did we learn in Project A that applies to Project B?"

```
memsearch search (project-local, top 10)
    ↓
graph query (cross-project connections, up to 2)
    ↓
weighted re-ranking (score × 0.6 + usefulness × 0.2 + recency × 0.1 + sentiment × 0.1)
    ↓
top 5 results + 2 graph-connected supplements
```

Design principle: **Markdown is the source of truth.** The knowledge graph lives in `MEMORY/GRAPH/entities.md` and `relations.md` — human-readable, git-trackable, manually editable. The JSON cache is derived and rebuildable.

> Memory enhancement was inspired by concepts from [cognee](https://github.com/topoteretes/cognee).

#### 2. Multi-Project Management

The system manages 40+ projects concurrently through:

- **MEMORY/WORK/** — Each project gets a timestamped PRD (Product Requirements Document) with ISC criteria, decisions, and verification evidence
- **Multi-session architecture** — Multiple Claude Code sessions run simultaneously, each focused on a different project
- **Cross-project memory** — The knowledge graph connects lessons learned across projects

#### 3. Roundtable Discussions

An interactive multi-perspective discussion system using **real historical and contemporary figures** (not fictional agents). Features:

- Participants must speak authentically from their actual belief systems, referencing canonical works
- Dynamic dialogue with action labels (陳述/質疑/補充/反駁/修正/綜合)
- Moderator synthesizes tensions and generates ASCII knowledge network diagrams
- User-controlled depth: continue, end, deepen current thread, or introduce new participants
- Auto-saves complete transcripts to Obsidian vault

> Roundtable workflow adapted from [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills) (`ljg-roundtable`). The original design by [lijigang](https://github.com/lijigang) introduced the concept of real-figure roundtable discussions with truth-seeking over surface harmony.

#### 4. Content Automation Pipeline

PAI doesn't stop at building — it automates promotion:

- **ASO (App Store Optimization) skill** — Research, optimize, and track mobile app performance
- **Content visualization** — Transform content into PNG cards, infographics, visual sketchnotes, comics
- **AI builder digest** — Monitors top AI builders and remixes their content into digestible summaries
- **Video pipeline** — n8n + AI video generation + Remotion overlays for automated content production

> Content visualization (ljg-card) adapted from [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills).

#### 5. Thinking Skill Suite

A unified analytical and creative thinking system with 7 modes:

| Mode | Purpose |
|------|---------|
| **First Principles** | Decompose, challenge assumptions, rebuild |
| **Iterative Depth** | Multi-angle deep exploration |
| **Council (Debate)** | Multi-agent structured decision-making |
| **Council (Roundtable)** | Real-figure thought exploration |
| **Red Team** | Adversarial attack on ideas |
| **World Threat Model** | Future scenario analysis |
| **Science** | Hypothesis generation and testing |

#### 6. Principal Reflection Capture

Captures the human side of the learning loop — your observations, ideas, epiphanies — separately from AI-generated signals. Stores reflections in Obsidian with auto-generated tags, preserving original wording.

## Directory Structure

```
.
├── PAI/                          # Core framework
│   ├── Algorithm/                # The Algorithm (v3.7.0)
│   ├── Tools/                    # CLI tools (pai.ts, algorithm.ts, etc.)
│   ├── USER/                     # Personal context (template — add your own)
│   │   └── TELOS/                # Goals, beliefs, challenges
│   ├── MEMORYSYSTEM.md           # Memory architecture spec
│   ├── SKILLSYSTEM.md            # Skill system spec
│   ├── THEHOOKSYSTEM.md          # Hook system spec
│   ├── PRDFORMAT.md              # PRD specification
│   ├── REFLECTIONS.md            # Reflection capture spec
│   └── ...                       # Other system documentation
│
├── skills/                       # Skill library
│   ├── Thinking/                 # 7-mode analytical thinking
│   │   └── Council/              # Debate + Roundtable + Quick
│   ├── memory-recall/            # Enhanced memory with weights + graph
│   ├── app-store-optimization/   # ASO toolkit
│   ├── ljg-card/                 # Content → visual cards
│   ├── follow-builders/          # AI builder digest
│   └── ...
│
├── MEMORY/                       # Memory hierarchy (template)
│   ├── GRAPH/                    # Knowledge graph (markdown source of truth)
│   │   ├── entities.md           # Entity definitions
│   │   └── relations.md          # Relationship definitions
│   ├── LEARNING/REFLECTIONS/     # Algorithm reflections (JSONL)
│   ├── WORK/                     # Project PRDs
│   └── ...
│
├── memsearch-enhancement/        # Memory enhancement scripts
│   └── scripts/
│       ├── update-weights.py     # Feedback weight updates
│       ├── extract-entities.py   # Entity extraction → graph
│       ├── build-graph-cache.py  # Markdown → JSON cache
│       ├── query-graph.py        # Graph query engine
│       ├── migrate-weights.py    # Seed weights from reflections
│       └── rollback.sh           # Full rollback script
│
├── CLAUDE.md.template            # Claude Code instruction template
└── hooks/                        # Event-driven automation hooks
```

## Prerequisites

- [Claude Code](https://claude.ai/claude-code) (CLI or desktop)
- [memsearch](https://github.com/zilliztech/memsearch) plugin (for memory features)
- Python 3.9+ (for enhancement scripts — stdlib only, no extra dependencies)

## Getting Started

1. **Clone this repo** into your Claude Code config directory:
   ```bash
   git clone https://github.com/yizhengzhou/Personal_AI_Infrastructure.git ~/.claude/PAI-system
   ```

2. **Personalize** `PAI/USER/` with your own TELOS, identity, and preferences.

3. **Copy** `CLAUDE.md.template` to `~/.claude/CLAUDE.md` and adjust.

4. **Install memsearch** for memory features:
   ```bash
   pip install 'memsearch[onnx]'
   ```

5. **Run migration** to seed initial knowledge graph:
   ```bash
   python3 memsearch-enhancement/scripts/build-graph-cache.py
   ```

## Philosophy

This system is built on three beliefs:

1. **AI should manage projects, not just write code.** From ideation (TELOS) through development (Algorithm) to market (ASO, content pipeline) — the entire lifecycle.

2. **Memory should learn from itself.** Frequently useful memories should surface faster. Cross-project patterns should be discoverable. The system gets smarter over time.

3. **Markdown is the source of truth.** Every piece of knowledge — memory, graph, PRD, reflection — lives in human-readable, git-trackable Markdown. Databases and caches are derived and disposable.

## Credits

- **Core PAI Framework** — [Daniel Miessler](https://github.com/danielmiessler) / [Personal_AI_Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) (v4.0.3)
- **Roundtable & Content Cards** — [lijigang](https://github.com/lijigang) / [ljg-skills](https://github.com/lijigang/ljg-skills) (ljg-roundtable, ljg-card)
- **Memory Enhancement Inspiration** — [cognee](https://github.com/topoteretes/cognee) (knowledge graph + weighted retrieval concepts)
- **Semantic Memory Search** — [memsearch](https://github.com/zilliztech/memsearch) (Milvus-based hybrid search)
- **AI Agent Platform** — [Claude Code](https://claude.ai/claude-code) by Anthropic

## License

MIT — see [LICENSE](LICENSE).
