## Finishing a task

Before reporting a task as done, run pre-commit only on the files modified in this session, with `uv run pre-commit run --files <file> ...`. If the session only touched test files, run it on those test files only. Fix every issue it reports, and re-run until it passes. Do not run `--all-files`, and do not report the task as done while any hook still fails.
