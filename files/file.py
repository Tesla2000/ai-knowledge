from typing import Literal

from files._base import FileBase
from files._types import FileType


class File(FileBase):
    type: Literal[FileType.FILE] = FileType.FILE
