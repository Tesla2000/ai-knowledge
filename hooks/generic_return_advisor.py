#!/usr/bin/env python3
import json
import re
import sys

_DEF_GENERIC = re.compile(r"\bdef\s+(\w+)\[")

_ADVICE = (
    "Generic method '{name}' at line {line}: type parameter '{param}' isn't "
    "reflected in the return type (-> {return_annotation}). If it only types "
    "one input with no typed output, consider dropping the generic and using "
    "the bound type directly instead of a TypeVar. Keep it generic only for a "
    "valid use, e.g. constraining two or more parameters to agree with each "
    "other (as in FightCharacter[SlotT] attacker/defender checks) -- this "
    "hook already stays silent on that shape, so if you're seeing this, "
    "that's probably not what's happening here."
)


def _string_field(tool_input: dict[str, object], key: str) -> str:
    value = tool_input.get(key, "")
    return value if isinstance(value, str) else ""


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
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
            if depth == 0:
                return index
    return None


def _find_top_level_colon(content: str, start_index: int) -> int | None:
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(start_index, len(content)):
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
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == ":" and depth == 0:
            return index
    return None


def _split_top_level(body: str) -> list[str]:
    segments: list[str] = []
    current: list[str] = []
    depth = 0
    quote: str | None = None
    escaped = False
    for char in body:
        if quote is not None:
            current.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"":
            quote = char
            current.append(char)
            continue
        if char in "([{":
            depth += 1
            current.append(char)
        elif char in ")]}":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            segments.append("".join(current))
            current = []
        else:
            current.append(char)
    tail = "".join(current).strip()
    if tail:
        segments.append(tail)
    return segments


def _type_param_name(segment: str) -> str:
    text = segment.strip().lstrip("*").strip()
    for stop in (":", "="):
        index = text.find(stop)
        if index != -1:
            text = text[:index]
    return text.strip()


def _skip_whitespace(content: str, index: int) -> int | None:
    while index < len(content) and content[index] in " \t\n":
        index += 1
    return index if index < len(content) else None


def _extract_return_annotation(content: str, close_paren_index: int) -> str | None:
    cursor = _skip_whitespace(content, close_paren_index + 1)
    if cursor is None:
        return None
    if content[cursor : cursor + 2] == "->":
        cursor = _skip_whitespace(content, cursor + 2)
        if cursor is None:
            return None
        colon_index = _find_top_level_colon(content, cursor)
        if colon_index is None:
            return None
        return content[cursor:colon_index].strip()
    if content[cursor] == ":":
        return ""
    return None


def _evaluate_generic_method(
    content: str, name: str, open_bracket_index: int
) -> tuple[str, str, str] | None:
    close_bracket_index = _find_close_bracket(content, open_bracket_index)
    if close_bracket_index is None:
        return None
    type_params_body = content[open_bracket_index + 1 : close_bracket_index]
    type_param_names = [
        name
        for name in (
            _type_param_name(segment)
            for segment in _split_top_level(type_params_body)
        )
        if name
    ]
    if not type_param_names:
        return None

    paren_index = _skip_whitespace(content, close_bracket_index + 1)
    if paren_index is None or content[paren_index] != "(":
        return None
    close_paren_index = _find_close_bracket(content, paren_index)
    if close_paren_index is None:
        return None
    params_body = content[paren_index + 1 : close_paren_index]
    param_segments = _split_top_level(params_body)

    return_annotation = _extract_return_annotation(content, close_paren_index)
    if return_annotation is None:
        return None

    for type_param_name in type_param_names:
        word = re.compile(r"\b" + re.escape(type_param_name) + r"\b")
        if word.search(return_annotation):
            continue
        used_in_params = sum(1 for segment in param_segments if word.search(segment))
        if used_in_params >= 2:
            continue
        return name, type_param_name, return_annotation or "None"
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

    for match in _DEF_GENERIC.finditer(content):
        result = _evaluate_generic_method(content, match.group(1), match.end() - 1)
        if result is None:
            continue
        name, type_param_name, return_annotation = result
        line = content[: match.start()].count("\n") + 1
        sys.stdout.write(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": _ADVICE.format(
                            name=name,
                            line=line,
                            param=type_param_name,
                            return_annotation=return_annotation,
                        ),
                    }
                }
            )
        )
        return


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
