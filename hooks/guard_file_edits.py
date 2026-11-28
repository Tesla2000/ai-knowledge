#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path


class FileGuard:
    ALL: str = "all"
    IMPLEMENTATION: str = "implementation"
    TEST: str = "test"
    TEST_TDD: str = "test-tdd"
    TESTS_DIR: str = "tests"
    UNIT_DIR: str = "unit"
    CONFIG_DIR: str = ".claude"
    TITLE_TYPE: str = "custom-title"
    ROLE_PATTERNS: tuple[tuple[str, str], ...] = (
        (ALL, r"(?<![a-z0-9])all"),
        (IMPLEMENTATION, r"(?<![a-z0-9])implementation"),
        (TEST_TDD, r"(?<![a-z0-9])test-tdd"),
        (TEST, r"(?<![a-z0-9])test(?!-tdd)"),
    )

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
    def session_roles(cls, session_id: str, transcript_path: str) -> frozenset[str]:
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
            return frozenset()
        if not isinstance(title, str):
            return frozenset()
        name = title.lower()
        return frozenset(
            role
            for role, pattern in cls.ROLE_PATTERNS
            if re.search(pattern, name) is not None
        )

    @classmethod
    def role_allows(cls, role: str, in_tests: bool, in_unit: bool) -> bool:
        if role == cls.ALL:
            return True
        if role == cls.IMPLEMENTATION:
            return not in_tests
        if role == cls.TEST_TDD:
            return in_unit
        return in_tests

    @classmethod
    def role_denial(cls, role: str) -> str:
        if role == cls.IMPLEMENTATION:
            return (
                f"the implementation role may not modify {cls.TESTS_DIR}/. "
                "Tests are the spec. Change production code instead, "
                "and report any test that looks wrong without editing it."
            )
        if role == cls.TEST_TDD:
            return (
                f"test-tdd sessions may only modify files under {cls.TESTS_DIR}/{cls.UNIT_DIR}/. "
                "Leave production code and other test folders alone and report what needs changing."
            )
        return (
            f"the test role may only modify files under {cls.TESTS_DIR}/. "
            "Leave production code alone and report what needs changing."
        )

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
        roles = cls.session_roles(session_id, transcript_path)
        if cls.ALL in roles:
            return None
        parts = cls.relative_parts(file_path)
        if parts is not None and parts[:1] == (cls.CONFIG_DIR,):
            return None
        if not roles:
            return (
                "Blocked: this session has no role, so it may not modify anything. "
                f"Put one or more of {cls.ALL}, {cls.IMPLEMENTATION}, "
                f"{cls.TEST} or {cls.TEST_TDD} anywhere in the session name."
            )
        in_tests = parts is not None and parts[:1] == (cls.TESTS_DIR,)
        in_unit = parts is not None and parts[:2] == (cls.TESTS_DIR, cls.UNIT_DIR)
        if any(cls.role_allows(role, in_tests, in_unit) for role in roles):
            return None
        denials = " Also, ".join(cls.role_denial(role) for role in sorted(roles))
        return f"Blocked: {denials}"


if __name__ == "__main__":
    try:
        hook_input = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    reason = FileGuard.blocked_reason(hook_input)
    if reason is not None:
        print(reason, file=sys.stderr)
        sys.exit(2)
