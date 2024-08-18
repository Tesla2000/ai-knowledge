from __future__ import annotations

import os
from pathlib import Path

from _generate_scripts.copy import copy
from _generate_scripts.create_project_folder import create_project_folders
from _generate_scripts.generate_modifications import generate_modifications
from _generate_scripts.pick_template import pick_template


def main():
    ignored = (".venv", "_generate.py", "_generate_scripts", ".git", ".idea", "_templatest", ".pre-commit-hooks.yaml")
    modified = (
    "pyproject.toml", "Dockerfile", ".pre-commit-config.yaml", "LICENSE",)
    project_path = Path("/home/tesla2000/PassionProjects/Autodoc-hook")
    modifications = generate_modifications(project_path)
    project_path.mkdir(exist_ok=True)
    root_dest = Path(os.getcwd()).joinpath(project_path)
    template = pick_template()
    copy(root_dest, template, ignored, modified, modifications)
    copy(root_dest, Path(__file__).parent, ignored, modified, modifications)
    create_project_folders(project_path)


if __name__ == "__main__":
    exit(main())
