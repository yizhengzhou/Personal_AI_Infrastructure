## 開發驗證流程（Verification Protocol）

每次完成功能修改後，必須自證 code 可以運行。不要只說「應該可以了」。

### 三層驗證

**第一層：自動測試（每次改 code 必做）**
```bash
flutter test
```
- 所有既有測試必須通過
- 如果新增了功能，要寫對應的 unit test

**第二層：Simulator 驗證（涉及 UI 變更時必做）**
```bash
# 確認 simulator 在跑
xcrun simctl list devices booted

# 用 agent-device 操作驗證
npx agent-device open
npx agent-device snapshot -i          # 看畫面元素
npx agent-device press @eN            # 操作相關按鈕
npx agent-device screenshot           # 截圖存證
npx agent-device close
```
- 截圖保存到 `docs/verification/` 目錄
- 確認 UI 顯示正確、互動正常

**第三層：驗證報告（完成一個完整功能時做）**
在回覆中附上驗證摘要：
```
✅ 驗證報告
- flutter test: 全部通過 (N/N)
- Simulator 驗證: [描述操作了什麼、看到什麼]
- 截圖: docs/verification/YYYY-MM-DD-feature-name.png
```

### 什麼時候用哪一層

| 改動類型 | 第一層 | 第二層 | 第三層 |
|---------|--------|--------|--------|
| 純邏輯/model 修改 | ✅ | — | — |
| UI 微調（顏色、間距） | ✅ | ✅ | — |
| 新功能/新畫面 | ✅ | ✅ | ✅ |
| Bug 修復 | ✅ | ✅ | ✅ |
| 重構 | ✅ | — | — |

### 注意事項
- Hot reload 後等 1 秒再截圖，確保畫面穩定
- 如果 simulator 沒在跑，先用 `xcrun simctl boot "iPhone 16 Pro"` 啟動
- 不要偽造驗證結果 — 如果跑不過就說跑不過
