#!/usr/bin/env python3
import json
import os
import sys
import tempfile
from pathlib import Path


class StopGate:
    GATE_NAME: str = "gate"
    MAX_FAILURES: int = 5
    OUTPUT_TAIL_LINES: int = 80
    STUCK_NOTE: str = (
        "If you are stuck and cannot fix this yourself, ask the user with "
        "AskUserQuestion instead of retrying. Asking does not trigger this validation."
    )

    @classmethod
    def read_input(cls) -> dict:
        try:
            hook_input = json.load(sys.stdin)
        except ValueError:
            return {}
        if not isinstance(hook_input, dict):
            return {}
        return hook_input

    @classmethod
    def project_dir(cls) -> Path:
        return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()

    @classmethod
    def counter_path(cls, session_id: str) -> Path:
        return Path(tempfile.gettempdir()) / f"claude-{cls.GATE_NAME}-{session_id}.count"

    @classmethod
    def edits_path(cls, session_id: str) -> Path:
        return Path(tempfile.gettempdir()) / f"claude-edited-{session_id}.txt"

    @classmethod
    def record_edit(cls, session_id: str, file_path: str) -> None:
        try:
            with cls.edits_path(session_id).open("a") as edits:
                edits.write(f"{file_path}\n")
        except OSError:
            pass

    @classmethod
    def edited_files(cls, session_id: str) -> list[str]:
        try:
            recorded = cls.edits_path(session_id).read_text().splitlines()
        except OSError:
            return []
        project = cls.project_dir()
        relative: set[str] = set()
        for entry in recorded:
            path = (project / entry).resolve()
            if path.is_file() and path.is_relative_to(project):
                relative.add(str(path.relative_to(project)))
        return sorted(relative)

    @classmethod
    def clear_edits(cls, session_id: str) -> None:
        cls.edits_path(session_id).unlink(missing_ok=True)

    @classmethod
    def log_path(cls, session_id: str) -> Path:
        return Path(tempfile.gettempdir()) / f"claude-{cls.GATE_NAME}-{session_id}.log"

    @classmethod
    def save_output(cls, session_id: str, output: str) -> Path:
        path = cls.log_path(session_id)
        try:
            path.write_text(output)
        except OSError:
            pass
        return path

    @classmethod
    def failure_count(cls, session_id: str) -> int:
        try:
            return int(cls.counter_path(session_id).read_text())
        except (OSError, ValueError):
            return 0

    @classmethod
    def record_failure(cls, session_id: str) -> int:
        count = cls.failure_count(session_id) + 1
        try:
            cls.counter_path(session_id).write_text(str(count))
        except OSError:
            pass
        return count

    @classmethod
    def reset_failures(cls, session_id: str) -> None:
        cls.counter_path(session_id).unlink(missing_ok=True)
        cls.log_path(session_id).unlink(missing_ok=True)

    @classmethod
    def tail(cls, output: str) -> str:
        return "\n".join(output.splitlines()[-cls.OUTPUT_TAIL_LINES :])

    @classmethod
    def block(cls, session_id: str, title: str, output: str) -> None:
        attempt = cls.record_failure(session_id)
        log_path = cls.save_output(session_id, output)
        if attempt > cls.MAX_FAILURES:
            print(
                f"{title} still failing after {cls.MAX_FAILURES} attempts; "
                "letting the model stop. Tell the user the check is failing.",
                file=sys.stderr,
            )
            sys.exit(0)
        print(
            f"{title} failed (attempt {attempt}/{cls.MAX_FAILURES}). "
            "Fix the issues below before stopping.\n\n"
            f"{cls.tail(output)}\n\n"
            f"Full output saved to {log_path} (read it if the tail above is not enough).\n"
            f"{cls.STUCK_NOTE}",
            file=sys.stderr,
        )
        sys.exit(2)
