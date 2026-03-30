# PAI System Roadmap

Development directions for the project-oriented PAI System. Prioritized by impact and feasibility.

---

## Completed (2026-03-30)

### Knowledge Graph + Weighted Memory Search
- [x] Feedback weights (EMA-based, sentiment from Algorithm reflections)
- [x] Knowledge graph (Markdown source of truth + JSON derived cache)
- [x] Enhanced memory-recall skill with re-ranking + graph query
- [x] Migration from 54 reflections → 79 chunks weighted
- [x] 4-round testing passed (isolation, weights, cross-project, end-to-end)
- [x] Rollback mechanism (3-tier: full / graph-only / weights-only)

### Pre-Algorithm Evaluation Layer
- [x] 7-step project evaluation skill (project-evaluation)
- [x] Integrates: ME Community Test, JTBD, Lean Canvas, Gstack 6 Forcing Questions, Pre-Mortem, ICE Score, Solo Dev Checklist
- [x] Conditional BMC analysis (auto-triggers for platform-dependent projects)
- [x] Go/Pivot/Kill verdict with EVALUATION.md output
- [x] CLAUDE.md gate: new projects must pass evaluation before Algorithm
- [x] Progress bar display per step

### GitHub Public Repo
- [x] Sanitized and published (no private project names, no API keys, no bot handles)
- [x] README with credits (danielmiessler, lijigang, cognee, memsearch)

---

## Direction 1: Technology Auto-Iteration
**Goal:** Existing projects' tools and skills auto-update to keep up with the latest developments.

**Problem:** YZ manually discovers new tools (browsers, CLI tools, build methods) and asks PAI to evaluate. This should be proactive, not reactive.

**Examples:**
- NotebookLM skill's browser tool: should PAI auto-detect when a better headless browser emerges?
- iOS build workflow: Xcode CLI tools evolve, PAI should suggest adoption
- Lightpanda vs Claude-in-Chrome vs Playwright: periodic re-evaluation

**Planned approach:**
- [ ] Periodic tech scan skill (monthly): scan GitHub trending, npm/pip updates, upstream PAI releases
- [ ] "Tech health check" per skill: compare current tool versions against latest
- [ ] Output: tech report with upgrade recommendations (human approves, PAI executes)
- [ ] Integrate with follow-builders skill for AI ecosystem tracking

**Status:** Discussed, not implemented.

---

## Direction 2: Self-Developing Personality
**Goal:** PAI develops consistent personality for deeper trust and partnership feel.

**Boundary:** Personality is for efficiency and consistency, NOT emotional attachment. PAI is a tool that understands your work patterns, not a simulated friend.

**Already in place:**
- DAIDENTITY.md (June persona)
- RELATIONSHIP/ (interaction patterns, session log)
- Feedback memory system

**Planned approach:**
- [ ] Systematic interaction pattern learning (beyond current ad-hoc)
- [ ] Proactive reminders based on past patterns ("you tend to abandon projects at this stage")
- [ ] Work rhythm adaptation (deep sessions vs quick tasks)
- [ ] Clear boundary: no emotional language, no "I'm worried about you"

**Status:** Ongoing, no specific implementation needed — evolves naturally with use.

---

## Direction 3: Mobile Full PAI Experience
**Goal:** Phone (Telegram or custom app) provides full PAI experience, not an isolated session.

**Problem:** Current Telegram integration is a separate session with limited context. Miessler's demo shows real-time voice conversation with PAI from any device.

**Challenges:**
- Claude Code sessions are per-terminal, no native cross-device sync
- Telegram bot polling instability (multiple processes competing)
- TTS integration is unreliable
- Context window differences (desktop 1M vs mobile text-only)

**Planned approach (phased):**
- [ ] Short-term: Stabilize single Telegram session (fixed in this session — plugin isolation)
- [ ] Mid-term: Custom iOS/Android app as thin client → WebSocket to Mac PAI session
- [ ] Long-term: Cloud-hosted PAI session (Railway/VPS), all devices connect to same instance
- [ ] TTS: Investigate alternatives to current ElevenLabs integration

**Status:** Discussed, Telegram stabilized but not production-ready.

---

## Direction 4: Company Management Role
**Goal:** PAI manages not just personal projects but operates as a virtual company team — CFO, PM, Legal advisor — providing professional counsel to the solo founder.

**Problem:** One-person company = echo chamber. No one challenges decisions. PAI should serve as:
- CFO: Monthly financial review, spending alerts, tax deadlines
- Product Manager: Product line prioritization, user feedback analysis
- Legal Advisor: Contract review reminders, compliance checks
- Blind Spot Detector: "You've abandoned 3 consecutive projects at MVP stage — should we set a completion commitment this time?"

**First step completed:** Pre-Algorithm Evaluation Layer (project-evaluation skill) — the "should we do this?" gate.

**Next steps:**
- [ ] Portfolio Review skill: Monthly review of all active projects using ICE scoring
- [ ] Company role skills: CFO monthly check, PM quarterly product review
- [ ] Gstack office-hours integration: Use YC forcing questions for ongoing project health checks (not just new projects)
- [ ] Integrate with TELOS: Company goals aligned with personal goals
- [ ] Scheduled triggers: Monthly CFO review via LaunchAgent (like Daily Brief)

**Status:** Evaluation layer done, portfolio review and role skills not yet built.

---

## Priority Order

1. **Direction 4** (Company Management) — highest value, most feasible, builds on evaluation layer
2. **Direction 1** (Tech Iteration) — important for long-term system health
3. **Direction 3** (Mobile) — high desire but technically hardest
4. **Direction 2** (Personality) — continuous, no discrete implementation needed

---

## Design Inspirations

- [danielmiessler/Personal_AI_Infrastructure](https://github.com/danielmiessler/Personal_AI_Infrastructure) — Core PAI framework
- [garrytan/gstack](https://github.com/garrytan/gstack) — YC-level evaluation methodology (Six Forcing Questions)
- [slavingia/skills](https://github.com/slavingia/skills) — Minimalist Entrepreneur framework
- [topoteretes/cognee](https://github.com/topoteretes/cognee) — Knowledge graph + weighted retrieval concepts
- [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills) — Roundtable discussions + content visualization
