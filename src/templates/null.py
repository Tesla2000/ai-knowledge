from __future__ import annotations

from typing import Literal

from src.files import AnyFile
from src.templates._base import Template
from src.templates._type import TemplateType


class NullTemplate(Template):
    type: Literal[TemplateType.NULL] = TemplateType.NULL
    files: tuple[AnyFile, ...] = ()
