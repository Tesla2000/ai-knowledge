#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import ClassVar

sys.path.insert(0, str(Path(__file__).parent))

from _pytest_guard import (  # noqa: E402
    CodeStateHasher,
    PytestCommandMatcher,
    PytestGuardStateStore,
)
from pydantic import BaseModel, ConfigDict  # noqa: E402


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class PytestGuardPreHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    repo_root: Path

    def evaluate(self, payload: PreToolUseHookPayload) -> None:
        command = payload.tool_input.get("command", "")
        if payload.tool_name != "Bash" or not PytestCommandMatcher.is_pytest_command(
            command
        ):
            return
        current_hash = CodeStateHasher(repo_root=self.repo_root).hash_working_tree()
        state_store = PytestGuardStateStore(
            state_path=self.repo_root / ".claude" / "hooks" / ".pytest_state.json"
        )
        record = state_store.load()
        if record is None or record.code_hash != current_hash or record.passed:
            return
        sys.stdout.write(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            "pytest already failed against this exact code "
                            "state and nothing has changed since. Do not "
                            "re-run pytest with different parameters/flags "
                            "to try to get a different result — read "
                            "the saved failure output in "
                            ".claude/hooks/.pytest_state.json instead, and "
                            "make a code change before rerunning."
                        ),
                    }
                }
            )
        )


if __name__ == "__main__":
    payload = PreToolUseHookPayload.model_validate_json(sys.stdin.read())
    PytestGuardPreHook(repo_root=Path(__file__).parent.parent.parent).evaluate(payload)
