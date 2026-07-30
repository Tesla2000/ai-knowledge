#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _pytest_guard import (  # noqa: E402
    PytestRunRecord,
    hash_working_tree,
    is_pytest_command,
    save_record,
)

_FAILURE_PATTERN = re.compile(r"=+ .*\d+ failed")


def record_result(payload: dict[str, object], repo_root: Path) -> None:
    tool_input = payload.get("tool_input", {})
    command = str(tool_input.get("command", "")) if isinstance(tool_input, dict) else ""
    if payload.get("tool_name") != "Bash" or not is_pytest_command(command):
        return
    tool_response = payload.get("tool_response", {})
    if not isinstance(tool_response, dict):
        tool_response = {}
    stdout = str(tool_response.get("stdout", ""))
    stderr = str(tool_response.get("stderr", ""))
    output = stdout + stderr
    current_hash = hash_working_tree(repo_root)
    save_record(
        repo_root / ".claude" / "hooks" / ".pytest_state.json",
        PytestRunRecord(
            code_hash=current_hash,
            passed=not _FAILURE_PATTERN.search(output),
            output=output,
        ),
    )


if __name__ == "__main__":
    record_result(json.loads(sys.stdin.read()), Path(__file__).parent.parent.parent)
