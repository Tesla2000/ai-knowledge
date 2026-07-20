#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERNS = [
    re.compile(r"\scast\("),
    re.compile(r"\btyping\.cast\("),
    re.compile(r"from\s+typing\s+import\b[^#\n]*\bcast\b"),
]


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class CastGuardHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def evaluate(self, payload: PreToolUseHookPayload) -> None:
        if payload.tool_name == "Write":
            content = payload.tool_input.get("content", "")
        elif payload.tool_name == "Edit":
            content = payload.tool_input.get("new_string", "")
        else:
            return

        for p in _PATTERNS:
            m = p.search(content, re.MULTILINE)
            if m:
                line = content[: m.start()].count("\n") + 1
                reason = (
                    f"cast() on line {line}: remove it -- cast() creates a discrepancy "
                    "between static type checking and runtime behaviour. If it is "
                    "genuinely necessary, the user must explicitly approve it and add "
                    "it themselves."
                )
                sys.stdout.write(
                    json.dumps(
                        {
                            "hookSpecificOutput": {
                                "hookEventName": "PreToolUse",
                                "permissionDecision": "deny",
                                "permissionDecisionReason": reason,
                            }
                        }
                    )
                )
                return


if __name__ == "__main__":
    payload = PreToolUseHookPayload.model_validate_json(sys.stdin.read())
    CastGuardHook().evaluate(payload)
