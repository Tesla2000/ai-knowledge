# ai-knowledge (deprecated)

This repository is **no longer supported**. Do not add it as a project's `.claude` submodule,
and do not add changes to it.

It was a single shared `.claude` folder (hooks, skills, agents, commands, rules and a
`CLAUDE.md`) that every project pulled in as one submodule. That design mixed shared and
project-specific config, and it put Claude's runtime state inside the project.

## Replacement

Shared config now comes from five submodules, one per element type. Each project adds them
when it is initialised:

| Repository | Mounted at | Provides |
|---|---|---|
| [agentic-hooks](https://github.com/Tesla2000/agentic-hooks) | `.claude/shared/hooks` | plugin: hooks |
| [agentic-skills](https://github.com/Tesla2000/agentic-skills) | `.claude/shared/skills` | plugin: skills |
| [agentic-agents](https://github.com/Tesla2000/agentic-agents) | `.claude/shared/agents` | plugin: agents |
| [agentic-commands](https://github.com/Tesla2000/agentic-commands) | `.claude/shared/commands` | plugin: commands |
| [agentic-rules](https://github.com/Tesla2000/agentic-rules) | `.claude/rules/shared` | rules |

Project-specific config stays in the project's own `.claude/`. Memories and project `CLAUDE.md`
content are never shared unless someone explicitly asks.

**To migrate a project, follow [MIGRATION.md](MIGRATION.md).**
