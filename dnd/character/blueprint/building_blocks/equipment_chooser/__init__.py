from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.equipment_chooser.ai import (
    AIEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.random import (
    RandomEquipmentChooser,
)
from pydantic import Field

AnyEquipmentChooser = Annotated[
    Union[
        RandomEquipmentChooser,
        AIEquipmentChooser,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AIEquipmentChooser",
    "RandomEquipmentChooser",
    "AnyEquipmentChooser",
]
