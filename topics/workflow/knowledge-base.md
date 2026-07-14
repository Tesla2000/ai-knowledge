# Knowledge Base Maintenance

## Structure

```
~/.claude/CLAUDE.md                          # lean always-loaded rules + skill pointers
~/.claude/skills/<name>/SKILL.md             # domain rules loaded on demand via /<name>
~/PassionProjects/ai-knowledge/topics/       # full documentation with examples and rationale
~/PassionProjects/ai-knowledge/index.md      # auto-generated index (do not edit manually)
~/PassionProjects/ai-knowledge/scripts/rebuild_index.py
```

## When to put a rule where

| Where | When |
|-------|------|
| Hard rules in CLAUDE.md | Must apply in every session without being invoked |
| Skill SKILL.md | Domain-specific, loaded on demand with /<skill-name> |
| topics/ file | Full explanation, examples, rationale -- source of truth |

## How to add or update a rule

1. Edit the relevant skill file: `~/.claude/skills/<name>/SKILL.md`
2. Mirror the change in the corresponding topic file: `~/PassionProjects/ai-knowledge/topics/<domain>/<file>.md`
3. Rebuild the index: `python3 ~/PassionProjects/ai-knowledge/scripts/rebuild_index.py`
4. If the rule must always load (not just on demand), also add it to the Hard rules section in `~/.claude/CLAUDE.md`

## How to add a new skill

1. Create `~/.claude/skills/<name>/SKILL.md` with frontmatter:
   ```markdown
   ---
   name: <name>
   description: one-line summary of when to load this skill
   ---
   ```
2. Create a matching topic file in `~/PassionProjects/ai-knowledge/topics/<domain>/<name>.md`
3. Add a pointer to the Skills section in `~/.claude/CLAUDE.md`: `Use /<name> for: ...`
4. Rebuild the index.

## How to remove a rule

1. Delete or edit the skill file.
2. Delete or edit the topic file.
3. If it was in Hard rules, remove it from CLAUDE.md.
4. Rebuild the index.

## Index rebuild

The index is auto-generated from topic file headings and first paragraphs. Never edit it manually.

```bash
python3 ~/PassionProjects/ai-knowledge/scripts/rebuild_index.py
```

The GitHub Actions workflow (`.github/workflows/rebuild_index.yml`) also rebuilds it automatically
on every push that touches `topics/**/*.md`.
