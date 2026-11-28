# Migrating a project off `ai-knowledge`

This guide is written for an agent or a person working in a project that still has
`Tesla2000/ai-knowledge` as its `.claude` submodule. Follow it in order, on a branch.
Do not add changes to `ai-knowledge`.

## 0. Check whether you need this

```
grep -A2 'submodule ".claude"' .gitmodules
```

If this prints `url = ...ai-knowledge.git`, the project needs this migration. If it prints
nothing, the project is already on the new setup.

## 1. Keep the project-specific files

Anything in `.claude/` that is specific to this project must survive the migration. Copy it
out of the old submodule first, into a temporary folder. Typical project-specific items:

- rules you wrote for this project (`.claude/rules/*.md`, outside any `shared/`),
- project skills, agents and commands (`.claude/skills/`, `.claude/agents/`, `.claude/commands/`),
- project hook scripts you added yourself,
- the project's own settings in `.claude/settings.json` (permissions, model, theme, and so on).

Do not copy the shared content back in. Hooks, skills, agents, commands and rules that came
from `ai-knowledge` now come from the new submodules.

## 2. Remove the old submodule

```
git rm --cached .claude
git config --file .gitmodules --remove-section 'submodule..claude' 2>/dev/null || true
rm -rf .claude/.git .git/modules/.claude
```

Then remove any `[submodule ".claude"]` block still left in `.gitmodules`, and commit that
removal before the next step.

## 3. Add the five shared submodules

```
git submodule add -b main git@github.com:Tesla2000/agentic-hooks.git .claude/shared/hooks
git submodule add -b main git@github.com:Tesla2000/agentic-skills.git .claude/shared/skills
git submodule add -b main git@github.com:Tesla2000/agentic-agents.git .claude/shared/agents
git submodule add -b main git@github.com:Tesla2000/agentic-commands.git .claude/shared/commands
git submodule add -b main git@github.com:Tesla2000/agentic-rules.git .claude/rules/shared
```

Each submodule must end up as a submodule entry (`git ls-tree HEAD .claude/shared` shows
`160000 commit` lines). If `git add` reports "adding embedded git repository" instead, the
submodule was not registered: remove that path from the index and run `git submodule add` again.

## 4. Write `.claude/settings.json`

Enable the four plugins and register their marketplaces. Keep your project's own settings in
the same file:

```json
{
  "extraKnownMarketplaces": {
    "agentic-hooks": {"source": {"source": "directory", "path": "./.claude/shared/hooks"}},
    "agentic-skills": {"source": {"source": "directory", "path": "./.claude/shared/skills"}},
    "agentic-agents": {"source": {"source": "directory", "path": "./.claude/shared/agents"}},
    "agentic-commands": {"source": {"source": "directory", "path": "./.claude/shared/commands"}}
  },
  "enabledPlugins": {
    "agentic-hooks@agentic-hooks": true,
    "agentic-skills@agentic-skills": true,
    "agentic-agents@agentic-agents": true,
    "agentic-commands@agentic-commands": true
  }
}
```

Remove any old `hooks` block that pointed at `.claude/hooks/*`. The plugin provides those hooks
now, and keeping the old block runs every hook twice. Project-only hooks go in a `hooks` block
of their own, and they run alongside the plugin hooks.

## 5. Remove the old copies

Delete the shared content that now comes from the submodules: `.claude/hooks/`,
`.claude/skills/` (except the project-only skills you kept in step 1), `.claude/agents/`,
`.claude/commands/`, `.claude/topics/`, `.claude/scripts/`, `.claude/index.md`. Do not touch
`.claude/rules/shared/`, because that is now a submodule.

Copy the project-only files you kept in step 1 back into place.

## 6. Move user-level instructions into the project

If `.claude/CLAUDE.md` holds personal instructions that apply to every project, add them as
`.claude/rules/<name>.md` with `paths: ["**"]`, then delete `.claude/CLAUDE.md`. The same goes
for `.claude/rules/finishing.md`-style rules: they belong in the project's `.claude/rules/`.

Memories are not shared. Do not move them into any `agentic-*` repository. A project's memories
and `CLAUDE.md` content stay with that project.

## 7. Use the current devcontainer

If the project has a `.devcontainer` submodule, it must point at the merged `main` of
`Tesla2000/devcontainer`, which no longer sets `CLAUDE_CONFIG_DIR`. Rebuild the container.
Without that change, `claude plugin install` writes to the read-only project `settings.json`
and fails with `EBUSY`.

## 8. Verify

```
git submodule status        # five agentic-* submodules, no .claude entry
claude plugin list          # the four agentic-* plugins are enabled
```

In a new session, check that a shared hook runs. For example, the guard hook rejects an edit
to `tests/` from a session whose name starts with `implementation`.

Then run pre-commit on the files you changed, as the project's rules require.

## Notes for agents

- The devcontainer mounts `.claude/settings.json` read-only. You cannot edit it from inside
  the container. Ask a person to edit it on the host, or use `settings.local.json` for
  machine-local settings.
- A directory-marketplace plugin is copied into the plugin cache. After a shared submodule
  changes, run `claude plugin marketplace update agentic-<name>`, or bump `version` in the
  plugin's `plugin.json`.
- Changes that apply to every project go to the matching `agentic-*` repository. Changes that
  apply to one project stay in that project.
