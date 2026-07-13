from abc import ABC

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.character.armor.names import ArmorName
from dnd.choices.equipment_creation.weapons import WeaponName
from pydantic import ConfigDict


class EquipmentChooser(BuildingBlock, ABC):
    """Abstract base class for choosing equipment from available options."""

    model_config = ConfigDict(frozen=True)

    def apply(self, blueprint: _BPT) -> _BPT:
        weapons, armors, others = self._pick_equipment(blueprint)
        return blueprint.model_copy(
            update={
                "weapons": blueprint.weapons + tuple(weapons),
                "armors": blueprint.armors + tuple(armors),
                "other_equipment": blueprint.other_equipment + tuple(others),
                "equipment_choices": (),
            }
        )

    def _pick_equipment(
        self, blueprint: _BPT
    ) -> tuple[list[WeaponName], list[ArmorName], list[str]]:
        """Return (weapons, armors, other_equipment) from equipment_choices."""
        raise NotImplementedError
