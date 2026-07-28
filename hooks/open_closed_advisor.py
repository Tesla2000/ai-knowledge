#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_ADVICE = (
    "{file_path} was already committed before this edit. Before moving on, judge "
    "whether this specific change expands an existing class to accommodate "
    "something new (e.g. a bolted-on field, especially a nullable one) instead of "
    "solving it architecturally -- a new subclass, composition, or similar. "
    "Extending an Enum, adding a match/case arm, adding a member to an AnyX "
    "union, a genuine bugfix, or any other change you judge necessary is fine "
    "as-is. This fires on every edit to a committed file regardless of what "
    "changed, so most of the time there's nothing wrong -- just take a moment to "
    "check this one on its merits; no need to ask the user."
)


class PostToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str | bool]

    def string_field(self, key: str) -> str:
        value = self.tool_input.get(key, "")
        return value if isinstance(value, str) else ""


class CommittedFileChecker(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def is_committed(self, file_path: str) -> bool:
        path = Path(file_path)
        cwd = path.parent if path.is_absolute() else Path.cwd()
        toplevel = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if toplevel.returncode != 0:
            return False
        repo_root = Path(toplevel.stdout.strip())
        relative_path = path.relative_to(repo_root) if path.is_absolute() else path
        result = subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{relative_path.as_posix()}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0


class OpenClosedAdvisorHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def evaluate(self, payload: PostToolUseHookPayload) -> None:
        if payload.tool_name not in ("Write", "Edit"):
            return
        file_path = payload.string_field("file_path")
        if not file_path.endswith(".py"):
            return
        path = Path(file_path)
        if (
            "tests" in path.parts
            or path.name.startswith("test_")
            or path.name.endswith("_test.py")
        ):
            return

        if not CommittedFileChecker().is_committed(file_path):
            return

        sys.stdout.write(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "additionalContext": _ADVICE.format(file_path=file_path),
                    }
                }
            )
        )


if __name__ == "__main__":
    payload = PostToolUseHookPayload.model_validate_json(sys.stdin.read())
    OpenClosedAdvisorHook().evaluate(payload)
