# DEPRECATED: do not add this repository as `.claude`

This repository is no longer supported. Projects must not use it as their `.claude` submodule.
Shared agentic config now comes from five submodules, one per element type:

- `Tesla2000/agentic-hooks` -> `.claude/shared/hooks` (plugin)
- `Tesla2000/agentic-skills` -> `.claude/shared/skills` (plugin)
- `Tesla2000/agentic-agents` -> `.claude/shared/agents` (plugin)
- `Tesla2000/agentic-commands` -> `.claude/shared/commands` (plugin)
- `Tesla2000/agentic-rules` -> `.claude/rules/shared` (rules, loaded automatically)

If the project you are working in still has this repository as `.claude`, read
[MIGRATION.md](MIGRATION.md) in this repository and follow it before making other changes.
Do not add content to this repository.

## Finishing a task

Before reporting a task as done, run pre-commit only on the files modified in this session, with `uv run pre-commit run --files <file> ...`. If the session only touched test files, run it on those test files only. Fix every issue it reports, and re-run until it passes. Do not run `--all-files`, and do not report the task as done while any hook still fails.
