from typing import Literal

from src.files._base import FileBase
from src.files._types import FileType


class File(FileBase):
    type: Literal[FileType.FILE] = FileType.FILE
