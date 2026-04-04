---
name: Council
description: >-
  Multi-perspective deliberation with visible transcripts. USE WHEN council,
  debate, roundtable, 圓桌, perspectives, weigh options, deliberate, multiple
  viewpoints. Three modes: Debate (engineering decisions), Quick (sanity check),
  Roundtable (philosophical/conceptual exploration).
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/PAI/USER/SKILLCUSTOMIZATIONS/Council/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# Council Skill

Multi-perspective deliberation system where specialized voices discuss topics in rounds, respond to each other's points, and surface insights through intellectual friction.

**Key Differentiator from RedTeam:** Council is collaborative-adversarial (debate to find best path), while RedTeam is purely adversarial (attack the idea). Council produces visible conversation transcripts; RedTeam produces steelman + counter-argument.

## Workflow Routing

| Trigger | Workflow | Description |
|---------|----------|-------------|
| Engineering/design decisions, code review, architecture choices | `Workflows/Debate.md` | Structured 3-round debate with domain experts, convergent (30-90s) |
| Fast sanity check, quick feedback | `Workflows/Quick.md` | Single-round parallel perspectives, fast (10-20s) |
| Philosophy, society, culture, conceptual exploration, 圓桌 | `Workflows/Roundtable.md` | Dialectical exploration with real historical/contemporary figures, divergent, user-controlled |
| Pure adversarial analysis | RedTeam skill | (separate skill) |

**Quick heuristic:** Has a "better answer" → Debate. Need a sanity check → Quick. Has "no answer, only structure" → Roundtable.

## Quick Reference

| Workflow | Purpose | Rounds | Output | User in loop? |
|----------|---------|--------|--------|---------------|
| **DEBATE** | Find best path among options | 3 (fixed) | Complete transcript + synthesis | No |
| **QUICK** | Fast perspective check | 1 (fixed) | Initial positions + go/no-go | No |
| **ROUNDTABLE** | Map the shape of a question | User-controlled | Knowledge network + open questions | Yes (可/止/深入/引入) |

## Core Philosophy

**Origin:** Best decisions emerge from diverse perspectives challenging each other. Not just collecting opinions — genuine intellectual friction where experts respond to each other's actual points.

- **Debate** is collaborative-adversarial: friction to converge on a recommendation
- **Quick** is parallel-assessment: fast multi-angle check
- **Roundtable** is exploratory-adversarial: friction to reveal the structure of the problem

**Speed:** Parallel execution within rounds, sequential between rounds. A 3-round debate of 4 agents = 12 agent calls but only 3 sequential waits.

## Examples

```
"Council: Should we use WebSockets or SSE?"
→ DEBATE workflow → 3-round transcript

"Quick council check: Is this API design reasonable?"
→ QUICK workflow → Fast perspectives

"Council with security: Evaluate this auth approach"
→ DEBATE with Security agent added

"圓桌：文學作品能否成為 agent skill？"
→ ROUNDTABLE workflow → Interactive multi-round exploration
```

## Integration

**Works well with:**
- **RedTeam** — Pure adversarial attack after collaborative discussion
- **Development** — Before major architectural decisions
- **Research** — Gather context before convening the council

## Best Practices

1. Use QUICK for sanity checks, DEBATE for important decisions, ROUNDTABLE for open questions
2. Add domain-specific experts as needed (security for auth, etc.)
3. Review the transcript — insights are in the responses, not just positions
4. Trust multi-agent convergence in DEBATE; trust divergence in ROUNDTABLE
5. In ROUNDTABLE: the open questions at the end are often more valuable than the discussion itself
