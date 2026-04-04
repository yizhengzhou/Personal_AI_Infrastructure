# PAI (Personal AI Infrastructure) 專案分析報告

本報告旨在概述 PAI 專案的目的、技術細節與核心架構，由 Antigravity 整理。

## 1. 專案目的與核心目標
**PAI (Personal AI Infrastructure)** 是一個開源項目，由 Daniel Miessler 發起。其核心理念是 **「AI 應該放大每個人，而不僅僅是頂層的 1%」**。

- **願景**：激活人類的創造力。PAI 認為大多數人擁有未被開發的潛力，而 AI 可以作為催化劑，幫助個人識別、表達並追求生命意義。
- **定位**：PAI 不僅是一個聊天機器人（Chatbot），而是一個 **個人的數字助理（DA）系統**。它具有持久記憶、學習能力，並且專注於使用者的長期目標（Goal-oriented）而非僅僅是單次的指令任務（Task-oriented）。
- **使命**：提供一個可持續進化的個人 AI 平台，讓 AI 基礎設施對每個人都觸手可及。

## 2. 技術架構與細節
PAI 採用了模組化且具備高度擴展性的架構，核心技術棧如下：

### 核心驅動
- **Claude Code Native**：PAI 完全基於 Anthropic 的 Claude Code 構建，利用其 Hook 系統、MCD (Model Context Protocol) 以及強大的 Agentic 能力作為基礎引擎。

### 開發語言與運作環境
- **TypeScript**：主要的邏輯開發語言，用於編寫技能（Skills）、工具（Tools）與推論邏輯。
- **Bun**：作為高效的執行環境與套件管理器，主要用於執行 `.ts` 腳本（例如 `BuildCLAUDE.ts`）。
- **Bash**：用於安裝、平台檢測、自動化工作流（Workflows）以及與系統底層交互（如音訊播放、通知發送）。

### 關鍵組件（Primitives）
- **TELOS (Deep Goal Understanding)**：核心文件組（如 `MISSION.md`, `GOALS.md`, `BELIEFS.md` 等），記錄使用者的目標與價值觀，為 DA 提供深層背景。
- **技能系統 (Skill System)**：包含數十種專項技能，分為多個階層（Categories），確定的輸出優於隨機生成。
- **Hook 系統**：在會話開始（SessionStart）、工具使用、任務完成等生命週期事件觸發自動化動作。
- **記憶系統 (Memory System)**：捕獲每一步的反饋、情緒與結果，持續學習並優化未來的反應。
- **安全掛鉤 (Security Hook)**：在指令執行前進行驗證，確保安全而不犧牲流暢度。

### 第三方整合
- **聲音系統**：整合 **ElevenLabs (TTS)** 與 Google Cloud TTS，讓 AI 具備自然的人聲反饋。
- **通知系統**：支援 **ntfy (mobile)**, **Discord**, 以及 macOS 系統原生通知。

## 3. 跨平台支持
- **macOS**：原生開發與支援的首選平台。
- **Linux**：社群支援度高，已解決多項相容性問題（如 `sed` 文法、音訊播放器等）。
- **Windows**：目前尚不支持（主要是路徑與 shell 環境差異），待社群貢獻。

## 4. 專案特色
1. **User/System 分離**：使用者的配置存在 `USER/` 目錄，系統邏輯在 `SYSTEM/` 或 `.claude/PAI/`，升級時不會覆蓋使用者個人資料。
2. **科學方法論**：內部遵循「觀察 → 思考 → 計畫 → 執行 → 驗證 → 學習 → 改進」的完整算法（The Algorithm）。
3. **終端介面 (CLI) 導向**：強調 CLI 的速度與腳本化能力，並透過豐富的狀態列（Statusline）提供直觀的反饋。

---
*本報告已歸檔至專案目錄：`/Volumes/NEWXYZ/macOS_data_mirror/Project/Personal_AI_Infrastructure/project_analysis.md`*
