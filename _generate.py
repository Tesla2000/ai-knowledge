from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence


def main():
    ignored = (".venv", "_generate.py", ".git", ".idea")
    project_name = Path("/home/tesla2000/PassionProjects/Autodoc-hook")
    project_name.mkdir(exist_ok=True)
    root_dest = Path(os.getcwd()).joinpath(project_name)
    copy(root_dest, Path(__file__).parent, ignored)


def copy(root_dest: Path, source: Path, ignored: Sequence[str]):
    for path in source.iterdir():
        if path.name in ignored:
            continue
        new_path = root_dest.joinpath(path.name)
        if path.is_file():
            new_path.write_bytes(path.read_bytes())
        elif path.is_dir():
            new_path.mkdir(exist_ok=True)
            copy(new_path, path, ignored)
        else:
            raise ValueError("What?")


if __name__ == "__main__":
    exit(main())
