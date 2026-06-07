from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Literal

from src.files._base import FileBase
from src.files._types import FileType
from src.files.python_version_file import PythonVersion


class ReadmeFile(FileBase):
    type: Literal[FileType.README] = FileType.README
    relative_path: Path = Path("README.md")
    description: str
    github_owner: str | None = None
    github_repo: str | None = None
    python_version: PythonVersion | None = None
    include_badges: bool = True
    content: str = """\
$badges## Description

$description
"""

    def _get_content(self, project_root: Path) -> str:
        badges = ""
        if self.include_badges and self.github_owner and self.github_repo:
            badge_lines = [
                f"[![codecov](https://codecov.io/gh/{self.github_owner}/{self.github_repo}/branch/main/graph/badge.svg)](https://codecov.io/gh/{self.github_owner}/{self.github_repo})",
                "[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)",
                f"[![PyPI version](https://badge.fury.io/py/{self.github_repo}.svg)](https://pypi.org/project/{self.github_repo}/)",
            ]
            if self.python_version:
                badge_lines.append(
                    f"[![Python {self.python_version}+](https://img.shields.io/badge/python-{self.python_version}+-blue.svg)](https://www.python.org/downloads/)"
                )
            badge_lines.append(
                "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)"
            )
            badges = "\n".join(badge_lines) + "\n\n"
        return Template(self.content).safe_substitute(
            description=self.description, badges=badges
        )
