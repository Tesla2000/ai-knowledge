from typing import Annotated

from pydantic import Discriminator

from src.templates.cli_package import CliPackage
from src.templates.package import PythonPackage

AnyTemplate = Annotated[PythonPackage | CliPackage, Discriminator("type")]

__all__ = [
    "AnyTemplate",
    "CliPackage",
    "PythonPackage",
]
