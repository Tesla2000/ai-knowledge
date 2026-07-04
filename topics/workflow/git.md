# Git & Dependency Workflow

## Rules

- Never commit unless explicitly asked.
- Never `git add` unless explicitly asked.
- Never skip hooks (`--no-verify`, `--no-gpg-sign`).
- Always use `uv add <package>` when adding a new dependency. Never edit pyproject.toml manually for deps.
- Never use `# type: ignore[import-not-found]`. Add the package or create stub files.

## Adding a dependency

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # dev / test only
```

## New files

New files that belong in the repo should be staged with `git add` -- but only when
the user asks to commit or add to git.

## Related

- [imports.md](../python/imports.md) -- stub files for untyped packages
