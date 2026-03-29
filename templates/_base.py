from abc import ABC
from contextlib import ExitStack
from pathlib import Path

from files import AnyFile
from pydantic import BaseModel
from templates._type import TemplateType


class Template(BaseModel, ABC):
    type: TemplateType
    files: tuple[AnyFile, ...]

    def generate(self, project_root: Path) -> None:
        with ExitStack() as stack:
            for file in self.files:
                stack.enter_context(file.revert_on_fail(project_root))
                file.write(project_root)
