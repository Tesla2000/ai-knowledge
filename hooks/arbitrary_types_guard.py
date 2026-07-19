#!/usr/bin/env python3
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERN = re.compile(r"arbitrary_types_allowed\s*=\s*True", re.MULTILINE)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class ArbitraryTypesGuardHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def evaluate(self, payload: PreToolUseHookPayload) -> None:
        if payload.tool_name not in ("Write", "Edit"):
            return
        if not payload.tool_input.get("file_path", "").endswith(".py"):
            return
        if payload.tool_name == "Write":
            content = payload.tool_input.get("content", "")
        else:
            content = payload.tool_input.get("new_string", "")

        m = _PATTERN.search(content)
        if m:
            line = content[: m.start()].count("\n") + 1
            sys.stderr.write(
                f"WARNING: arbitrary_types_allowed=True on line {line}. "
                "Prefer InstanceOf[T] for non-Pydantic fields rather than "
                "relaxing type constraints.\n"
            )


if __name__ == "__main__":
    payload = PreToolUseHookPayload.model_validate_json(sys.stdin.read())
    ArbitraryTypesGuardHook().evaluate(payload)
