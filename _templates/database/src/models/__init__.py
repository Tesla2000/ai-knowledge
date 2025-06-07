from __future__ import annotations

from importlib import import_module
from pathlib import Path

from base import Base
from connection import db



def import_python(root: Path):
    for module_path in root.glob("*.py"):
        if module_path.name in ("__init__.py", "pycache", "__pycache__"):
            continue
        if module_path.is_file():
            relative_path = module_path.relative_to(Path(__file__).parent)
            subfolders = "".join(map(".{}".format, relative_path.parts[:-1]))
            str_path = module_path.with_suffix("").name
            yield import_module("." + str_path, __name__ + subfolders)
            continue
        yield from import_python(module_path)

db.create_tables(
    set(
        filter(
            Base.__subclasscheck__,
            filter(
                lambda elem: isinstance(elem, type) and elem != Base,
                (
                    getattr(module, name)
                    for module in import_python(Path(__file__).parent)
                    for name in dir(module)
                ),
            ),
        )
    )
)
