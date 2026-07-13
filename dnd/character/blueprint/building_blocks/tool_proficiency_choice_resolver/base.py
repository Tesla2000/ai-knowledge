from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
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
    def select_tool_proficiency(
        self,
        available: list[ToolProficiency],
        tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...],
    ) -> ToolProficiency: ...

    @abstractmethod
    def select_gaming_set(
        self,
        available: list[GamingSet],
        tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...],
    ) -> GamingSet: ...

    @abstractmethod
    def select_musical_instrument(
        self,
        available: list[MusicalInstrument],
        tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...],
    ) -> MusicalInstrument: ...

    def apply(self, blueprint: _BPT) -> _BPT:
        resolved: list[ToolProficiency | GamingSet | MusicalInstrument] = []
        for tool in blueprint.tool_proficiencies:
            if (
                isinstance(tool, ToolProficiency)
                and tool == ToolProficiency.ANY_OF_YOUR_CHOICE
            ):
                available_tools: list[ToolProficiency] = [
                    t
                    for t in ToolProficiency
                    if t != ToolProficiency.ANY_OF_YOUR_CHOICE
                ]
                resolved.append(
                    self.select_tool_proficiency(
                        available_tools, blueprint.tool_proficiencies
                    )
                )
            elif isinstance(tool, GamingSet) and tool == GamingSet.ANY_OF_YOUR_CHOICE:
                available_gaming_sets: list[GamingSet] = [
                    g for g in GamingSet if g != GamingSet.ANY_OF_YOUR_CHOICE
                ]
                resolved.append(
                    self.select_gaming_set(
                        available_gaming_sets, blueprint.tool_proficiencies
                    )
                )
            elif (
                isinstance(tool, MusicalInstrument)
                and tool == MusicalInstrument.ANY_OF_YOUR_CHOICE
            ):
                available_instruments: list[MusicalInstrument] = [
                    m
                    for m in MusicalInstrument
                    if m != MusicalInstrument.ANY_OF_YOUR_CHOICE
                ]
                resolved.append(
                    self.select_musical_instrument(
                        available_instruments, blueprint.tool_proficiencies
                    )
                )
            else:
                resolved.append(tool)
        return blueprint.model_copy(update={"tool_proficiencies": tuple(resolved)})
