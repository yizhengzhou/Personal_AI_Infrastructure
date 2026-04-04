# Knowledge Graph — Relations

<!-- Seeded 2026-03-29 from WORK/ PRD analysis + known PAI ecosystem connections -->
<!-- Format: ## EntityA ←relation→ EntityB / - key: value lines -->
<!-- Relation types: applies_to | similar_to | depends_on | evolved_from -->

---

## PAI System ←applies_to→ memory-graph
- reason: Knowledge graph is a core new component of PAI's hierarchical memory architecture
- evidence: 2026-03-30 pai-memory-enhancement-plan PRD

## Memory Architecture ←applies_to→ memsearch
- reason: memsearch is the derived index layer built on top of Markdown source files
- evidence: 2026-03-08 WORK sessions use memsearch for recall

## Cognee AI ←similar_to→ PAI System
- reason: Both use hierarchical storage combining graph, vector, and document layers
- evidence: 2026-03-29 cognee-self-learning-analysis PRD

## MCP ←applies_to→ claude-in-chrome
- reason: claude-in-chrome is implemented as an MCP server enabling browser control
- evidence: 2026-03-23 browser-use-vs-claude-in-chrome PRD

## MCP ←applies_to→ Mirroir
- reason: Mirroir exposes iOS screen control via MCP protocol
- evidence: 2026-03-23 mobile-agent-testing-research PRD

## Fabric ←evolved_from→ PAI System
- reason: Fabric was the original PAI predecessor, rewritten from Python to Go
- evidence: 2026-03-30 entities seed

## Telegram bot ←depends_on→ PAI System
- reason: JunePai_bot integrates with PAI via LaunchAgent scheduling and Claude Code sessions
- evidence: 2026-03-22 fix-telegram-bots, 2026-03-28 multi-project-telegram-bot

## multi-session-architecture ←applies_to→ Telegram bot
- reason: Multi-project session routing was built specifically to enable JunePai_bot project isolation
- evidence: 2026-03-28 multi-project-telegram-bot PRD

## NotebookLM ←applies_to→ PAI System
- reason: NotebookLM techniques documented in PAI memory; used for research deep-dives
- evidence: 2026-03-08 MEMORY/WORK sessions

## Raspberry Pi 5 ←applies_to→ rpi5-always-on
- reason: RPi5 hardware is the physical realization of the always-on compute concept
- evidence: 2026-03-10 evaluate-install-claude-rpi5 PRD

## evaluate-install-claude-rpi5 ←similar_to→ install-gemini-gstack-rpi
- reason: Both are RPi5 agent-runtime installation tasks, different LLM backends (Gemini vs Claude)
- evidence: 2026-03-10, 2026-03-22 PRD slugs

## style-transfer ←evolved_from→ face-swap
- reason: ATTENTION feature pivoted from style-transfer to face-swap after style results were unsatisfactory
- evidence: 2026-03-13 evaluate-transformation-tech-route PRD

## k-means-segmentation ←applies_to→ style-transfer
- reason: K-means color segmentation became the face detection method feeding the style compositing pipeline
- evidence: 2026-03-16 kmeans-v3-pipeline-test PRD

## ephemeral-content ←applies_to→ ephemeral-photo-share-report
- reason: The ephemeral-photo-share-report task directly implements the ephemeral-content pattern
- evidence: 2026-03-15 ephemeral-photo-share-report PRD

## app-store-optimization ←applies_to→ merge-aso-skills-global-pipeline
- reason: The merge task restructured ASO skills into a reusable global pipeline
- evidence: 2026-03-25 merge-aso-skills-global-pipeline PRD

## self-reflection-capture ←depends_on→ PAI System
- reason: Self-reflection capture is a new PAI memory subsystem capturing principal-side insights
- evidence: 2026-03-26 pai-self-reflection-capture-design PRD

## cognee-self-learning-analysis ←applies_to→ pai-memory-enhancement-plan
- reason: Cognee analysis directly informed and preceded the PAI memory enhancement design
- evidence: 2026-03-29 cognee PRD leads to 2026-03-30 enhancement PRD

## Claude Code ←applies_to→ PAI System
- reason: Claude Code is the primary execution engine for all PAI work sessions
- evidence: All WORK/ PRDs from 2026-03-08 onward

## singlingo-mvp-design-spec ←evolved_from→ xcode-ios-dev-workflow-research
- reason: iOS workflow research directly fed into SingLingo project scaffold decisions
- evidence: 2026-03-22 and 2026-03-23 PRDs in sequence

## browser-use-vs-claude-in-chrome ←similar_to→ mobile-agent-testing-research
- reason: Both tasks evaluate AI browser/mobile automation approaches for the same underlying agent-testing need
- evidence: 2026-03-23 two PRDs on same day

## Markdown Source of Truth → Knowledge Graph
- relation: applies_to
- reason: Markdown files (entities.md, relations.md) serve as source of truth for knowledge graph
- first_seen: 2026-03-30


## Derived Index Layer → knowledge-graph.json
- relation: applies_to
- reason: JSON cache is derived from markdown source, can be rebuilt if deleted
- first_seen: 2026-03-30


## Derived Index Layer → memsearch
- relation: applies_to
- reason: memsearch hash IDs are derived/cached data that can be reindexed
- first_seen: 2026-03-30


## Hierarchical Memory Storage → PAI System
- relation: applies_to
- reason: PAI uses layered architecture separating source truth from derived data
- first_seen: 2026-03-30


## knowledge-graph.json → entities.md
- relation: evolved_from
- reason: JSON derives from markdown entities as source of truth
- first_seen: 2026-03-30

## BookToSkill → Book-to-Skill Decision Tree
- relation: applies_to
- reason: Decision tree is core framework within BookToSkill project
- first_seen: 2026-03-30


## PrinciplesDiagnose → BookToSkill
- relation: depends_on
- reason: PrinciplesDiagnose spec uses BookToSkill's decision tree framework
- first_seen: 2026-03-30


## skill.config.json → Chat
- relation: applies_to
- reason: config is translation layer for Chat skill type
- first_seen: 2026-03-30


## skill.config.json → Form-to-Result
- relation: applies_to
- reason: config is translation layer for Form-to-Result skill type
- first_seen: 2026-03-30


## Unified Template Skeleton → Chat
- relation: applies_to
- reason: Template skeleton used for Chat skill implementation
- first_seen: 2026-03-30


## Unified Template Skeleton → Form-to-Result
- relation: applies_to
- reason: Template skeleton used for Form-to-Result skill implementation
- first_seen: 2026-03-30


## Book-to-Skill Decision Tree → Chat
- relation: similar_to
- reason: Decision tree classifies interaction modes including Chat
- first_seen: 2026-03-30


## Book-to-Skill Decision Tree → Form-to-Result
- relation: similar_to
- reason: Decision tree classifies interaction modes including Form-to-Result
- first_seen: 2026-03-30


## Book-to-Skill Decision Tree → Pipeline
- relation: similar_to
- reason: Decision tree classifies interaction modes including Pipeline
- first_seen: 2026-03-30


## Progress Display → statusLine
- relation: evolved_from
- reason: Progress display pattern extends statusLine to per-step level
- first_seen: 2026-03-30


## BYOK Configuration → skill.config.json
- relation: applies_to
- reason: BYOK settings defined in skill.config.json schema
- first_seen: 2026-03-30


## Backend Requirements Determination → skill.config.json
- relation: applies_to
- reason: Backend requirement logic drives config generation
- first_seen: 2026-03-30


## Web App Generation → SKILL.md
- relation: depends_on
- reason: Web app is generated by parsing SKILL.md metadata
- first_seen: 2026-03-30

## BookToSkill → NotebookLM
- relation: depends_on
- reason: BookToSkill uses NotebookLM to automatically generate skills from books
- first_seen: 2026-04-03


## BookToSkill → Sahil's Skills
- relation: similar_to
- reason: Both convert books into skills; BookToSkill automates what Sahil did manually
- first_seen: 2026-04-03


## Instruction Stacking → Running Lean
- relation: applies_to
- reason: Running Lean serves as concrete example of instruction-stacking problem
- first_seen: 2026-04-03


## Skills → Knowledge Internalization
- relation: applies_to
- reason: Skills discussed as mechanism for internalizing knowledge from books
- first_seen: 2026-04-03

## n8n-video → pipeline
- relation: applies_to
- reason: n8n-video project is used to create and manage pipelines
- first_seen: 2026-04-04


## pipeline → Meta Threads
- relation: depends_on
- reason: pipeline publishing requires Meta Threads API credentials
- first_seen: 2026-04-04


## pipeline → X
- relation: depends_on
- reason: pipeline publishing requires X API credentials
- first_seen: 2026-04-04


## Meta Threads → X
- relation: similar_to
- reason: both are social media platforms targeted for pipeline publishing
- first_seen: 2026-04-04

