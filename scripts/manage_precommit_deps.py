#!/usr/bin/env python3
"""Add or remove additional_dependencies entries in the mypy hook of .pre-commit-config.yaml.

Usage:
    python3 .claude/scripts/manage_precommit_deps.py add types-requests
    python3 .claude/scripts/manage_precommit_deps.py remove types-requests

Direct edits to .pre-commit-config.yaml are forbidden. Use this script instead.
"""

import sys
from pathlib import Path


_CONFIG = Path(".pre-commit-config.yaml")


class PreCommitDepsManager:
    def __init__(self, path: Path) -> None:
        self._path = path

    def _find_mypy_deps_block(self, lines: list[str]) -> tuple[int, int, str]:
        """Return (insert_after_line, block_end_line, indent) for the mypy additional_dependencies block."""
        in_mypy = False
        in_deps = False
        header_line = -1
        block_end = -1
        indent = "          "

        for i, line in enumerate(lines):
            if "id: mypy" in line:
                in_mypy = True
                continue
            if in_mypy and "additional_dependencies:" in line:
                in_deps = True
                header_line = i
                indent = " " * (len(line) - len(line.lstrip()) + 2)
                continue
            if in_deps:
                stripped = line.strip()
                if stripped.startswith("- "):
                    block_end = i
                elif stripped == "":
                    continue
                else:
                    break

        if header_line == -1:
            raise RuntimeError("Could not find mypy additional_dependencies block")
        end = block_end + 1 if block_end != -1 else header_line + 1
        return header_line, end, indent

    def _existing_deps(self, lines: list[str], header: int, end: int) -> list[str]:
        deps = []
        for line in lines[header + 1 : end]:
            stripped = line.strip()
            if stripped.startswith("- "):
                deps.append(stripped[2:].strip())
        return deps

    def add(self, package: str) -> None:
        lines = self._path.read_text().splitlines(keepends=True)
        header, end, indent = self._find_mypy_deps_block(lines)
        existing = self._existing_deps(lines, header, end)
        if package in existing:
            sys.stdout.write(f"Already present: {package}")
            return
        new_deps = sorted(existing + [package], key=str.lower)
        dep_lines = [f"{indent}- {dep}\n" for dep in new_deps]
        lines[header + 1 : end] = dep_lines
        self._path.write_text("".join(lines))
        sys.stdout.write(f"Added: {package}")

    def remove(self, package: str) -> None:
        lines = self._path.read_text().splitlines(keepends=True)
        header, end, indent = self._find_mypy_deps_block(lines)
        existing = self._existing_deps(lines, header, end)
        if package not in existing:
            sys.stdout.write(f"Not found: {package}")
            return
        new_deps = [d for d in existing if d != package]
        dep_lines = [f"{indent}- {dep}\n" for dep in new_deps]
        lines[header + 1 : end] = dep_lines
        self._path.write_text("".join(lines))
        sys.stdout.write(f"Removed: {package}")


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in ("add", "remove"):
        sys.stderr.write(
            "Usage: manage_precommit_deps.py <add|remove> <package>",
        )
        return 1
    manager = PreCommitDepsManager(_CONFIG)
    action, package = argv[1], argv[2]
    if action == "add":
        manager.add(package)
    else:
        manager.remove(package)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
