from __future__ import annotations

import json
import os
import shutil
import traceback
from pathlib import Path

from _generate_scripts.copy import copy
from _generate_scripts.create_project_folder import create_project_folders
from _generate_scripts.generate_modifications import generate_modifications
from _generate_scripts.pick_template import pick_template


def main():
    answers = {}
    answers_file = Path("answers.json")
    if answers_file.exists():
        answers = json.loads(answers_file.read_text())
        os.remove(answers_file)
    base_path = Path(f"/home/filip/PassionProjects")
    print(f"Creating project in {base_path}")
    project_path = base_path.joinpath(input('Project name: '))
    try:
        ignored = (
            ".venv",
            "_generate.py",
            "_generate_scripts",
            ".git",
            ".idea",
            "_templates",
        )
        modified = (
            "pyproject.toml",
            "Dockerfile",
            ".pre-commit-config.yaml",
            ".pre-commit-hooks.yaml",
            "LICENSE",
            "README.md",
            "__main__.py",
        )
        modifications = generate_modifications(project_path, answers)
        project_path.mkdir(exist_ok=True)
        root_dest = Path(os.getcwd()).joinpath(project_path)
        template = pick_template(answers)
        copy(root_dest, template, ignored, modified, modifications)
        copy(
            root_dest, Path(__file__).parent, ignored, modified, modifications
        )
        create_project_folders(project_path)
        return 0
    except BaseException as e:
        print(str(e))
        print(traceback.format_exc())
        shutil.rmtree(project_path)
        answers_file.write_text(json.dumps(answers))
        return 1


if __name__ == "__main__":
    exit(main())
