#!/usr/bin/env python3
import json
import re
import sys

_PATTERN = re.compile(r"#\s*type:\s*ignore", re.MULTILINE)

_DENIAL = (
    "# type: ignore on line {line}: report the mypy error instead of suppressing it. "
    "If suppression is genuinely necessary, the user must explicitly approve it and "
    "add it themselves."
)


def evaluate(payload: dict[str, object]) -> None:
    tool_name = payload.get("tool_name")
    if tool_name not in ("Write", "Edit"):
        return
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return
    if not str(tool_input.get("file_path", "")).endswith(".py"):
        return
    if tool_name == "Write":
        content = str(tool_input.get("content", ""))
    else:
        content = str(tool_input.get("new_string", ""))

    m = _PATTERN.search(content)
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


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
