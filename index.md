# DEPRECATED: this index is no longer maintained

Shared agentic config moved to `Tesla2000/agentic-*` submodules (see [MIGRATION.md](MIGRATION.md)).
Rules are loaded automatically from `.claude/rules/`, so this index is not needed.

# Knowledge Base Index (last version, not maintained)

| File | Summary |
|------|---------|
| [Imports](topics/python/imports.md) | - Never use local (inline) imports unless explicitly allowed by the supervisor. |
| [Python version](topics/python/python-version.md) | - The `requires-python` declared in `pyproject.toml` decides which syntax is allowed. Never raise |
| [Testing](topics/python/testing.md) | - Use pytest exclusively. |
| [Typing](topics/python/typing.md) | - Always type hint both arguments and return type. |
| [Workflow](topics/workflow.md) | - When a task is impossible as stated, stop and ask for clarification before reverting any changes. Do not silently roll back and mark the task done. |
