#!/usr/bin/env python3
import json
import re
import sys

_CLASS_HEADER = re.compile(r"^(\s*)class\s+\w+\s*\(([^)]*)\)\s*:\s*$")
_MEMBER_ASSIGN = re.compile(
    r"^(\s+)([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['\"])((?:(?!\3).)*)\3\s*$"
)

_REASON = (
    "'{name} = \"{value}\"' on line {line} could just be '{name} = auto()' -- "
    "StrEnum's auto() already produces the lower-cased member name, so the "
    "literal is redundant. Use auto() (from enum import auto) unless the "
    "value must differ from name.lower(), e.g. it comes from an external "
    "schema/API and needs an exact case or format."
)


def evaluate(payload: dict[str, object]) -> None:
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return
    if tool_name == "Write":
        content = str(tool_input.get("content", ""))
    elif tool_name == "Edit":
        content = str(tool_input.get("new_string", ""))
    else:
        return
    if not str(tool_input.get("file_path", "")).endswith(".py"):
        return

    lines = content.splitlines()
    for index, line in enumerate(lines):
        header = _CLASS_HEADER.match(line)
        if header is None or "StrEnum" not in header.group(2):
            continue
        class_indent = len(header.group(1))
        for offset, member_line in enumerate(lines[index + 1 :], start=1):
            if member_line.strip() == "":
                continue
            indent = len(member_line) - len(member_line.lstrip(" "))
            if indent <= class_indent:
                break
            match = _MEMBER_ASSIGN.match(member_line)
            if match is None:
                continue
            name, value = match.group(2), match.group(4)
            if value != name.lower():
                continue
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": _REASON.format(
                                name=name, value=value, line=index + offset + 1
                            ),
                        }
                    }
                )
            )
            return


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
