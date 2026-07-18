#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from typing import ClassVar

sys.path.insert(0, str(Path(__file__).parent))

from _pytest_guard import (  # noqa: E402
    CodeStateHasher,
    PytestCommandMatcher,
    PytestGuardStateStore,
    PytestRunRecord,
)
from pydantic import BaseModel, ConfigDict  # noqa: E402

_FAILURE_PATTERN = re.compile(r"=+ .*\d+ failed")


class PostToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]
    tool_response: dict[str, object]


class PytestGuardPostHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    repo_root: Path

    def record_result(self, payload: PostToolUseHookPayload) -> None:
        command = payload.tool_input.get("command", "")
        if payload.tool_name != "Bash" or not PytestCommandMatcher.is_pytest_command(
            command
        ):
            return
        stdout = str(payload.tool_response.get("stdout", ""))
        stderr = str(payload.tool_response.get("stderr", ""))
        output = stdout + stderr
        current_hash = CodeStateHasher(repo_root=self.repo_root).hash_working_tree()
        state_store = PytestGuardStateStore(
            state_path=self.repo_root / ".claude" / "hooks" / ".pytest_state.json"
        )
        state_store.save(
            PytestRunRecord(
                code_hash=current_hash,
                passed=not _FAILURE_PATTERN.search(output),
                output=output,
            )
        )


if __name__ == "__main__":
    payload = PostToolUseHookPayload.model_validate_json(sys.stdin.read())
    PytestGuardPostHook(repo_root=Path(__file__).parent.parent.parent).record_result(
        payload
    )
