#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERN = re.compile(r"^\s+case\s+_\s*:", re.MULTILINE)

_DENIAL = (
    'Bare case _: on line {line}: use "case _ as never:" for exhaustive matching '
    "-- the binding name \"never\" is excluded from coverage in pyproject.toml "
    "and signals to the type checker that this branch is unreachable."
)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class BareWildcardMatchGuardHook(BaseModel):
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
    BareWildcardMatchGuardHook().evaluate(payload)
