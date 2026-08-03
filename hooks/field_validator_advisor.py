#!/usr/bin/env python3
import json
import re
import sys

_FIELD_VALIDATOR_DECORATOR = re.compile(r"@field_validator\b")

_ADVICE = (
    "@field_validator usage at line {line}: this is fishy in this codebase. "
    "Prefer Annotated[BaseClass, BeforeValidator(...)/AfterValidator(...)] (optionally "
    "with Field) as a reusable NewType instead. @field_validator is only acceptable "
    "when: (1) validation calls classmethods of a class, (2) validation applies to "
    "all fields via mode=\"before\" and a wildcard \"*\", or (3) many subclasses are "
    "expected to override it. Confirm which exception applies with the human overseer "
    "before keeping this decorator."
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

    match = _FIELD_VALIDATOR_DECORATOR.search(content)
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
