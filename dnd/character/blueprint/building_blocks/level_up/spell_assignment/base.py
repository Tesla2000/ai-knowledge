from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import ClassVar

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.spells import Cantrip
from dnd.character.spells import EighthLevel
from dnd.character.spells import FifthLevel
from dnd.character.spells import filter_accessible
from dnd.character.spells import FirstLevel
from dnd.character.spells import FourthLevel
from dnd.character.spells import NinthLevel
from dnd.character.spells import SecondLevel
from dnd.character.spells import SeventhLevel
from dnd.character.spells import SixthLevel
from dnd.character.spells import Spell
from dnd.character.spells import SPELLCASTING_ABILITY_MAP
from dnd.character.spells import ThirdLevel
from dnd.character.spells.max_spell_levels import CasterType
from dnd.character.spells.max_spell_levels import (
    MAX_SPELL_LEVELS,
)
from dnd.choices.class_creation.character_class import Class
from frozendict import frozendict
from pydantic import Field


class SpellAssigner(BuildingBlock, ABC):
    """Abstract base class for spell assignment strategies.

    Subclasses must implement get_change to determine how spells are selected
    and assigned to the character.
    """

    class_: Class = Field(
        description="The character class for which spells are being assigned"
    )

    _class_to_caster: ClassVar[frozendict[Class, CasterType]] = frozendict(
        {
            Class.BARD: CasterType.FULL,
            Class.CLERIC: CasterType.FULL,
            Class.DRUID: CasterType.FULL,
            Class.SORCERER: CasterType.FULL,
            Class.WIZARD: CasterType.FULL,
            Class.ARTIFICER: CasterType.HALF,
            Class.PALADIN: CasterType.HALF,
            Class.RANGER: CasterType.HALF,
            Class.WARLOCK: CasterType.WARLOCK,
            Class.FIGHTER: CasterType.ELDRITCH_KNIGHT,
            Class.ROGUE: CasterType.ELDRITCH_KNIGHT,
        }
    )

    _spell_level_to_class: ClassVar[frozendict[int, type[Spell]]] = frozendict(
        {
            0: Cantrip,
            1: FirstLevel,
            2: SecondLevel,
            3: ThirdLevel,
            4: FourthLevel,
            5: FifthLevel,
            6: SixthLevel,
            7: SeventhLevel,
            8: EighthLevel,
            9: NinthLevel,
        }
    )

    _spell_level_to_attr: ClassVar[frozendict[int, str]] = frozendict(
        {
            0: "cantrips",
            1: "first_level_spells",
            2: "second_level_spells",
            3: "third_level_spells",
            4: "fourth_level_spells",
            5: "fifth_level_spells",
            6: "sixth_level_spells",
            7: "seventh_level_spells",
            8: "eighth_level_spells",
            9: "ninth_level_spells",
        }
    )

    def _get_effective_caster_level(self, blueprint: Blueprint) -> int:
        """Calculate effective caster level for multiclassing.

        For spell slots, combine levels from all caster classes:
        - Full casters (Wizard, Sorcerer, etc.): count full levels
        - Half casters (Paladin, Ranger): count half levels
        - Third casters (Eldritch Knight): count third levels

        Args:
            blueprint: Current character blueprint.

        Returns:
            Effective caster level for determining max spell level.
        """
        if self.class_ in (Class.SORCERER, Class.WIZARD):
            return blueprint.classes.get(Class.SORCERER, 0) + blueprint.classes.get(
                Class.WIZARD, 0
            )
        raise NotImplementedError("To be implemented for other classes")

    def _get_max_spell_level(self, blueprint: Blueprint) -> int:
        """Get the maximum spell level based on effective caster level.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Maximum spell level (0-9).
        """
        effective_caster_level = self._get_effective_caster_level(blueprint)
        if effective_caster_level == 0:
            return 0
        caster_type = self._class_to_caster[self.class_]
        return MAX_SPELL_LEVELS[caster_type][min(effective_caster_level, 20) - 1]

    @staticmethod
    def _is_first_level(blueprint: Blueprint) -> bool:
        """Check if character is at first level for wizard/sorcerer.

        Args:
            blueprint: Current character blueprint.

        Returns:
            True if character has exactly 1 level in wizard or sorcerer.
        """
        return (
            blueprint.classes.get(Class.WIZARD, 0)
            + blueprint.classes.get(Class.SORCERER, 0)
        ) == 1

    def _get_spells_to_learn(self, blueprint: Blueprint) -> dict[int, int]:
        """Calculate how many spells to learn per spell level.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Dictionary mapping spell level to number of spells to learn.
        """
        spell_increase = {}
        n_cantrips_increase_levels = (4, 10)
        if self.class_ not in blueprint.classes:
            raise ValueError(
                f"Character has no levels in {self.class_}. Level up {self.class_} before assigning spells for it."
            )
        if self.class_ == Class.WIZARD:
            if blueprint.classes[self.class_] == 1:
                return {0: 3, 1: 6}
            spell_increase[self._get_max_spell_level(blueprint)] = 2
            spell_increase[0] = (
                blueprint.classes[self.class_] in n_cantrips_increase_levels
            )
            return spell_increase
        if self.class_ == Class.SORCERER:
            if blueprint.classes[self.class_] == 1:
                return {0: 4, 1: 2}
            spell_increase[self._get_max_spell_level(blueprint)] = 1
            spell_increase[0] = (
                blueprint.classes[self.class_] in n_cantrips_increase_levels
            )
            return spell_increase
        raise NotImplementedError(
            "For non-wizards, no specific spell learning rules yet"
        )

    def _get_available_spells(self, spell_level: int) -> frozenset[Spell]:
        """Get all accessible spells for class at spell level.

        Args:
            spell_level: The spell level (0-9).

        Returns:
            Frozenset of available spells.
        """
        spell_type = self._spell_level_to_class[spell_level]
        return filter_accessible(spell_type, self.class_)

    @abstractmethod
    def _select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        blueprint: Blueprint,
    ) -> tuple[Spell, ...]:
        """Select N spells from available list.

        This is the only method that differs between implementations.

        Args:
            spell_level: The spell level (0-9).
            count: Number of spells to select.
            available_spells: Filtered list of available spells to choose from.
            blueprint: Current character blueprint for context.

        Returns:
            Tuple of selected spells.
        """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Apply spell assignments to the blueprint.

        Args:
            blueprint: The current blueprint state.

        Yields:
            Blueprint with updated spells.

        Raises:
            ValueError: If character doesn't have the specified class.
        """

        # 1. Validate class is spellcaster
        if self.class_ not in SPELLCASTING_ABILITY_MAP:
            # Not a spellcasting class, yield empty and return
            return Blueprint()

        # 2. Determine spells to learn
        spells_to_learn = self._get_spells_to_learn(blueprint)

        if not spells_to_learn:
            # No spells to learn for this class for this level
            return Blueprint()

        # 3. Select spells for each level
        spells = blueprint.spells
        for spell_level, count in spells_to_learn.items():
            # Get available spells for this level
            available = list(self._get_available_spells(spell_level))

            if not available:
                continue

            # Filter out already-known spells
            existing_spells = set(
                blueprint.spells.get_spell_level_by_index(spell_level)
            )
            available_filtered = [s for s in available if s not in existing_spells]

            if not available_filtered:
                continue

            # Call subclass-specific selection method
            selected = self._select_spells(
                spell_level, count, available_filtered, blueprint
            )

            # Merge with existing
            merged = existing_spells.union(selected)
            attr_name = self._spell_level_to_attr[spell_level]
            spells = spells.model_copy(update={attr_name: tuple(merged)})

        return Blueprint(spells=spells)
