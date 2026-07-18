#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERNS = [
    re.compile(r"^\s+import\s+\w", re.MULTILINE),
    re.compile(r"^\s+from\s+\S+\s+import\s", re.MULTILINE),
]

_DENIAL = (
    "Local import on line {line} (import inside a function/method/class body). "
    "Move it to module level -- local imports hide circular dependency and "
    "missing-package errors. If it is genuinely necessary, the user must "
    "explicitly approve it and add it themselves."
)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class LocalImportGuardHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def evaluate(self, payload: PreToolUseHookPayload) -> None:
        if payload.tool_name not in ("Write", "Edit"):
            return
        file_path = payload.tool_input.get("file_path", "")
        if not file_path.endswith(".py"):
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
    LocalImportGuardHook().evaluate(payload)
