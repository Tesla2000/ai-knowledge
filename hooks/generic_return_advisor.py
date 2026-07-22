#!/usr/bin/env python3
import json
import re
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_DEF_GENERIC = re.compile(r"\bdef\s+(\w+)\[")

_ADVICE = (
    "Generic method '{name}' at line {line}: type parameter '{param}' isn't "
    "reflected in the return type (-> {return_annotation}). If it only types "
    "one input with no typed output, consider dropping the generic and using "
    "the bound type directly instead of a TypeVar. Keep it generic only for a "
    "valid use, e.g. constraining two or more parameters to agree with each "
    "other (as in FightCharacter[SlotT] attacker/defender checks) -- this "
    "hook already stays silent on that shape, so if you're seeing this, "
    "that's probably not what's happening here."
)


class PostToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str | bool]

    def string_field(self, key: str) -> str:
        value = self.tool_input.get(key, "")
        return value if isinstance(value, str) else ""


class BracketMatcher(BaseModel):
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
            elif char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
                if depth == 0:
                    return index
        return None

    def find_top_level_colon(self, start_index: int) -> int | None:
        depth = 0
        quote: str | None = None
        escaped = False
        for index in range(start_index, len(self.content)):
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
            elif char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
            elif char == ":" and depth == 0:
                return index
        return None


class TopLevelSplitter(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    body: str

    def split(self) -> list[str]:
        segments: list[str] = []
        current: list[str] = []
        depth = 0
        quote: str | None = None
        escaped = False
        for char in self.body:
            if quote is not None:
                current.append(char)
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                continue
            if char in "'\"":
                quote = char
                current.append(char)
                continue
            if char in "([{":
                depth += 1
                current.append(char)
            elif char in ")]}":
                depth -= 1
                current.append(char)
            elif char == "," and depth == 0:
                segments.append("".join(current))
                current = []
            else:
                current.append(char)
        tail = "".join(current).strip()
        if tail:
            segments.append(tail)
        return segments


class TypeParamNameExtractor(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    segment: str

    def name(self) -> str:
        text = self.segment.strip().lstrip("*").strip()
        for stop in (":", "="):
            index = text.find(stop)
            if index != -1:
                text = text[:index]
        return text.strip()


class GenericMethodCandidate(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    content: str
    name: str
    def_start: int
    open_bracket_index: int

    def evaluate(self) -> tuple[str, str, str] | None:
        matcher = BracketMatcher(content=self.content)
        close_bracket_index = matcher.find_close_index(self.open_bracket_index)
        if close_bracket_index is None:
            return None
        type_params_body = self.content[
            self.open_bracket_index + 1 : close_bracket_index
        ]
        type_param_names = [
            TypeParamNameExtractor(segment=segment).name()
            for segment in TopLevelSplitter(body=type_params_body).split()
        ]
        type_param_names = [name for name in type_param_names if name]
        if not type_param_names:
            return None

        paren_index = self._skip_whitespace(close_bracket_index + 1)
        if paren_index is None or self.content[paren_index] != "(":
            return None
        close_paren_index = matcher.find_close_index(paren_index)
        if close_paren_index is None:
            return None
        params_body = self.content[paren_index + 1 : close_paren_index]
        param_segments = TopLevelSplitter(body=params_body).split()

        return_annotation = self._extract_return_annotation(
            matcher, close_paren_index
        )
        if return_annotation is None:
            return None

        for type_param_name in type_param_names:
            word = re.compile(r"\b" + re.escape(type_param_name) + r"\b")
            if word.search(return_annotation):
                continue
            used_in_params = sum(
                1 for segment in param_segments if word.search(segment)
            )
            if used_in_params >= 2:
                continue
            return self.name, type_param_name, return_annotation or "None"
        return None

    def _skip_whitespace(self, index: int) -> int | None:
        while index < len(self.content) and self.content[index] in " \t\n":
            index += 1
        return index if index < len(self.content) else None

    def _extract_return_annotation(
        self, matcher: BracketMatcher, close_paren_index: int
    ) -> str | None:
        cursor = self._skip_whitespace(close_paren_index + 1)
        if cursor is None:
            return None
        if self.content[cursor : cursor + 2] == "->":
            cursor = self._skip_whitespace(cursor + 2)
            if cursor is None:
                return None
            colon_index = matcher.find_top_level_colon(cursor)
            if colon_index is None:
                return None
            return self.content[cursor:colon_index].strip()
        if self.content[cursor] == ":":
            return ""
        return None


class GenericReturnAdvisorHook(BaseModel):
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

        for match in _DEF_GENERIC.finditer(content):
            candidate = GenericMethodCandidate(
                content=content,
                name=match.group(1),
                def_start=match.start(),
                open_bracket_index=match.end() - 1,
            )
            result = candidate.evaluate()
            if result is None:
                continue
            name, type_param_name, return_annotation = result
            line = content[: match.start()].count("\n") + 1
            sys.stdout.write(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PostToolUse",
                            "additionalContext": _ADVICE.format(
                                name=name,
                                line=line,
                                param=type_param_name,
                                return_annotation=return_annotation,
                            ),
                        }
                    }
                )
            )
            return


if __name__ == "__main__":
    payload = PostToolUseHookPayload.model_validate_json(sys.stdin.read())
    GenericReturnAdvisorHook().evaluate(payload)
