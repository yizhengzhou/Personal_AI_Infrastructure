# /dump — 自由腦倒

Inspired by breferrari/obsidian-mind's /dump command.

User will narrate freely — meetings, decisions, ideas, discoveries, wins, frustrations — all mixed together. Your job is to **parse, classify, and route** each piece to the correct location.

## Procedure

1. Read the user's entire dump without interrupting
2. Classify each piece into categories:
   - **Decision** → Create or update note in `~/Documents/YZ-Brain/wiki/` or relevant project doc
   - **Idea** → Create note in `~/Documents/YZ-Brain/inbox/`
   - **Learning/Discovery** → Add to relevant wiki article or create new one in `~/Documents/YZ-Brain/wiki/`
   - **Feedback about june** → Save as feedback memory in `~/.claude/projects/-Users-zhyz--claude/memory/`
   - **Project update** → Update relevant project notes
   - **Personal reflection** → Add to `~/Documents/YZ-Brain/inbox/` with appropriate title
3. For each piece:
   - Create/update the note with proper frontmatter and wikilinks
   - Use `[[wikilink]]` syntax for cross-references
4. After processing, output a summary:
   ```
   📥 腦倒處理完成
   - 📋 N 個決策記錄
   - 💡 N 個想法捕捉
   - 📚 N 個學習記錄
   - 🔗 N 個連結建立
   ```

## Rules
- Never ask clarifying questions during dump processing — just do your best
- Use Traditional Chinese for filenames and content
- Every note must have at least one `[[wikilink]]` to another note
- Frontmatter must include `date`, `tags`, and `source: dump`
