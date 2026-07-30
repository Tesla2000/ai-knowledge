#!/usr/bin/env python3
import json
import sys
from pathlib import Path

_ADVICE = (
    "File name '{filename}' duplicates its parent package name '{parent_dir}' "
    "(redundant word(s): {overlap}). The directory already provides that context "
    "-- rename to '{suggestion}' instead of repeating the package name in the file."
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
    file_path = _string_field(tool_input, "file_path")
    if not file_path.endswith(".py"):
        return

    path = Path(file_path)
    stem_words = [w for w in path.stem.lstrip("_").split("_") if w]
    dir_words = [w for w in path.parent.name.split("_") if w]
    if not dir_words:
        return

    dir_word_set = set(dir_words)
    stem_word_set = set(stem_words)
    if not dir_word_set.issubset(stem_word_set):
        return

    remainder = [w for w in stem_words if w not in dir_word_set]
    suggestion = "_" + "_".join(remainder) + ".py" if remainder else "a non-redundant name"
    sys.stdout.write(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": _ADVICE.format(
                        filename=path.name,
                        parent_dir=path.parent.name,
                        overlap=", ".join(dir_words),
                        suggestion=suggestion,
                    ),
                }
            }
        )
    )


if __name__ == "__main__":
    evaluate(json.loads(sys.stdin.read()))
