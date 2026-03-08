from __future__ import annotations

from typing import Literal

from files import AnyFile
from templates._base import Template
from templates._type import TemplateType


class NullTemplate(Template):
    type: Literal[TemplateType.NULL] = TemplateType.NULL
    files: tuple[AnyFile, ...] = ()
