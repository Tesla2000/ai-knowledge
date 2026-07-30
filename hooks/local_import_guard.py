#!/usr/bin/env python3
import json
import re
import sys

_PATTERNS = [
    re.compile(r"^\s+import\s+\w", re.MULTILINE),
    re.compile(r"^\s+from\s+\S+\s+import\s", re.MULTILINE),
]

_DENIAL = (
    "Local import on line {line} (import inside a function/method/class body). "
    "Move it to module level -- local imports hide circular dependency and "
    "missing-package errors. If it is genuinely necessary, the user must "
    "explicitly approve it and add it themselves."
)


def evaluate(payload: dict[str, object]) -> None:
    tool_name = payload.get("tool_name")
    if tool_name not in ("Write", "Edit"):
        return
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return
    file_path = str(tool_input.get("file_path", ""))
    if not file_path.endswith(".py"):
        return
    if tool_name == "Write":
        content = str(tool_input.get("content", ""))
    else:
        content = str(tool_input.get("new_string", ""))

    for p in _PATTERNS:
        m = p.search(content)
        if m:
            line = content[: m.start()].count("\n") + 1
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": _DENIAL.format(line=line),
                        }
                    }
                )
            )
            return


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
