from __future__ import annotations

from collections.abc import Generator
from typing import Literal
from typing import cast
from typing import overload
from typing import TYPE_CHECKING

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasFeats
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import Field


class FeatsDelta(Delta):
    """Delta produced when FeatAdder appends a feat."""

    delta_type: Literal["FeatsDelta"] = "FeatsDelta"
    feats: tuple[FeatName, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasFeats]:

        if TYPE_CHECKING:

            class BlueprintWithFeats(Blueprint):
                feats: tuple[FeatName, ...]

        else:

            class BlueprintWithFeats(type(state)):
                feats: tuple[FeatName, ...]

        return cast(
            ProtocolIntersection[T, HasFeats],
            BlueprintWithFeats.model_validate({**dict(state), "feats": self.feats}),
        )


class FeatAdder(BuildingBlock):
    """Adds a feat to the character's feat list."""

    type: Literal[BuildingBlockType.FEAT_ADDER] = BuildingBlockType.FEAT_ADDER

    feat: FeatName = Field(description="Feat to add to character's feat list")

    @overload
    def get_change[T: HasFeats](
        self, state: T
    ) -> Generator[FeatsDelta, None, ProtocolIntersection[T, HasFeats]]: ...

    @overload
    @deprecated("Pass a state satisfying HasFeats for precise return typing")
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, HasFeats):
            raise TypeError(
                f"{type(self).__name__} requires HasFeats, got {type(state).__name__}"
            )
        if self.feat in state.feats:
            raise ValueError(f"Feat {self.feat} already exists in character feats")
        delta = FeatsDelta(feats=state.feats + (self.feat,))
        yield delta
        return delta.apply(state)
