#!/bin/bash
# UserPromptSubmit hook — classify incoming message and inject routing hints
# Inspired by breferrari/obsidian-mind's UserPromptSubmit classification hook
# Lightweight: pure text matching, no LLM call, <100ms

INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    msg = data.get('message', '')
    if isinstance(msg, dict):
        msg = msg.get('content', '')
    if isinstance(msg, list):
        for block in msg:
            if isinstance(block, dict) and block.get('type') == 'text':
                msg = block['text']
                break
    print(str(msg)[:500])
except:
    print('')
" 2>/dev/null)

[ -z "$MESSAGE" ] && exit 0

# Classify by keyword patterns
HINTS=""

# Decision detection
if echo "$MESSAGE" | grep -qiE '決定|decided|decision|選擇|choose|we.ll go with|確定要|不做了|改成'; then
    HINTS+="[DECISION detected — consider recording in YZ-Brain/wiki/ or MEMORY] "
fi

# Idea/insight detection
if echo "$MESSAGE" | grep -qiE '我想到|idea|突然想|靈感|如果我們|what if|maybe we|也許可以'; then
    HINTS+="[IDEA detected — consider capturing in YZ-Brain/inbox/] "
fi

# Feedback/correction detection
if echo "$MESSAGE" | grep -qiE '不要這樣|不對|錯了|wrong|don.t do|stop doing|不准|以後別'; then
    HINTS+="[FEEDBACK detected — consider saving as feedback memory] "
fi

# Person mention detection
if echo "$MESSAGE" | grep -qiE '跟.*聊|meeting with|見了|talked to|說他|told me'; then
    HINTS+="[PERSON/MEETING detected — consider noting context] "
fi

# Learning/discovery detection
if echo "$MESSAGE" | grep -qiE '學到|discovered|發現|原來|turns out|TIL|才知道'; then
    HINTS+="[LEARNING detected — consider adding to wiki or memory] "
fi

# Output hints if any were detected
if [ -n "$HINTS" ]; then
    echo "$HINTS"
fi
