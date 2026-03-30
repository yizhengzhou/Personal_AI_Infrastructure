# Knowledge Graph — Relations

<!-- Format: ## EntityA ←relation→ EntityB / - key: value lines -->
<!-- Relation types: applies_to | similar_to | depends_on | evolved_from -->
<!-- This is an example. Your relations will be auto-populated by extract-entities.py -->

---

## Memory Architecture ←applies_to→ memsearch
- reason: memsearch is the derived index layer built on top of markdown source files
- evidence: Core PAI design

## PAI System ←applies_to→ Claude Code
- reason: PAI runs natively on Claude Code as its execution environment
- evidence: Core PAI design
