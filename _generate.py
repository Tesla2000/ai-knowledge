from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Sequence


def generate_modifications(project_path: Path) -> dict[str, str]:
    project_name = project_path.name
    return {
        "project_name": project_name,
        "description": input("Provide project description"),
        "script_name": project_name.replace("_", "-"),
        "docker_image_name": project_name,
        "autodoc_args": "--llm, google/gemma-2-2b-it" if input(
            "Is project private (y/n)").strip().lower() == "y" else "--llm, gpt-4o-mini, --api_keys=OPENAI_API_KEY",
        "year": str(datetime.now().year),
    }


def create_project_folders(project_path: Path):
    project_name = project_path.name
    shutil.move(project_path / "src", project_path / project_name / "src")
    docs_path = project_path / "docs/source"
    shutil.move(docs_path / "src", docs_path / project_name / "src")
    (project_path / project_name / "__init__.py").write_bytes(b"")


def main():
    ignored = (".venv", "_generate.py", ".git", ".idea", "_src_alternatives")
    modified = (
    "pyproject.toml", "Dockerfile", ".pre-commit-config.yaml", "LICENSE",)
    project_name = Path("/home/tesla2000/PassionProjects/Autodoc-hook")
    modifications = generate_modifications(project_name)
    project_name.mkdir(exist_ok=True)
    root_dest = Path(os.getcwd()).joinpath(project_name)
    copy(root_dest, Path(__file__).parent, ignored, modified, modifications)


def copy(root_dest: Path, source: Path, ignored: Sequence[str],
         modified: Sequence[str], modifications: dict[str, str]):
    for path in source.iterdir():
        if path.name in ignored:
            continue
        new_path = root_dest.joinpath(path.name)
        if path.is_file() and path.name in modified:
            new_path.write_text(path.read_text().format(**modifications))
        elif path.is_file():
            new_path.write_bytes(path.read_bytes())
        elif path.is_dir():
            new_path.mkdir(exist_ok=True)
            copy(new_path, path, ignored, modified, modifications)
        else:
            raise ValueError("What?")


if __name__ == "__main__":
    exit(main())
