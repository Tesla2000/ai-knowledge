from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic_settings import CliImplicitFlag

from src.files._base import FileBase
from src.files._types import FileType
from src.files.package_pyproject_toml import Dependency
from src.files.python_version_file import PythonVersion


class PreCommitConfig(FileBase):
    type: Literal[FileType.PRE_COMMIT_CONFIG] = FileType.PRE_COMMIT_CONFIG
    relative_path: Path = Path(".pre-commit-config.yaml")
    mypy_additional_dependencies: tuple[Dependency, ...] = ()
    generate_stubs: CliImplicitFlag[bool] = False
    python_version: PythonVersion
    content: str = """\
repos:
  - repo: https://github.com/PyCQA/autoflake
    rev: v2.3.3
    hooks:
      - id: autoflake
        args: [ --remove-all-unused-imports, --in-place ]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.16
    hooks:
      - id: ruff-format
      - id: ruff
        args: [ "--extend-ignore=E501" ]
  - repo: https://github.com/asottile/pyupgrade
    rev: v3.21.2
    hooks:
      - id: pyupgrade
        args: [ --$python-target-version-plus ]
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: [--exclude-files, '^(README\\.md|alembic/.*)$']
  - repo: https://github.com/Tesla2000/vulture
    rev: v0.0.4
    hooks:
      - id: vulture
        args:
          [
            ".",
            "--exclude",
            ".venv,venv,tests",
            "--ignore-attributes-for-classes=.*",
            "--ignore-decorators=@app.*,@pytest.fixture,@property,@model_validator,@field_serializer,@field_validator",
            "--ignore-names=Meta,__dict__,cli_cmd",
             "--extra-sys-path=.venv/lib/python3.12/site-packages,.",
          ]
        stages: [ pre-commit ]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v2.1.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.8.2
          - pydantic-settings>=2.13.0
        # mypy_additional_dependencies
        args: [ --strict, --config-file, pyproject.toml ]
        exclude: ^tests/
  - repo: https://github.com/Tesla2000/any-hook
    rev: v3.11.0
    hooks:
      - id: any-hook
        args: [--modifiers, '[$package-dependent{"type": "remove-f-prefix"},{"type": "open-to-path"},{"type": "any-to-object"},{"type":"pydantic-config-to-model-config"},{"type":"local-imports"},{"type":"pydantic-v1-to-v2"},{"type":"str-enum-inheritance"},{"type":"forbidden-functions","forbidden_functions":["hasattr","getattr","print"]},{"type":"utcnow-to-datetime-now"},{"type":"len-as-bool"},{"type":"typing-to-builtin"},{"type":"comment-detector","patterns":["type: ignore"]}]']
"""

    def _get_content(self, project_root: Path) -> str:
        if self.mypy_additional_dependencies:
            deps_str = "        additional_dependencies:\n" + "".join(
                f"          - {dep}\n"
                for dep in self.mypy_additional_dependencies
            )
        else:
            deps_str = ""
        hooks = [
            {
                "type": "check-untracked",
                "directories": [project_root.name, "tests"],
            }
        ]
        if self.generate_stubs:
            hooks.append(
                {
                    "type": "generate-stubs",
                    "directories": [project_root.name],
                }
            )
        content = self.content.replace(
            "$package-dependent",
            ",".join(map(json.dumps, hooks)) + ",",
        )
        content = content.replace("$project-root", project_root.name)
        content = content.replace(
            "$python-target-version",
            f"py{self.python_version.major}{self.python_version.minor}",
        )
        return content.replace(
            "        # mypy_additional_dependencies\n", deps_str
        )
