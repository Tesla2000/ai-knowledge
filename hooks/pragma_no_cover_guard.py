#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERN = re.compile(r"#\s*pragma:\s*no\s*cover", re.MULTILINE)

_DENIAL = (
    "# pragma: no cover on line {line}: banned. Coverage exclusions belong in "
    "[tool.coverage.report] exclude_lines in pyproject.toml, not inline. "
    "The project already excludes assert_never, case _ as never:, "
    "if TYPE_CHECKING:, ..., and pass."
)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class PragmaNoCoverGuardHook(BaseModel):
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
    PragmaNoCoverGuardHook().evaluate(payload)
