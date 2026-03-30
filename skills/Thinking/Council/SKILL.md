---
name: Council
description: Multi-perspective debate — auto-routes between decision-making (parallel agents) and thought exploration (real historical figures roundtable). USE WHEN council, debate, perspectives, weigh options, deliberate, roundtable, 辯論, 圓桌, 圓桌討論, 多角度, 討論一下, 幫我辯論, 探索這個議題.
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/PAI/USER/SKILLCUSTOMIZATIONS/Council/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## 🚨 MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the Council skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **Council** skill to ACTION...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# Council Skill

Multi-agent debate system where specialized agents discuss topics in rounds, respond to each other's points, and surface insights through intellectual friction.

**Key Differentiator from RedTeam:** Council is collaborative-adversarial (debate to find best path), while RedTeam is purely adversarial (attack the idea). Council produces visible conversation transcripts; RedTeam produces steelman + counter-argument.


## Workflow Routing

Auto-route based on the nature of the question:

| 判斷條件 | Workflow | 說明 |
|----------|----------|------|
| 有明確選項要選（A or B）、技術選型、產品決策、商業判斷 | `Workflows/Debate.md` | 平行 agent，快速決策，固定輪數 |
| 快速觀點檢查、sanity check | `Workflows/Quick.md` | 1 輪快速意見 |
| 哲學/社會/文化/概念性探索、沒有標準答案、思想性議題 | `Workflows/Roundtable.md` | 真實人物視角，用戶互動控制深度 |
| 純對抗性分析 | RedTeam skill | 攻擊想法 |

**路由邏輯：**
- 用戶明確說「圓桌」→ Roundtable
- 用戶明確說「quick」→ Quick
- 否則根據議題性質自動判斷：有選項/決策 → Debate，探索/開放性 → Roundtable

**輪數參數：**
- Debate: 預設 3 輪，可用 `N輪` 或 `rounds:N` 指定（如「council 5輪：該用哪個框架？」）
- Quick: 固定 1 輪
- Roundtable: 無上限，用戶互動控制（可/止/深入/加人）

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow in the **Council** skill to ACTION...
```

## Quick Reference

| Workflow | Purpose | Rounds | Output |
|----------|---------|--------|--------|
| **DEBATE** | 決策型結構討論 | 預設 3（可調） | Transcript + synthesis |
| **QUICK** | 快速觀點檢查 | 1 | Initial positions |
| **ROUNDTABLE** | 思想探索式圓桌 | 用戶控制 | 完整紀錄 + 知識網絡 + Obsidian 檔案 |

## Context Files

| File | Content |
|------|---------|
| `CouncilMembers.md` | Agent roles, perspectives, voice mapping |
| `RoundStructure.md` | Three-round debate structure and timing |
| `OutputFormat.md` | Transcript format templates |

## Core Philosophy

**Origin:** Best decisions emerge from diverse perspectives challenging each other. Not just collecting opinions - genuine intellectual friction where experts respond to each other's actual points.

**Speed:** Parallel execution within rounds, sequential between rounds. A 3-round debate of 4 agents = 12 agent calls but only 3 sequential waits. Complete in 30-90 seconds.

## Examples

```
"Council: Should we use WebSockets or SSE?"
-> Invokes DEBATE workflow -> 3-round transcript

"Quick council check: Is this API design reasonable?"
-> Invokes QUICK workflow -> Fast perspectives

"Council with security: Evaluate this auth approach"
-> DEBATE with Security agent added
```

## Integration

**Works well with:**
- **RedTeam** - Pure adversarial attack after collaborative discussion
- **Development** - Before major architectural decisions
- **Research** - Gather context before convening the council

## Best Practices

1. Use QUICK for sanity checks, DEBATE for important decisions
2. Add domain-specific experts as needed (security for auth, etc.)
3. Review the transcript - insights are in the responses, not just positions
4. Trust multi-agent convergence when it occurs

---

**Last Updated:** 2025-12-20
