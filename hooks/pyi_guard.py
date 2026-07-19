#!/usr/bin/env python3
import json
import sys
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

_DENIAL = (
    "Creating .pyi stub files is forbidden for Claude. "
    ".pyi files must be created by the user directly. "
    "If type stubs for a package are missing, add them as additional_dependencies "
    "to the mypy hook in .pre-commit-config.yaml using the manage script:\n"
    "  python3 .claude/scripts/manage_precommit_deps.py add <stub-package>\n"
    "  (e.g. types-requests, pandas-stubs, boto3-stubs)\n"
    "To remove a stub package:\n"
    "  python3 .claude/scripts/manage_precommit_deps.py remove <stub-package>\n"
    "Direct modification of .pre-commit-config.yaml is forbidden -- always use the manage script."
)


class PreToolUseHookPayload(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    tool_name: str
    tool_input: dict[str, str]


class PyiGuardHook(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    def evaluate(self, payload: PreToolUseHookPayload) -> None:
        if payload.tool_name != "Write":
            return
        if not payload.tool_input.get("file_path", "").endswith(".pyi"):
            return
        sys.stdout.write(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": _DENIAL,
                    }
                }
            )
        )


if __name__ == "__main__":
    payload = PreToolUseHookPayload.model_validate_json(sys.stdin.read())
    PyiGuardHook().evaluate(payload)
