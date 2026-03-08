from typing import Annotated, Union

from pydantic import Discriminator

from templates.null import NullTemplate
from templates.package import PythonPackage

AnyTemplate = Annotated[
    Union[NullTemplate, PythonPackage], Discriminator("type")
]

__all__ = [
    "NullTemplate",
    "PythonPackage",
    "AnyTemplate",
]