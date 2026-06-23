from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from dnd.character.delta.delta import Delta

if TYPE_CHECKING:
    from dnd.character.delta.any_delta import AnyDelta


def __getattr__(name: str) -> object:
    if name == "AnyDelta":
        return importlib.import_module(".any_delta", package=__package__).AnyDelta
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["AnyDelta", "Delta"]
