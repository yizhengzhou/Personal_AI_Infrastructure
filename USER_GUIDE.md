# PAI (Personal AI Infrastructure) 使用手冊

## 1. PAI 是什麼？
PAI 是您個人的 **AI 基礎設施輔助系統**，運行於 Claude Code 之上。它讓 Claude Code 在每次啟動時都了解您的情況（目標、習慣、學習紀錄），不再是一個「失憶」的工具。

> **PAI 不是聊天機器人**，它是一個「知道你是誰」的 AI 代理人。

---

## 2. 如何啟動 PAI
在您的終端機輸入：
```bash
pai
```
這會啟動 Claude Code，並自動載入 PAI 的上下文（您的身份、習慣、學習記錄）。

---

## 3. 如何與 PAI 互動（用自然語言說就好）

PAI 不是靠 slash command 使用的，而是**用自然語言描述您的需求**，它會自動路由到對應的技能。以下是幾個實用範例：

### 📚 學習紀錄整理
啟動 PAI 後，對它說：
```
請幫我整理 Learnings/Daily/2026-03-07.md 的學習筆記，
抓出核心概念並幫我產生一份摘要
```

### 📋 每週學習彙整
```
請分析 Learnings/Daily/ 資料夾中本週的筆記，
列出我這週學到的主要技術概念與待解問題
```

### 💡 深化理解
```
我今天學了 XXX 的概念，請幫我用具體例子解釋清楚，
並告訴我還有哪些相關知識我應該了解
```

---

## 4. 學習紀錄的目錄結構
```
Personal_AI_Infrastructure/
├── Learnings/
│   ├── Daily/          ← 每天的學習筆記（用 Obsidian 撰寫）
│   │   ├── TEMPLATE.md ← 複製這個模板開始記錄
│   │   └── 2026-03-07.md
│   └── Summaries/      ← PAI 幫您整理的週/月彙整報告
└── PAI_USER/           ← 您的個人 AI 設定（TELOS、GOALS 等）
    └── TELOS/          ← 您的長期目標文件
```

---

## 5. 個人化 PAI（選做）
如果您想讓 PAI 更了解您，可以用 Obsidian 編輯 `PAI_USER/TELOS/` 下的文件：
- **MISSION.md**：您的長期使命或現階段最重要的事
- **GOALS.md**：目前正在追求的具體目標

這些文件一旦填寫，PAI 在協助您整理學習筆記時，會更有針對性地找出與您目標相關的知識連結。

---

## 6. 每日工作流（建議）

```
[早上/白天] → 用 Obsidian 撰寫學習筆記到 Learnings/Daily/YYYY-MM-DD.md
[任何時刻] → 打開終端機執行 pai，請它整理、深化或延伸您的筆記
[每週]     → 請 PAI 彙整本週學習摘要到 Learnings/Summaries/
```

---

*已歸檔於專案目錄：`Personal_AI_Infrastructure/USER_GUIDE.md`*
