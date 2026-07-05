from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import overload
from typing import Protocol
from typing import runtime_checkable
from typing import TYPE_CHECKING

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasStats
from dnd.character.delta.delta import Delta
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic
from pydantic import ConfigDict
from pydantic import NonNegativeInt
from typing import Literal


class StatChoiceDelta(Delta):
    """Delta produced when StatChoiceResolver resolves stat choices."""

    delta_type: Literal["StatChoiceDelta"] = "StatChoiceDelta"
    stats: Stats
    n_stat_choices: NonNegativeInt

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasStats]:

        if TYPE_CHECKING:

            class BlueprintWithStats(Blueprint):
                stats: Stats
                n_stat_choices: NonNegativeInt

        else:

            class BlueprintWithStats(type(state)):
                stats: Stats
                n_stat_choices: NonNegativeInt

        return cast(
            ProtocolIntersection[T, HasStats],
            BlueprintWithStats.model_validate(
                {
                    **dict(state),
                    "stats": self.stats,
                    "n_stat_choices": self.n_stat_choices,
                }
            ),
        )


@runtime_checkable
class _StatT(HasStats, HasNStatChoices, Protocol):
    pass


class StatChoiceResolver(BuildingBlock, ABC):
    """Abstract base for resolving n_stat_choices.

    When a race/subrace grants ability score increases of the player's choice
    (n_stat_choices > 0), this component determines which stats to increase.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def select_stats_to_increase(self, state: _StatT) -> dict[Statistic, int]: ...

    @overload
    def get_change[T: _StatT](
        self, state: T
    ) -> Generator[StatChoiceDelta, None, ProtocolIntersection[T, HasStats]]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasStats and HasNStatChoices for precise return typing"
    )
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, _StatT):
            raise TypeError(
                f"{type(self).__name__} requires HasStats and HasNStatChoices, got {type(state).__name__}"
            )
        if state.n_stat_choices == 0:
            delta = StatChoiceDelta(stats=state.stats, n_stat_choices=0)
            yield delta
            return delta.apply(state)

        stat_increases = self.select_stats_to_increase(state)
        new_stats = Stats(
            strength=state.stats.strength + stat_increases.get(Statistic.STRENGTH, 0),
            dexterity=state.stats.dexterity
            + stat_increases.get(Statistic.DEXTERITY, 0),
            constitution=state.stats.constitution
            + stat_increases.get(Statistic.CONSTITUTION, 0),
            intelligence=state.stats.intelligence
            + stat_increases.get(Statistic.INTELLIGENCE, 0),
            wisdom=state.stats.wisdom + stat_increases.get(Statistic.WISDOM, 0),
            charisma=state.stats.charisma + stat_increases.get(Statistic.CHARISMA, 0),
        )
        delta = StatChoiceDelta(stats=new_stats, n_stat_choices=0)
        yield delta
        return delta.apply(state)
