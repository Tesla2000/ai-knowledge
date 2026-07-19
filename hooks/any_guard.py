#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERNS = [
    re.compile(r"\btyping\.Any\b"),
    re.compile(r"from\s+typing\s+import\b[^#\n]*\bAny\b"),
    re.compile(r":\s*Any\b"),
    re.compile(r"->\s*Any\b"),
    re.compile(r"\[\s*Any\b"),
]

_DENIAL = (
    "typing.Any on line {line}: Any is banned outright -- it defeats the purpose of "
    "type checking entirely. Use object, a specific type, or a Protocol instead. "
    "The user will not approve Any in any shape or form."
)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class AnyGuardHook(BaseModel):
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

        for p in _PATTERNS:
            m = p.search(content)
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
                return


if __name__ == "__main__":
    payload = PreToolUseHookPayload.model_validate_json(sys.stdin.read())
    AnyGuardHook().evaluate(payload)
