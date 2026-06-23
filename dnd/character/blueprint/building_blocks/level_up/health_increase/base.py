from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import ClassVar
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasHealthBase
from dnd.character.delta.delta import Delta
from dnd.choices.class_creation.character_class import Class
from dnd.choices.equipment_creation.weapons import HitDieSize
from pydantic import Field


class HealthBaseDelta(Delta):
    """Delta produced when HealthIncrease updates health_base."""

    health_base: int

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasHealthBase]:

        if TYPE_CHECKING:

            class BlueprintWithHealthBase(Blueprint):
                health_base: int

        else:

            class BlueprintWithHealthBase(type(state)):
                health_base: int

        return cast(
            ProtocolIntersection[T, HasHealthBase],
            BlueprintWithHealthBase.model_validate(
                {**dict(state), "health_base": self.health_base}
            ),
        )


class HealthIncrease[T: HasClasses](
    BuildingBlock[T, HealthBaseDelta, HasHealthBase], ABC
):
    """Abstract base class for health increase strategies when leveling up.

    Subclasses must implement _get_hit_die_value to determine how much
    health to gain from the hit die (fixed value, random roll, etc.).
    """

    class_: Class = Field(
        description="The character class for which health is being increased"
    )

    _class2hit_die: ClassVar[dict[Class, HitDieSize]] = {
        Class.BARBARIAN: HitDieSize.TWELVE,
        Class.BARD: HitDieSize.EIGHT,
        Class.CLERIC: HitDieSize.EIGHT,
        Class.DRUID: HitDieSize.EIGHT,
        Class.FIGHTER: HitDieSize.TEN,
        Class.MONK: HitDieSize.EIGHT,
        Class.PALADIN: HitDieSize.TEN,
        Class.RANGER: HitDieSize.TEN,
        Class.ROGUE: HitDieSize.EIGHT,
        Class.SORCERER: HitDieSize.SIX,
        Class.WARLOCK: HitDieSize.EIGHT,
        Class.WIZARD: HitDieSize.SIX,
        Class.ARTIFICER: HitDieSize.EIGHT,
    }

    @abstractmethod
    def _get_hit_die_value(self, hit_die: HitDieSize) -> int:
        """Get the hit die value for health increase."""

    def get_change(
        self, state: T
    ) -> Generator[HealthBaseDelta, None, ProtocolIntersection[T, HasHealthBase]]:
        hit_die = self._class2hit_die[self.class_]
        current_health: int | None = (
            state.health_base if isinstance(state, HasHealthBase) else None
        )

        if current_health is None:
            hit_die_value = hit_die.value
            current_health = 0
        else:
            hit_die_value = self._get_hit_die_value(hit_die)

        delta = HealthBaseDelta(health_base=current_health + hit_die_value)
        yield delta
        return delta.apply(state)
