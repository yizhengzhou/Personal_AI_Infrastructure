# The Notification System

**Notifications for PAI workflows and task execution.**

**IMPORTANT: Voice/TTS is disabled. Do NOT execute any curl commands to localhost:8888. No voice notifications.**

---

## Task Start Announcements

**When STARTING a task, output a text notification:**

```
[Doing what {PRINCIPAL.NAME} asked]...
```

**Skip for conversational responses** (greetings, acknowledgments, simple Q&A).

---

## Context-Aware Announcements

**Match your announcement to what {PRINCIPAL.NAME} asked.** Start with the appropriate gerund:

| {PRINCIPAL.NAME}'s Request | Announcement Style |
|------------------|-------------------|
| Question ("Where is...", "What does...") | "Checking...", "Looking up...", "Finding..." |
| Command ("Fix this", "Create that") | "Fixing...", "Creating...", "Updating..." |
| Investigation ("Why isn't...", "Debug this") | "Investigating...", "Debugging...", "Analyzing..." |
| Research ("Find out about...", "Look into...") | "Researching...", "Exploring...", "Looking into..." |

---

## Workflow Invocation Notifications

**For skills with `Workflows/` directories, use "Executing..." format:**

```
Executing the **WorkflowName** workflow within the **SkillName** skill...
```

**NEVER announce fake workflows:**
- If it's not listed in a skill's Workflow Routing, DON'T use "Executing" format
- For non-workflow tasks, use context-appropriate gerund

---

## When to Skip Notifications

**Always skip notifications when:**
- **Conversational responses** - Greetings, acknowledgments, simple Q&A
- **Skill has no workflows** - The skill has no `Workflows/` directory
- **Direct skill handling** - SKILL.md handles request without invoking a workflow file
- **Quick utility operations** - Simple file reads, status checks
- **Sub-workflows** - When a workflow calls another workflow (avoid double notification)

---

## External Notifications (Push, Discord)

**Beyond text notifications, PAI supports external notification channels:**

### Available Channels

| Channel | Service | Purpose | Configuration |
|---------|---------|---------|---------------|
| **ntfy** | ntfy.sh | Mobile push notifications | `settings.json → notifications.ntfy` |
| **Discord** | Webhook | Team/server notifications | `settings.json → notifications.discord` |
| **Desktop** | macOS native | Local desktop alerts | Always available |

### Smart Routing

Notifications are automatically routed based on event type:

| Event | Default Channels | Trigger |
|-------|------------------|---------|
| `taskComplete` | Text only | Normal task completion |
| `longTask` | ntfy | Task duration > 5 minutes |
| `backgroundAgent` | ntfy | Background agent completes |
| `error` | ntfy | Error in response |
| `security` | ntfy + Discord | Security alert |

### Configuration

Located in `~/.claude/settings.json`:

```json
{
  "notifications": {
    "ntfy": {
      "enabled": true,
      "topic": "kai-[random-topic]",
      "server": "ntfy.sh"
    },
    "discord": {
      "enabled": false,
      "webhook": "https://discord.com/api/webhooks/..."
    },
    "thresholds": {
      "longTaskMinutes": 5
    },
    "routing": {
      "taskComplete": [],
      "longTask": ["ntfy"],
      "backgroundAgent": ["ntfy"],
      "error": ["ntfy"],
      "security": ["ntfy", "discord"]
    }
  }
}
```

---

## Event Log Channel (events.jsonl)

PAI hooks emit structured events to `${PAI_DIR}/MEMORY/STATE/events.jsonl`. This is an append-only JSONL file where each line is a typed event. It serves as a unified observability channel that any process can consume by tailing or watching the file.

---

### Design Principles

1. **Fire and forget** - Notifications never block hook execution
2. **Fail gracefully** - Missing services don't cause errors
3. **Conservative defaults** - Avoid notification fatigue
4. **Duration-aware** - Only push for long-running tasks (>5 min)
