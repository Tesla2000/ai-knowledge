#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _pytest_guard import (  # noqa: E402
    hash_working_tree,
    is_pytest_command,
    load_record,
)


def evaluate(payload: dict[str, object], repo_root: Path) -> None:
    tool_input = payload.get("tool_input", {})
    command = str(tool_input.get("command", "")) if isinstance(tool_input, dict) else ""
    if payload.get("tool_name") != "Bash" or not is_pytest_command(command):
        return
    current_hash = hash_working_tree(repo_root)
    record = load_record(repo_root / ".claude" / "hooks" / ".pytest_state.json")
    if record is None or record.code_hash != current_hash or record.passed:
        return
    sys.stdout.write(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        "pytest already failed against this exact code "
                        "state and nothing has changed since. Do not "
                        "re-run pytest with different parameters/flags "
                        "to try to get a different result — read "
                        "the saved failure output in "
                        ".claude/hooks/.pytest_state.json instead, and "
                        "make a code change before rerunning."
                    ),
                }
            }
        )
    )


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()), Path(__file__).parent.parent.parent)
