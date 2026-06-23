from __future__ import annotations

from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasOtherAbilities
from dnd.character.delta.delta import Delta


class FeatureDelta(Delta):
    """Delta produced when FeatureAssigner applies a feature's active abilities."""

    other_active_abilities: tuple[str, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasOtherAbilities]:
        if TYPE_CHECKING:

            class BlueprintWithOtherAbilities(Blueprint):
                other_active_abilities: tuple[str, ...]

        else:

            class BlueprintWithOtherAbilities(type(state)):
                other_active_abilities: tuple[str, ...]

        return cast(
            ProtocolIntersection[T, HasOtherAbilities],
            BlueprintWithOtherAbilities.model_validate(
                dict(state) | {"other_active_abilities": self.other_active_abilities}
            ),
        )
