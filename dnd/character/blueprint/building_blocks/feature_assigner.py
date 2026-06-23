from __future__ import annotations

from collections.abc import Generator

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasOtherAbilities
from dnd.character.delta.feature_delta import FeatureDelta
from dnd.character.feature.feature import Feature
from pydantic import Field


class FeatureAssigner(
    BuildingBlock[BlueprintProtocol, FeatureDelta, HasOtherAbilities]
):
    """Building block that assigns a feature to a character blueprint.

    Example:
        >>> trance = Feature(...)
        >>> trance_assigner = FeatureAssigner(feature=trance)
    """

    feature: Feature = Field(
        description="Character feature to assign (ability, trait, or stat boost)"
    )

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[FeatureDelta, None, HasOtherAbilities]:
        existing = (
            state.other_active_abilities if isinstance(state, HasOtherAbilities) else ()
        )
        delta = FeatureDelta(other_active_abilities=existing)
        yield delta
        return delta.apply(state)
