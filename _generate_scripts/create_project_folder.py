from __future__ import annotations

import os
import shutil
from pathlib import Path


def create_project_folders(project_path: Path):
    project_name = to_snake(project_path.name)
    _move_directory_contents(project_path / "src", project_path / "src" / project_name)
    docs_path = project_path / "docs/source"
    _move_directory_contents(docs_path / "src", docs_path / "src" / project_name)
    (project_path / "src/__init__.py").write_bytes(b"")


def _move_directory_contents(src_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.abspath(src_path) != os.path.abspath(dest_dir):
            shutil.move(src_path, dest_path)
        else:
            print(f"Skipping move of '{src_path}' into itself '{dest_path}'.")



def to_snake(string: str):
    if not string:
        return string
    return string[0].lower() + "".join(f"_{char.lower()}" if char.isupper() else char for char in string[1:])

