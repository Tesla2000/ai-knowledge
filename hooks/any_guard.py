#!/usr/bin/env python3
import json
import re
import sys

_PATTERNS = [
    re.compile(r"\btyping\.Any\b"),
    re.compile(r"from\s+typing\s+import\b[^#\n]*\bAny\b"),
    re.compile(r":\s*Any\b"),
    re.compile(r"->\s*Any\b"),
    re.compile(r"\[\s*Any\b"),
]

_DENIAL = (
    "typing.Any on line {line}: Any is banned outright -- it defeats the purpose of "
    "type checking entirely. Use object, a specific type, or a Protocol instead. "
    "The user will not approve Any in any shape or form."
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
