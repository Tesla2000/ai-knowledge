#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_ADVICE = (
    "File name '{filename}' duplicates its parent package name '{parent_dir}' "
    "(redundant word(s): {overlap}). The directory already provides that context "
    "-- rename to '{suggestion}' instead of repeating the package name in the file."
)


class PostToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str | bool]

    def string_field(self, key: str) -> str:
        value = self.tool_input.get(key, "")
        return value if isinstance(value, str) else ""


class RedundantNameAdvisorHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def evaluate(self, payload: PostToolUseHookPayload) -> None:
        if payload.tool_name not in ("Write", "Edit"):
            return
        file_path = payload.string_field("file_path")
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
    payload = PostToolUseHookPayload.model_validate_json(sys.stdin.read())
    RedundantNameAdvisorHook().evaluate(payload)
