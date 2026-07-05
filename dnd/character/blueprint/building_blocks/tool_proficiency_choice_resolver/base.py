from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import overload
from typing import TYPE_CHECKING

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasToolProficiencies
from dnd.character.delta.delta import Delta
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from pydantic import ConfigDict
from typing import Literal


class ToolProficienciesDelta(Delta):
    """Delta produced when ToolProficiencyChoiceResolver resolves choices."""

    delta_type: Literal["ToolProficienciesDelta"] = "ToolProficienciesDelta"
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasToolProficiencies]:
        if TYPE_CHECKING:

            class BlueprintWithToolProficiencies(Blueprint):
                tool_proficiencies: tuple[
                    ToolProficiency | GamingSet | MusicalInstrument, ...
                ]

        else:

            class BlueprintWithToolProficiencies(type(state)):
                tool_proficiencies: tuple[
                    ToolProficiency | GamingSet | MusicalInstrument, ...
                ]

        return cast(
            ProtocolIntersection[T, HasToolProficiencies],
            BlueprintWithToolProficiencies.model_validate(
                {**dict(state), "tool_proficiencies": self.tool_proficiencies}
            ),
        )


class ToolProficiencyChoiceResolver(BuildingBlock, ABC):
    """Resolves ANY_OF_YOUR_CHOICE placeholders in tool proficiencies.

    This resolver handles the union type:
    ToolProficiency | GamingSet | MusicalInstrument

    Each placeholder is replaced based on its specific type.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_tool_proficiency(
        self, available: list[ToolProficiency], state: HasToolProficiencies
    ) -> ToolProficiency: ...

    @abstractmethod
    def _select_gaming_set(
        self, available: list[GamingSet], state: HasToolProficiencies
    ) -> GamingSet: ...

    @abstractmethod
    def _select_musical_instrument(
        self, available: list[MusicalInstrument], state: HasToolProficiencies
    ) -> MusicalInstrument: ...

    @overload
    def get_change[T: HasToolProficiencies](
        self, state: T
    ) -> Generator[
        ToolProficienciesDelta, None, ProtocolIntersection[T, HasToolProficiencies]
    ]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasToolProficiencies for precise return typing"
    )
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, HasToolProficiencies):
            raise TypeError(
                f"{type(self).__name__} requires HasToolProficiencies, got {type(state).__name__}"
            )
        resolved: list[ToolProficiency | GamingSet | MusicalInstrument] = []
        for tool in state.tool_proficiencies:
            if (
                isinstance(tool, ToolProficiency)
                and tool == ToolProficiency.ANY_OF_YOUR_CHOICE
            ):
                available_tools: list[ToolProficiency] = [
                    t
                    for t in ToolProficiency
                    if t != ToolProficiency.ANY_OF_YOUR_CHOICE
                ]
                resolved.append(self._select_tool_proficiency(available_tools, state))
            elif isinstance(tool, GamingSet) and tool == GamingSet.ANY_OF_YOUR_CHOICE:
                available_gaming_sets: list[GamingSet] = [
                    g for g in GamingSet if g != GamingSet.ANY_OF_YOUR_CHOICE
                ]
                resolved.append(self._select_gaming_set(available_gaming_sets, state))
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
                    self._select_musical_instrument(available_instruments, state)
                )
            else:
                resolved.append(tool)
        delta = ToolProficienciesDelta(tool_proficiencies=tuple(resolved))
        yield delta
        return delta.apply(state)
