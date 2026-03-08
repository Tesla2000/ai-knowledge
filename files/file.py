import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Literal
from typing import Self

from pydantic import BaseModel


class File(BaseModel, frozen=True):
    type: Literal[None] = None
    relative_path: Path
    content: str

    def write(self, project_root: Path) -> None:
        path = self.get_path(project_root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self._get_content(project_root))

    def get_path(self, project_root: Path) -> Path:
        return project_root.joinpath(self.relative_path)

    def _get_content(self, _: Path) -> str:
        return self.content

    @contextmanager
    def revert_on_fail(
        self, project_root: Path
    ) -> Generator[Self, None, None]:
        content = None
        path = self.get_path(project_root)
        if path.exists():
            content = path.read_text()
        try:
            yield
        except:  # noqa: E722
            if content is None:
                os.remove(path)
            else:
                path.write_text(content)
            raise
