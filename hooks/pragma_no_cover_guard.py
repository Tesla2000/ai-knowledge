#!/usr/bin/env python3
import json
import re
import sys

_PATTERN = re.compile(r"#\s*pragma:\s*no\s*cover", re.MULTILINE)

_DENIAL = (
    "# pragma: no cover on line {line}: banned. Coverage exclusions belong in "
    "[tool.coverage.report] exclude_lines in pyproject.toml, not inline. "
    "The project already excludes assert_never, case _ as never:, "
    "if TYPE_CHECKING:, ..., and pass."
)


def evaluate(payload: dict[str, object]) -> None:
    tool_name = payload.get("tool_name")
    if tool_name not in ("Write", "Edit"):
        return
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return
    if not str(tool_input.get("file_path", "")).endswith(".py"):
        return
    if tool_name == "Write":
        content = str(tool_input.get("content", ""))
    else:
        content = str(tool_input.get("new_string", ""))

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
    evaluate(json.loads(sys.stdin.read()))
