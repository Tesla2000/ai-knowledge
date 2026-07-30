#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

_ADVICE = (
    "{file_path} was already committed before this edit. Before moving on, judge "
    "whether this specific change expands an existing class to accommodate "
    "something new (e.g. a bolted-on field, especially a nullable one) instead of "
    "solving it architecturally -- a new subclass, composition, or similar. "
    "Extending an Enum, adding a match/case arm, adding a member to an AnyX "
    "union, a genuine bugfix, or any other change you judge necessary is fine "
    "as-is. This fires on every edit to a committed file regardless of what "
    "changed, so most of the time there's nothing wrong -- just take a moment to "
    "check this one on its merits; no need to ask the user."
)


def _string_field(tool_input: dict[str, object], key: str) -> str:
    value = tool_input.get(key, "")
    return value if isinstance(value, str) else ""


def _is_committed(file_path: str) -> bool:
    path = Path(file_path)
    cwd = path.parent if path.is_absolute() else Path.cwd()
    toplevel = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if toplevel.returncode != 0:
        return False
    repo_root = Path(toplevel.stdout.strip())
    relative_path = path.relative_to(repo_root) if path.is_absolute() else path
    result = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{relative_path.as_posix()}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.returncode == 0


def evaluate(payload: dict[str, object]) -> None:
    tool_name = payload.get("tool_name")
    if tool_name not in ("Write", "Edit"):
        return
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return
    file_path = _string_field(tool_input, "file_path")
    if not file_path.endswith(".py"):
        return
    path = Path(file_path)
    if (
        "tests" in path.parts
        or path.name.startswith("test_")
        or path.name.endswith("_test.py")
    ):
        return

    if not _is_committed(file_path):
        return

    sys.stdout.write(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": _ADVICE.format(file_path=file_path),
                }
            }
        )
    )


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
