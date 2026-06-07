from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import ClassVar

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.choices.class_creation.character_class import Class
from dnd.choices.equipment_creation.weapons import HitDieSize
from frozendict import frozendict
from pydantic import Field


class HealthIncrease(BuildingBlock, ABC):
    """Abstract base class for health increase strategies when leveling up.

    Subclasses must implement _get_hit_die_value to determine how much
    health to gain from the hit die (fixed value, random roll, etc.).
    """

    class_: Class = Field(
        description="The character class for which health is being increased"
    )

    _class2hit_die: ClassVar[frozendict[Class, HitDieSize]] = frozendict(
        {
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
    )

    @abstractmethod
    def _get_hit_die_value(self, hit_die: HitDieSize) -> int:
        """Get the hit die value for health increase.

        Args:
            hit_die: The hit die for the class.

        Returns:
            The hit die value to add to health.
        """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Calculate and apply health increase.

        Args:
            blueprint: The current blueprint state.

        Yields:
            Blueprint with updated health.

        Raises:
            ValueError: If stats are not configured.
        """
        current_health = blueprint.health_base
        hit_die = self._class2hit_die[self.class_]

        # First level always gets max hit die value
        if current_health is None:
            hit_die_value = hit_die.value
            current_health = 0
        else:
            hit_die_value = self._get_hit_die_value(hit_die)

        return Blueprint(health_base=current_health + hit_die_value)
