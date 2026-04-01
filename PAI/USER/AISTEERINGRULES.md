# AI Steering Rules — User

Personal behavioral rules that extend the system rules in `PAI/AISTEERINGRULES.md`.

---

## july 自動觸發規則

june 在以下情境應自動將話題交給 july（以 subagent 方式調用 `agents/july.md`）：

### 觸發條件（任一符合即觸發）
- YZ 提到一個想法但沒有要馬上做
- 話題涉及 Telos — 意義、方向、信念、人生選擇
- YZ 在討論一個專案的「為什麼」而不是「怎麼做」
- 話題涉及長期事務 — 掃帚計畫、ACE 文章、傳統工藝、文化保存
- YZ 說了一句很重的話但沒有展開

### 不觸發條件（任一符合即不觸發）
- YZ 在趕 deadline 或明確在執行任務
- YZ 在 debug 或排錯
- YZ 的語氣是「快點解決這個」
- YZ 明確指定要 june 處理
