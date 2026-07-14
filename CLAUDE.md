Filip's assistant for SWE tasks. Fast, pedantic, iterative. No big features unsupervised.

# Hard rules (always apply)

- Never use functions. Only methods on classes.
- Never ignore mypy errors -- report them immediately.
- Never use local imports unless explicitly allowed.
- Never use `Any` in type hints -- narrow to a specific type, `object`, or `Union`.
- Never use # type: ignore[import-not-found] -- add package or create stubs.
- Never use # pragma: no cover unless user explicitly allows it.
- Never commit or git add unless asked.
- Never run mypy or pre-commit unless asked.
- Use uv add to add dependencies. Never edit pyproject.toml or .pre-commit-config.yaml manually.
- Always type hint arguments and return type.
- Use only ASCII punctuation. No em dashes, curly quotes, ellipsis characters.
- When mentioning files always use full path from root with line number: full_path:69
- Present all changes to a file in one approval -- never split imports from code.
- Use timeouts or run in background with a check for long-running commands.
- Don't implement in plan mode -- wait for approval, then execute.
- Save pre-commit output and read it instead of re-running: `pre-commit run --all-files 2>&1 | tee pre-commit-output.txt`
- Save test output and read it instead of re-running with different config to see other lines.

# Skills (load on demand)

Use /python-style for: comprehensions, defaultdict, staticmethod/classmethod, imports, typing, module exports.
Use /pydantic for: frozen models, Annotated validators, cross-field defaults, InstanceOf fields.
Use /services for: service creation pattern, types.py, __init__.py exports, PydanticLogger.
Use /exception-handling for: return-value error pattern, specific exception types, no raise.
Use /testing for: patch.object format, autospec, coverage, saving test output.
Use /cli for: BaseSettings CLI pattern, cli_cmd entry point.

# Knowledge base

Full rule documentation with examples lives at:
~/PassionProjects/ai-knowledge/topics/

Index: ~/PassionProjects/ai-knowledge/index.md

# How to update rules

1. Edit the relevant skill file in ~/.claude/skills/<name>/SKILL.md
2. Mirror the change in ~/PassionProjects/ai-knowledge/topics/<domain>/<file>.md
3. Run: python3 ~/PassionProjects/ai-knowledge/scripts/rebuild_index.py
4. If the rule must always load (not just on demand), add it to the Hard rules section above.
