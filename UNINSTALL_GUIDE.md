# PAI 安裝變更記錄與解除安裝指南 (UNINSTALL_GUIDE.md)

如果您決定安裝 PAI，本文件將詳述系統對您的作業系統所做的每一項變更，並提供一份「一鍵清除」的腳本與手動移除指引，確保您的作業系統在不適用時能回復到最乾淨的狀態。

## 1. 安裝期間產生的變更清單

當執行 `install.sh` 與 `pai` 啟動後，以下檔案與設定會被建立：

### 檔案系統變更 (Directories & Files)
- **`~/.claude/`**：存放 PAI 的核心程式碼、技能、記憶與設定檔的主要目錄。
- **`~/.config/PAI/`**：存放敏感資訊（如 `.env` API 金鑰）的目錄。
- **`~/.env`** (Symlink)：指向 `~/.config/PAI/.env`，供語音伺服器讀取。
- **`~/.bun/`**：如果您原本沒安裝 Bun，安裝程式會建立此目錄（Bun Runtime）。

### 系統服務變更 (macOS Services)
- **`~/Library/LaunchAgents/com.pai.voice-server.plist`**：語音伺服器的自動啟動設定。
- **Port 8888**：語音伺服器會佔用此連接埠。

### Shell 設定 (Environment & Aliases)
- **`~/.zshrc` (或 `.bashrc`)**：
    - 加入一個名為 `pai` 的 alias。
    - 可能會加入 Bun 的 PATH 設定。

---

## 2. 乾淨移除方案

如果您想移除 PAI，我已經為您準備好了移除邏輯。您可以隨時請我執行以下步驟：

### 手動移除步驟 (懶人包)
1. **停止語音服務**：
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.pai.voice-server.plist 2>/dev/null
   rm ~/Library/LaunchAgents/com.pai.voice-server.plist
   lsof -ti:8888 | xargs kill -9
   ```
2. **刪除相關主目錄**：
   ```bash
   rm -rf ~/.claude
   rm -rf ~/.config/PAI
   rm ~/.env  # 僅刪除 symlink
   ```
3. **清理 Shell 設定**：
   開啟 `~/.zshrc`，刪除標註有 `# PAI alias` 的區塊。

---

## 3. 安全性評估
- **不可逆變更**：除了安裝全域 NPM 套件（如 `claude-code`）之外，PAI 的所有檔案都集中在專屬目錄中，具體路徑極為明確，具備高度的可移除性。
- **透明度**：所有的安裝動作都在 `Releases/v4.0.3/.claude/PAI-Install/engine/actions.ts` 中有紀錄，我隨時可以為您調閱原始碼確認。

**結論**：我可以幫您執行安裝並完整記錄過程（輸出至日誌檔）。PAI 的設計雖然「侵入」，但其實是非常「好聚好散」的，移除過程非常簡單且透明。
