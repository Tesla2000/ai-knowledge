#!/usr/bin/env python3
import subprocess
import sys

from stop_gate import StopGate


class PrecommitGate(StopGate):
    GATE_NAME: str = "precommit"

    @classmethod
    def run(cls) -> None:
        hook_input = cls.read_input()
        session_id = str(hook_input.get("session_id", "unknown"))
        files = cls.edited_files(session_id)
        if not files:
            cls.reset_failures(session_id)
            sys.exit(0)
        result = subprocess.run(
            ["uv", "run", "pre-commit", "run", "--files", *files],
            cwd=cls.project_dir(),
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            cls.reset_failures(session_id)
            cls.clear_edits(session_id)
            sys.exit(0)
        cls.block(session_id, "pre-commit", result.stdout + result.stderr)


if __name__ == "__main__":
    PrecommitGate.run()
