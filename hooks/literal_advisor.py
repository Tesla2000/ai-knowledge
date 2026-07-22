#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_LITERAL_START = re.compile(r"\bLiteral\[")

_ADVICE = (
    "Literal[...] with {count} elements added at line {line}: prefer an Enum "
    "for a multi-value Literal -- it gives a named type, exhaustiveness "
    "checking via match/case + assert_never, and one place to add or rename "
    "members. Only keep a multi-element Literal when an Enum is not viable "
    "(e.g. matching an external API's exact string constants, or a Pydantic "
    "discriminator field)."
)


class PostToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str | bool]

    def string_field(self, key: str) -> str:
        value = self.tool_input.get(key, "")
        return value if isinstance(value, str) else ""


class LiteralElementCounter(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    body: str

    def count(self) -> int:
        depth = 0
        quote: str | None = None
        escaped = False
        element_count = 1 if self.body.strip() else 0
        for char in self.body:
            if quote is not None:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                continue
            if char in "'\"":
                quote = char
            elif char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
            elif char == "," and depth == 0:
                element_count += 1
        return element_count


class LiteralBracketMatcher(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    content: str

    def find_close_index(self, open_index: int) -> int | None:
        depth = 0
        quote: str | None = None
        escaped = False
        for index in range(open_index, len(self.content)):
            char = self.content[index]
            if quote is not None:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                continue
            if char in "'\"":
                quote = char
            elif char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
                if depth == 0:
                    return index
        return None


class LiteralAdvisorHook(BaseModel):
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

        matcher = LiteralBracketMatcher(content=content)
        for match in _LITERAL_START.finditer(content):
            open_index = match.end() - 1
            close_index = matcher.find_close_index(open_index)
            if close_index is None:
                continue
            body = content[open_index + 1 : close_index]
            element_count = LiteralElementCounter(body=body).count()
            if element_count > 1:
                line = content[: match.start()].count("\n") + 1
                sys.stdout.write(
                    json.dumps(
                        {
                            "hookSpecificOutput": {
                                "hookEventName": "PostToolUse",
                                "additionalContext": _ADVICE.format(
                                    count=element_count, line=line
                                ),
                            }
                        }
                    )
                )
                return


if __name__ == "__main__":
    payload = PostToolUseHookPayload.model_validate_json(sys.stdin.read())
    LiteralAdvisorHook().evaluate(payload)
