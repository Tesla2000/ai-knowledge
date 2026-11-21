## Finishing a task

Before reporting a task as done, always run the full pre-commit suite on the repository (`uv run pre-commit run --all-files`), fix every issue it reports, and re-run until it passes. Do not report the task as done while any hook still fails.
