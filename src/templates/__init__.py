from typing import Annotated, Union

from pydantic import Discriminator

from src.templates.cli_package import CliPackage
from src.templates.null import NullTemplate
from src.templates.package import PythonPackage

AnyTemplate = Annotated[
    Union[NullTemplate, PythonPackage, CliPackage], Discriminator("type")
]

__all__ = [
    "NullTemplate",
    "PythonPackage",
    "CliPackage",
    "AnyTemplate",
]
