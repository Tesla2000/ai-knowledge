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
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasStats
from dnd.character.class_levels import ClassLevels
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from pydantic import ConfigDict
from typing import Literal


class FeatResolutionDelta(Delta):
    """Delta produced when FeatChoiceResolver resolves feat placeholders."""

    delta_type: Literal["FeatResolutionDelta"] = "FeatResolutionDelta"
    feats: tuple[FeatName, ...]
    n_stat_choices: int

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasNStatChoices]:

        if TYPE_CHECKING:

            class BlueprintWithFeatsResolved(Blueprint):
                feats: tuple[FeatName, ...]
                n_stat_choices: int

        else:

            class BlueprintWithFeatsResolved(type(state)):
                feats: tuple[FeatName, ...]
                n_stat_choices: int

        return cast(
            ProtocolIntersection[T, HasNStatChoices],
            BlueprintWithFeatsResolved.model_validate(
                {
                    **dict(state),
                    "feats": self.feats,
                    "n_stat_choices": self.n_stat_choices,
                }
            ),
        )


@runtime_checkable
class _FeatT(HasFeats, HasStats, Protocol):
    pass


class FeatChoiceResolver[S: _FeatT](BuildingBlock, ABC):
    """Resolves FeatName.ANY_OF_YOUR_CHOICE placeholders.

    This resolver replaces ANY_OF_YOUR_CHOICE placeholders in the
    blueprint's feats set with concrete FeatName choices.

    Handles special logic for ABILITY_SCORE_IMPROVEMENT:
    - Excluded from choices if character is level 1
    - Converted to n_stat_choices for StatChoiceResolver
    - Filtered out from final feats tuple
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_from_available(
        self, available: list[FeatName], state: S
    ) -> FeatName | None: ...

    @overload
    def get_change[T: _FeatT](
        self, state: T
    ) -> Generator[
        FeatResolutionDelta, None, ProtocolIntersection[T, HasNStatChoices]
    ]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasFeats and HasStats for precise return typing"
    )
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, _FeatT):
            raise TypeError(
                f"{type(self).__name__} requires HasFeats and HasStats, got {type(state).__name__}"
            )
        existing_classes = (
            state.classes if isinstance(state, HasClasses) else ClassLevels()
        )
        ability_score_improvement_allowed = existing_classes.total_level() != 1

        resolved = set()
        for feat in state.feats:
            result = self._resolve_feat(feat, state, ability_score_improvement_allowed)
            resolved.add(result if result is not None else feat)

        n_asi = sum(1 for f in resolved if f == FeatName.ABILITY_SCORE_IMPROVEMENT)
        final_feats = tuple(
            f for f in resolved if f != FeatName.ABILITY_SCORE_IMPROVEMENT
        )

        delta = FeatResolutionDelta(feats=final_feats, n_stat_choices=2 * n_asi)
        yield delta
        return delta.apply(state)

    def _resolve_feat(
        self, feat: FeatName, state: _FeatT, ability_score_improvement_allowed: bool
    ) -> FeatName | None:
        if feat not in FeatName.not_choosables():
            return feat
        excluded = list(FeatName.not_choosables())
        if not ability_score_improvement_allowed:
            excluded.append(FeatName.ABILITY_SCORE_IMPROVEMENT)
        available = [f for f in FeatName if f not in excluded]
        return self._select_from_available(available, state)
