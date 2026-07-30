#!/usr/bin/env python3
import json
import re
import sys

_PATTERN = re.compile(r"^[ \t]*match\s+\S.*:[ \t]*$", re.MULTILINE)

_ADVICE = (
    "match statement added at line {line}: match should only be used to prove "
    "exhaustiveness over an enum/union (paired with a final case _: that asserts "
    "unreachability, e.g. \"case _ as never: assert_never(never)\"). For ordinary "
    "conditional branching, use if/elif instead -- it is less verbose and does not "
    "imply an exhaustiveness guarantee."
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

    m = _PATTERN.search(content)
    if m:
        line = content[: m.start()].count("\n") + 1
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
