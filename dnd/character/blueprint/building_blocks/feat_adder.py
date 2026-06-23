from __future__ import annotations

from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasFeats
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from pydantic import Field


class FeatsDelta(Delta):
    """Delta produced when FeatAdder appends a feat."""

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


class FeatAdder[T: HasFeats](BuildingBlock[T, FeatsDelta, HasFeats]):
    """Adds a feat to the character's feat list."""

    feat: FeatName = Field(description="Feat to add to character's feat list")

    def get_change(
        self, state: T
    ) -> Generator[FeatsDelta, None, ProtocolIntersection[T, HasFeats]]:
        if self.feat in state.feats:
            raise ValueError(f"Feat {self.feat} already exists in character feats")
        delta = FeatsDelta(feats=state.feats + (self.feat,))
        yield delta
        return delta.apply(state)
