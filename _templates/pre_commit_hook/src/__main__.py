from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from utility_functions import file_modification_transaction

from $project_name_low._settings import Settings, create_settings
from $project_name_low.modify_file import modify_file


class Main:
    _settings: Settings

    def __call__(self) -> int:
        self._settings = create_settings()
        if self._settings is None:
            return 2
        with file_modification_transaction(self._settings.pos_args) as (paths, contents):
            pass
        return 0

    def _main(self, paths: Iterable[Path], contents: Iterable[str],
              settings: Settings) -> int:
        fail = 0
        for filepath, content in zip(paths, contents):
            fail |= modify_file(filepath, content, settings)
        return fail
