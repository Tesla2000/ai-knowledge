#!/usr/bin/env python3
import json
import re
import sys

_PATTERNS = [
    re.compile(r"\scast\("),
    re.compile(r"\btyping\.cast\("),
    re.compile(r"from\s+typing\s+import\b[^#\n]*\bcast\b"),
]


def evaluate(payload: dict[str, object]) -> None:
    tool_name = payload.get("tool_name")
    if tool_name == "Write":
        content = str(payload.get("tool_input", {}).get("content", ""))
    elif tool_name == "Edit":
        content = str(payload.get("tool_input", {}).get("new_string", ""))
    else:
        return

    for p in _PATTERNS:
        m = p.search(content)
        if m:
            line = content[: m.start()].count("\n") + 1
            reason = (
                f"cast() on line {line}: remove it -- cast() creates a discrepancy "
                "between static type checking and runtime behaviour. If it is "
                "genuinely necessary, the user must explicitly approve it and add "
                "it themselves."
            )
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": reason,
                        }
                    }
                )
            )
            return


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
