from __future__ import annotations

from pathlib import Path

import libcst

from .._settings import Settings


def modify_file(filepath: Path, code: str, config: Settings) -> int:
    module = libcst.parse_module(code)
    transformer = None
    new_code = module.visit(transformer).code
    if new_code != code:
        filepath.write_text(new_code)
        print(f"File {filepath} was modified")
        return 1
    return 0
