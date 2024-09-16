from __future__ import annotations

from pathlib import Path
from typing import Optional
from typing import Sequence


def copy(
    root_dest: Path,
    source: Path,
    ignored: Sequence[str] = tuple(),
    modified: Sequence[str] = tuple(),
    modifications: Optional[dict[str, str]] = None,
):
    modifications = modifications or {}
    for path in filter(lambda path: path.name not in ignored, sorted(source.iterdir(), key=Path.is_dir)):
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
