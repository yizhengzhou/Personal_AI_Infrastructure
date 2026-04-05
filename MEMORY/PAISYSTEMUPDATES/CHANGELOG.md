# PAI System Updates Changelog

> 所有 PAI 系統架構變更的唯一紀錄。位置遵循 MEMORYSYSTEM.md 規範。
> 路徑：`~/.claude/MEMORY/PAISYSTEMUPDATES/CHANGELOG.md`

---

## 2026-04-04 (Session 2)

### Obsidian Mind 機制移植

**來源：** [breferrari/obsidian-mind](https://github.com/breferrari/obsidian-mind) — 一個用 Obsidian vault 做 Claude Code 長期記憶的系統。

**移植了三個機制：**

1. **UserPromptSubmit 分類 hook** — 每則訊息自動偵測類型（決策/想法/反饋/人物/學習），注入路由提示讓 AI 知道該存到哪裡
   - Script: `~/.claude/hooks/classify-message.sh`
   - 純文字匹配，無 LLM 呼叫，<100ms

2. **Vault-first memory 原則** — CLAUDE.md 新增規則：所有持久知識存在 YZ-Brain vault，memory files 只存指標
   - 決策 → `wiki/` 或專案文檔
   - 想法 → `inbox/`
   - 學習 → `wiki/`

3. **/dump 指令** — 自由腦倒，一口氣說完，AI 自動分類、歸檔、建立 wikilink
   - Command: `~/.claude/commands/dump.md`

**不移植的：** Performance graph、brag doc、review brief、Slack 整合（上班族績效管理，不適用一人公司）

---

### Batch Implementation（D1/D2/D3/D5 共 7 項）

**完成項目：**

| 項目 | 產出 |
|------|------|
| D3-1 Git Activity 每日收集 | `scripts/daily-git-activity.sh` + LaunchAgent 08:00 |
| D2-6 Business Knowledge Files | COMPANY.md, CLIENTS.md, COSTS.md |
| D5-1 Session-log 品質修復 | update-relationship.sh transcript path fallback |
| D1-6 Wiki 編譯引擎（Karpathy） | `scripts/wiki-compile.sh` + 10 篇文章 |
| D1-8 Wiki 索引維護 | `wiki/_index.md` 自動生成 |
| D1-10 Knowledge Linting | `scripts/wiki-lint.sh` |
| D1-LaunchAgent | `com.june-wiki-compile.plist` 09:30 daily |

**實作率：** 0% → 22%（7/32 項完成）

---

### Repo Consolidation

- `~/.claude/PAI/` 改為 symlink → `~/Documents/Project/Personal_AI_Infrastructure/PAI/`
- GitHub push: `b61f6a7`
- ABOUTME.md 從 git tracking 移除（PII 保護）
- DAIDENTITY.md 移除醫療細節

---

### Upstream Merge

- 合併上游 PAI 23 個 commit
- 新增 12 個 Skill Packs（47 sub-skills）
- PAI on Pi v1.0.0
- 學習文件：`~/Documents/YZ-Brain/learning/PAI-upstream-packs-guide.md`

---

### Morning Brief 擴充

- GitHub Trending 每日掃描（三方向：興趣主題、專案相關、熱門）
- 直接嵌入 `daily-brief.sh`，不需額外 LaunchAgent

---

## Dimensions Overview (Proactive Self-Learning Upgrade)

| Dimension | 主題 | 狀態 | Spec 位置 |
|-----------|------|------|-----------|
| D1 | 個人能力盤點 | ✅ Spec complete | `~/Documents/YZ-Brain/writing/project/ACE/spec-dimension1-personal-growth.md` |
| D2 | 公司規劃 fork.work Business | ✅ Spec complete | `~/.claude/MEMORY/WORK/20260404-130000_pai-proactive-self-learning-upgrade/specs/spec-dimension2-business.md` |
| D3 | 專案開發行銷 | ✅ Spec complete | `~/Documents/YZ-Brain/writing/project/ACE/spec-dimension3-projects.md` |
| D4 | 自由學習 AI 環境 | 📋 待規劃 — 與 D1/D2 密切相關 | — |
| D5 | June 自學能力 | ✅ Phase 1+2 complete | PRDs in `MEMORY/WORK/` |

---

## 2026-04-04

### D5 Phase 1: 基礎自學機制（PRD: `20260404-160000_june-self-learning-system`）

**狀態：✅ Complete（22/22 ISC）**

#### 變更清單

**新增檔案：**
| 檔案 | 用途 |
|------|------|
| `~/.claude/hooks/update-relationship.sh` | Stop hook — 自動更新 RELATIONSHIP 檔案 |
| `~/.claude/MEMORY/STATE/last-session-summary.md` | 跨 session 錨點（每次覆寫） |
| `~/.claude/.gitignore` | 安全稽核後建立，排除 secrets/PII/session data |
| `~/.claude/scripts/cleanup-old-sessions.sh` | 清理 >30 天的 session JSONL |

**修改檔案：**
| 檔案 | 變更 |
|------|------|
| `~/.claude/settings.json` | Stop hooks 新增 `update-relationship.sh`；contextFiles 新增 4 個檔案（interaction-patterns, last-session-summary, TELOS/BELIEFS, TELOS/GOALS） |
| `~/.claude/PAI/THEHOOKSYSTEM.md` | 加入 Reality Check 說明——標記文檔中的 hooks 大部分不存在 |
| `~/.claude/projects/-Users-zhyz--claude/memory/feedback_auto_relationship_update.md` | 從「LLM-dependent 軟規則」更新為「已實作 hard hook」 |

**系統操作：**
| 操作 | 結果 |
|------|------|
| `git init ~/.claude/` | 建立版本控制安全網（commit `c124e16`） |
| 安全稽核（Gemini） | 發現 12+ 處明文 API key，.gitignore 全部排除 |
| 清理 >30 天 session | 刪除 345 個檔案，釋放 50MB |

#### 技術決策（with Gemini Review）
1. Stop hook 讀 stdin JSON payload（含 session_id, transcript_path），不只用 env var
2. 從 transcript 擷取真實 Human 訊息片段作 topics，不用佔位符
3. session-log.md 不加入 contextFiles（會無限增長），改用 last-session-summary.md 單檔覆寫
4. TELOS 加 BELIEFS.md + GOALS.md（共 34 行），不加 README.md（模板）
5. interaction-patterns 統計式更新暫緩，先確保基礎可靠

#### 外部參考
- Hermes Agent（NousResearch/hermes-agent）自學機制分析
  - 可取：procedural memory（自動建 skill）、memory 容量管理
  - 不需要：memory 安全掃描（單人系統無攻擊面）
  - 已有覆蓋：session search（memsearch）、user modeling（DAIDENTITY+TELOS）

---

### D5 Phase 2: Memory 管理（待開始）

**範圍（規劃中）：**
- session-log rotate（只保留最近 N 條，舊的歸檔）
- memory files 容量警告
- 借鏡 Hermes 的 bounded memory + consolidation 機制

---

### 架構回歸：補齊 MEMORYSYSTEM.md 定義的目錄結構

**狀態：✅ Complete**

**原因：** 調查發現 MEMORYSYSTEM.md 定義了完整的 MEMORY/ 結構，但約 70% 的目錄從未建立。同時確認上游 PAI 沒有 master index 檔案——正確做法是遵循現有的 MEMORYSYSTEM.md 規範，不另創規則。

**新建目錄：**
- `MEMORY/PAISYSTEMUPDATES/2026/04/` — 系統變更紀錄（本檔案搬至此處）
- `MEMORY/LEARNING/SYSTEM/`、`ALGORITHM/`、`FAILURES/`、`SYNTHESIS/` — 學習子系統
- `MEMORY/LEARNING/SIGNALS/` — 評分信號
- `MEMORY/RESEARCH/` — 研究產出
- `MEMORY/SECURITY/` — 安全事件
- `MEMORY/STATE/` 子目錄 — algorithms, kitty-sessions, tab-titles, progress, integrity

**搬移：**
- `UPGRADE-LOG.md` 從 `MEMORY/WORK/` 搬至 `MEMORY/PAISYSTEMUPDATES/CHANGELOG.md`

**決策依據：** 上游 PAI 的 User/System 分離原則 + MEMORYSYSTEM.md 權威定義。不發明新規則，補齊現有規範。

---

### D5 Phase 2: Memory 容量管理（PRD: `20260404-180000_d5p2-memory-management`）

**狀態：✅ Complete（10/10 ISC）**

**修改檔案：**
| 檔案 | 變更 |
|------|------|
| `~/.claude/hooks/update-relationship.sh` | 加入 session-log rotate 邏輯（保留最近 20 條，舊的歸檔到 session-log-archive.md） |

**新增檔案：**
| 檔案 | 用途 |
|------|------|
| `~/Library/LaunchAgents/com.pai.monthly-session-cleanup.plist` | 每月 1 日 03:00 自動清理 >30 天的 session JSONL |

**設計決策：**
- session-log 保留 20 條（約 1 個月），超出的歸檔不刪除
- 清理 LaunchAgent 只刪 session JSONL（projects/ 下的 .jsonl），不動 memory files
- 遵循上游原則 #6「Code Before Prompts」——純 bash/python，不用 LLM
