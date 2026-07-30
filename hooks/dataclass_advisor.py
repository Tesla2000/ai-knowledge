#!/usr/bin/env python3
import json
import re
import sys

_DATACLASS_DECORATOR = re.compile(r"@(?:dataclasses\.)?dataclass\b")

_ADVICE = (
    "@dataclass usage at line {line}: dataclass is forbidden in this codebase. "
    "Use a frozen Pydantic BaseModel when you need validation, defaults, or "
    "mutable-looking fields with methods; use NamedTuple for a plain, "
    "fixed-arity immutable record with no validation."
)


def _string_field(tool_input: dict[str, object], key: str) -> str:
    value = tool_input.get(key, "")
    return value if isinstance(value, str) else ""


def evaluate(payload: dict[str, object]) -> None:
    tool_name = payload.get("tool_name")
    if tool_name not in ("Write", "Edit"):
        return
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return
    if not _string_field(tool_input, "file_path").endswith(".py"):
        return
    if tool_name == "Write":
        content = _string_field(tool_input, "content")
    else:
        content = _string_field(tool_input, "new_string")

    match = _DATACLASS_DECORATOR.search(content)
    if match is None:
        return
    line = content[: match.start()].count("\n") + 1
    sys.stdout.write(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": _ADVICE.format(line=line),
                }
            }
        )
    )


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
