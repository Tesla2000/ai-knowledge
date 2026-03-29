from typing import Annotated
from typing import Union

from pydantic import Discriminator
from templates.cli_package import CliPackage
from templates.null import NullTemplate
from templates.package import PythonPackage

AnyTemplate = Annotated[
    Union[NullTemplate, PythonPackage, CliPackage], Discriminator("type")
]

__all__ = [
    "NullTemplate",
    "PythonPackage",
    "CliPackage",
    "AnyTemplate",
]
