#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


class FileGuard:
    IMPLEMENTATION: str = "implementation"
    TEST: str = "test"
    TEST_TDD: str = "test-tdd"
    TESTS_DIR: str = "tests"
    UNIT_DIR: str = "unit"
    CONFIG_DIR: str = ".claude"
    TITLE_TYPE: str = "custom-title"

    @classmethod
    def project_dir(cls) -> Path:
        return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()

    @classmethod
    def relative_parts(cls, file_path: str) -> tuple[str, ...] | None:
        project = cls.project_dir()
        target = (project / file_path).resolve()
        try:
            return target.relative_to(project).parts
        except ValueError:
            return None

    @classmethod
    def session_role(cls, session_id: str, transcript_path: str) -> str | None:
        title: object = None
        try:
            with open(transcript_path, encoding="utf-8") as transcript:
                for line in transcript:
                    if cls.TITLE_TYPE not in line:
                        continue
                    try:
                        entry = json.loads(line)
                    except ValueError:
                        continue
                    if (
                        isinstance(entry, dict)
                        and entry.get("type") == cls.TITLE_TYPE
                        and entry.get("sessionId") == session_id
                    ):
                        title = entry.get("customTitle")
        except OSError:
            return None
        if not isinstance(title, str):
            return None
        name = title.lower()
        if name.startswith(cls.IMPLEMENTATION):
            return cls.IMPLEMENTATION
        if name.startswith(cls.TEST_TDD):
            return cls.TEST_TDD
        if name.startswith(cls.TEST):
            return cls.TEST
        return None

    @classmethod
    def blocked_reason(cls, hook_input: object) -> str | None:
        if not isinstance(hook_input, dict):
            return None
        tool_input = hook_input.get("tool_input")
        if not isinstance(tool_input, dict):
            return None
        file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
        if not isinstance(file_path, str) or not file_path:
            return None
        session_id = hook_input.get("session_id")
        transcript_path = hook_input.get("transcript_path")
        if not isinstance(session_id, str) or not isinstance(transcript_path, str):
            return None
        role = cls.session_role(session_id, transcript_path)
        parts = cls.relative_parts(file_path)
        if parts is not None and parts[:1] == (cls.CONFIG_DIR,):
            return None
        in_tests = parts is not None and parts[:1] == (cls.TESTS_DIR,)
        in_unit = parts is not None and parts[:2] == (cls.TESTS_DIR, cls.UNIT_DIR)
        if role == cls.IMPLEMENTATION and in_tests:
            return (
                f"Blocked: the implementation role may not modify {cls.TESTS_DIR}/. "
                "Tests are the spec. Change production code under dnd/ instead, "
                "and report any test that looks wrong without editing it."
            )
        if role == cls.TEST_TDD and not in_unit:
            return (
                f"Blocked: test-tdd sessions may only modify files under {cls.TESTS_DIR}/{cls.UNIT_DIR}/. "
                "Leave production code and other test folders alone and report what needs changing."
            )
        if role == cls.TEST and not in_tests:
            return (
                f"Blocked: the test role may only modify files under {cls.TESTS_DIR}/. "
                "Leave production code alone and report what needs changing."
            )
        return None


if __name__ == "__main__":
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    reason = FileGuard.blocked_reason(hook_input)
    if reason is not None:
        print(reason, file=sys.stderr)
        sys.exit(2)
