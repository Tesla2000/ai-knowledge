from __future__ import annotations

from abc import ABC
from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import Equipment
from dnd.character.blueprint.state import HasArmors
from dnd.character.blueprint.state import HasEquipmentChoices
from dnd.character.blueprint.state import HasEquipmentResolved
from dnd.character.blueprint.state import HasOtherEquipment
from dnd.character.blueprint.state import HasWeapons
from dnd.character.armor.names import ArmorName
from dnd.character.delta.delta import Delta
from dnd.choices.equipment_creation.weapons import WeaponName
from pydantic import ConfigDict


class EquipmentDelta(Delta):
    """Delta produced when EquipmentChooser resolves equipment choices."""

    weapons: tuple[WeaponName, ...]
    armors: tuple[ArmorName, ...]
    other_equipment: tuple[str, ...]
    equipment_choices: tuple[tuple[Equipment, ...], ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasEquipmentResolved]:

        if TYPE_CHECKING:

            class BlueprintWithEquipment(Blueprint):
                weapons: tuple[WeaponName, ...]
                armors: tuple[ArmorName, ...]
                other_equipment: tuple[str, ...]
                equipment_choices: tuple[tuple[Equipment, ...], ...]

        else:

            class BlueprintWithEquipment(type(state)):
                weapons: tuple[WeaponName, ...]
                armors: tuple[ArmorName, ...]
                other_equipment: tuple[str, ...]
                equipment_choices: tuple[tuple[Equipment, ...], ...]

        return cast(
            ProtocolIntersection[T, HasEquipmentResolved],
            BlueprintWithEquipment.model_validate(
                {
                    **dict(state),
                    "weapons": self.weapons,
                    "armors": self.armors,
                    "other_equipment": self.other_equipment,
                    "equipment_choices": self.equipment_choices,
                }
            ),
        )


class EquipmentChooser[T: HasEquipmentChoices](
    BuildingBlock[T, EquipmentDelta, HasEquipmentResolved], ABC
):
    """Abstract base class for choosing equipment from available options."""

    model_config = ConfigDict(frozen=True)

    def get_change(
        self, state: T
    ) -> Generator[EquipmentDelta, None, ProtocolIntersection[T, HasEquipmentResolved]]:
        weapons, armors, others = self._pick_equipment(state)
        existing_weapons = state.weapons if isinstance(state, HasWeapons) else ()
        existing_armors = state.armors if isinstance(state, HasArmors) else ()
        existing_other = (
            state.other_equipment if isinstance(state, HasOtherEquipment) else ()
        )
        delta = EquipmentDelta(
            weapons=existing_weapons + tuple(weapons),
            armors=existing_armors + tuple(armors),
            other_equipment=existing_other + tuple(others),
            equipment_choices=(),
        )
        yield delta
        return delta.apply(state)

    def _pick_equipment(
        self, state: T
    ) -> tuple[list[WeaponName], list[ArmorName], list[str]]:
        """Return (weapons, armors, other_equipment) from equipment_choices."""
        raise NotImplementedError
