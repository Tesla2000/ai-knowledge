from pathlib import Path
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field

from src.files._base import FileBase
from src.files._types import FileType

_CodeOwner = Annotated[
    str, AfterValidator(lambda string: "@" + string.lstrip("@"))
]


class _CodeOwnersMixin(BaseModel):
    codeowners: tuple[_CodeOwner, ...] = Field(
        default=("@Tesla2000",), min_length=1
    )


class CodeOwnersFile(_CodeOwnersMixin, FileBase):
    type: Literal[FileType.CODE_OWNERS] = FileType.CODE_OWNERS
    relative_path: Path = Path(".github/CODEOWNERS")
    content: str = Field(
        default_factory=lambda validated_data: "* "
        + " ".join(validated_data.get("codeowners") or ())
    )
