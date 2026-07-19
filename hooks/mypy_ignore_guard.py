#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERN = re.compile(r"#\s*type:\s*ignore", re.MULTILINE)

_DENIAL = (
    "# type: ignore on line {line}: report the mypy error instead of suppressing it. "
    "If suppression is genuinely necessary, the user must explicitly approve it and "
    "add it themselves."
)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class MypyIgnoreGuardHook(BaseModel):
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
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": _DENIAL.format(line=line),
                        }
                    }
                )
            )


if __name__ == "__main__":
    payload = PreToolUseHookPayload.model_validate_json(sys.stdin.read())
    MypyIgnoreGuardHook().evaluate(payload)
