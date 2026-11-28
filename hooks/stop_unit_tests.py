#!/usr/bin/env python3
import subprocess
import sys
import tempfile
from pathlib import Path

from guard_file_edits import FileGuard
from stop_gate import StopGate


class UnitTestGate(StopGate):
    GATE_NAME: str = "unit-tests"
    PYTEST_COMMAND: tuple[str, ...] = ("uv", "run", "pytest", "tests/unit", "-q", "-x")

    @classmethod
    def run(cls) -> None:
        hook_input = cls.read_input()
        session_id = str(hook_input.get("session_id", "unknown"))
        transcript_path = str(hook_input.get("transcript_path", ""))
        if FileGuard.IMPLEMENTATION not in FileGuard.session_roles(
            session_id, transcript_path
        ):
            sys.exit(0)
        with tempfile.TemporaryDirectory() as directory:
            output_file = Path(directory) / "pytest.out"
            with output_file.open("w") as output:
                result = subprocess.run(
                    cls.PYTEST_COMMAND,
                    cwd=cls.project_dir(),
                    stdout=output,
                    stderr=subprocess.STDOUT,
                )
            report = output_file.read_text()
        if result.returncode == 0:
            cls.reset_failures(session_id)
            sys.exit(0)
        cls.block(session_id, "Unit tests", report)


if __name__ == "__main__":
    UnitTestGate.run()
