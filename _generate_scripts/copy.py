from __future__ import annotations

from pathlib import Path
from string import Template
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
    modifications.update({"pydantic_extra": '"pydantic[mypy]>=2.11.3"'})
    modifications.update({"anti_magic_formatting": "\"black {filepaths} --preview --line-length 79\\nreorder-python-imports {filepaths} --py37-plus --add-import 'from __future__ import annotations' --py39-plus\""})
    modifications.update({"config_parser": '"config-parser @ git+https://github.com/Tesla2000/ConfigParser"'})
    modifications.update({"utility_functions": '"utility-functions @ git+https://github.com/Tesla2000/UtilityFunctions"'})
    for path in filter(lambda path: path.name not in ignored, sorted(source.iterdir(), key=Path.is_dir)):
        new_path = root_dest.joinpath(path.name)
        if path.is_file() and path.name in modified:
            template = Template(path.read_text())
            new_path.write_text(template.safe_substitute(**modifications))
        elif path.is_file():
            new_path.write_bytes(path.read_bytes())
        elif path.is_dir():
            new_path.mkdir(exist_ok=True)
            copy(new_path, path, ignored, modified, modifications)
        else:
            raise ValueError("What?")
