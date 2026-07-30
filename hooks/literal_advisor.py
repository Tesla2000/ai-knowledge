#!/usr/bin/env python3
import json
import re
import sys

_LITERAL_START = re.compile(r"\bLiteral\[")

_ADVICE = (
    "Literal[...] with {count} elements added at line {line}: prefer an Enum "
    "for a multi-value Literal -- it gives a named type, exhaustiveness "
    "checking via match/case + assert_never, and one place to add or rename "
    "members. Only keep a multi-element Literal when an Enum is not viable "
    "(e.g. matching an external API's exact string constants, or a Pydantic "
    "discriminator field)."
)


def _string_field(tool_input: dict[str, object], key: str) -> str:
    value = tool_input.get(key, "")
    return value if isinstance(value, str) else ""


def _count_literal_elements(body: str) -> int:
    depth = 0
    quote: str | None = None
    escaped = False
    element_count = 1 if body.strip() else 0
    for char in body:
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"":
            quote = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            element_count += 1
    return element_count


def _find_close_bracket(content: str, open_index: int) -> int | None:
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(open_index, len(content)):
        char = content[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"":
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return index
    return None


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

    for match in _LITERAL_START.finditer(content):
        open_index = match.end() - 1
        close_index = _find_close_bracket(content, open_index)
        if close_index is None:
            continue
        body = content[open_index + 1 : close_index]
        element_count = _count_literal_elements(body)
        if element_count > 1:
            line = content[: match.start()].count("\n") + 1
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PostToolUse",
                            "additionalContext": _ADVICE.format(
                                count=element_count, line=line
                            ),
                        }
                    }
                )
            )
            return


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
