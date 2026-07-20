#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERN = re.compile(
    r"\b(dict|Mapping|MutableMapping|MappingProxyType|frozendict)\[str\s*,\s*object\]",
    re.MULTILINE,
)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class LeakyMappingGuardHook(BaseModel):
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
            type_name = m.group(1)
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": (
                                f"{type_name}[str, object] on line {line}: "
                                "undescriptive -- use a Pydantic model (strongly "
                                "preferred) or TypedDict to name the fields explicitly."
                            ),
                        }
                    }
                )
            )


if __name__ == "__main__":
    payload = PreToolUseHookPayload.model_validate_json(sys.stdin.read())
    LeakyMappingGuardHook().evaluate(payload)
