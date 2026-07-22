#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_PATTERN = re.compile(r"^[ \t]*match\s+\S.*:[ \t]*$", re.MULTILINE)

_ADVICE = (
    "match statement added at line {line}: match should only be used to prove "
    "exhaustiveness over an enum/union (paired with a final case _: that asserts "
    "unreachability, e.g. \"case _ as never: assert_never(never)\"). For ordinary "
    "conditional branching, use if/elif instead -- it is less verbose and does not "
    "imply an exhaustiveness guarantee."
)


class PostToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str | bool]

    def string_field(self, key: str) -> str:
        value = self.tool_input.get(key, "")
        return value if isinstance(value, str) else ""


class MatchStatementAdvisorHook(BaseModel):
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

        m = _PATTERN.search(content)
        if m:
            line = content[: m.start()].count("\n") + 1
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
    MatchStatementAdvisorHook().evaluate(payload)
