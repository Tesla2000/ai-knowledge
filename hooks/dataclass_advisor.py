#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_DATACLASS_DECORATOR = re.compile(r"@(?:dataclasses\.)?dataclass\b")

_ADVICE = (
    "@dataclass usage at line {line}: dataclass is forbidden in this codebase. "
    "Use a frozen Pydantic BaseModel when you need validation, defaults, or "
    "mutable-looking fields with methods; use NamedTuple for a plain, "
    "fixed-arity immutable record with no validation."
)


class PostToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str | bool]

    def string_field(self, key: str) -> str:
        value = self.tool_input.get(key, "")
        return value if isinstance(value, str) else ""


class DataclassAdvisorHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def evaluate(self, payload: PostToolUseHookPayload) -> None:
        if payload.tool_name not in ("Write", "Edit"):
            return
        if not payload.string_field("file_path").endswith(".py"):
            return
        if payload.tool_name == "Write":
            content = payload.string_field("content")
        else:
            content = payload.string_field("new_string")

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
    payload = PostToolUseHookPayload.model_validate_json(sys.stdin.read())
    DataclassAdvisorHook().evaluate(payload)
