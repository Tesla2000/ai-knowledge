from typing import Annotated, Union

from pydantic import Discriminator

from src.templates.cli_package import CliPackage
from src.templates.package import PythonPackage

AnyTemplate = Annotated[Union[PythonPackage, CliPackage], Discriminator("type")]

__all__ = [
    "PythonPackage",
    "CliPackage",
    "AnyTemplate",
]
