from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from pydantic import ConfigDict


class ToolProficiencyChoiceResolver(BuildingBlock, ABC):
    """Resolves ANY_OF_YOUR_CHOICE placeholders in tool proficiencies.

    This resolver handles the union type:
    ToolProficiency | GamingSet | MusicalInstrument

    Each placeholder is replaced based on its specific type.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_tool_proficiency(
        self, available: list[ToolProficiency], blueprint: Blueprint
    ) -> ToolProficiency:
        """Select from ToolProficiency options.

        Args:
            available: List of ToolProficiency excluding ANY_OF_YOUR_CHOICE.
            blueprint: Current character blueprint for context.

        Returns:
            Selected ToolProficiency.
        """

    @abstractmethod
    def _select_gaming_set(
        self, available: list[GamingSet], blueprint: Blueprint
    ) -> GamingSet:
        """Select from GamingSet options.

        Args:
            available: List of GamingSet excluding ANY_OF_YOUR_CHOICE.
            blueprint: Current character blueprint for context.

        Returns:
            Selected GamingSet.
        """

    @abstractmethod
    def _select_musical_instrument(
        self, available: list[MusicalInstrument], blueprint: Blueprint
    ) -> MusicalInstrument:
        """Select from MusicalInstrument options.

        Args:
            available: List of MusicalInstrument excluding ANY_OF_YOUR_CHOICE.
            blueprint: Current character blueprint for context.

        Returns:
            Selected MusicalInstrument.
        """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Replace tool proficiency ANY_OF_YOUR_CHOICE placeholders.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with tool proficiency placeholders replaced.
        """
        resolved = set()
        for tool in blueprint.tool_proficiencies:
            if (
                isinstance(tool, ToolProficiency)
                and tool == ToolProficiency.ANY_OF_YOUR_CHOICE
            ):
                available = [
                    t
                    for t in ToolProficiency
                    if t != ToolProficiency.ANY_OF_YOUR_CHOICE
                ]
                resolved.add(
                    self._select_tool_proficiency(available, blueprint)
                )
            elif (
                isinstance(tool, GamingSet)
                and tool == GamingSet.ANY_OF_YOUR_CHOICE
            ):
                available = [
                    g for g in GamingSet if g != GamingSet.ANY_OF_YOUR_CHOICE
                ]
                resolved.add(self._select_gaming_set(available, blueprint))
            elif (
                isinstance(tool, MusicalInstrument)
                and tool == MusicalInstrument.ANY_OF_YOUR_CHOICE
            ):
                available = [
                    m
                    for m in MusicalInstrument
                    if m != MusicalInstrument.ANY_OF_YOUR_CHOICE
                ]
                resolved.add(
                    self._select_musical_instrument(available, blueprint)
                )
            else:
                resolved.add(tool)
        return Blueprint(tool_proficiencies=resolved)
