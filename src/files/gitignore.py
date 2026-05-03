from pathlib import Path
from typing import Literal

from pydantic import Field

from src.files._base import FileBase
from src.files._types import FileType


class Gitignore(FileBase):
    type: Literal[FileType.GITIGNORE] = FileType.GITIGNORE
    relative_path: Path = Path(".gitignore")
    ignored: tuple[str, ...] = (
        "/sandbox.py",
        "/.idea",
        "/.env",
        "/.venv",
        "/.vscode",
        "/.run/",
        "*__pycache__",
        "/docs/build/",
        "/.coverage",
        "/coverage.xml",
        "/junit.xml",
        "/.coverage",
        "__pycache__/",
        "*.pyc",
    )
    content: str = Field(
        default_factory=lambda validated_data: "\n".join(
            validated_data.get("ignored", ())
        )
    )
