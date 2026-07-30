#!/usr/bin/env python3
import json
import re
import sys

_CHECKS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\bhasattr\s*\(", re.MULTILINE),
        "hasattr() on line {line}: use isinstance() or structural typing (Protocol) instead",
    ),
    (
        re.compile(r"\bgetattr\s*\(", re.MULTILINE),
        "getattr() on line {line}: prefer direct attribute access or a Protocol with the attribute",
    ),
    (
        re.compile(r"\bprint\s*\(", re.MULTILINE),
        "print() on line {line}: use logging -- print leaks into production output",
    ),
    (
        re.compile(r"\bpatch(?!\.)\s*\(", re.MULTILINE),
        "patch() on line {line}: use patch.object(target, target.method.__name__, autospec=True) instead of bare patch()",
    ),
    (
        re.compile(r'\bpatch\.object\s*\([^,]+,\s*["\']', re.MULTILINE),
        "patch.object() string arg on line {line}: second argument is a string literal -- use target.method.__name__ instead. If unavoidable the user must approve.",
    ),
]


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

    for pattern, message_template in _CHECKS:
        m = pattern.search(content)
        if m:
            line = content[: m.start()].count("\n") + 1
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": message_template.format(
                                line=line
                            ),
                        }
                    }
                )
            )
            return


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
