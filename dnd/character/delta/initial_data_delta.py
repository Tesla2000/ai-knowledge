from __future__ import annotations

from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasInitialData
from dnd.character.delta.delta import Delta
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.sex import Sex
from pydantic import PositiveInt
from typing import Literal


class InitialDataDelta(Delta):
    """Delta produced when InitialDataFiller assigns all required flavor fields."""

    delta_type: Literal["InitialDataDelta"] = "InitialDataDelta"
    name: str
    sex: Sex
    age: PositiveInt
    background: Background
    alignment: Alignment
    backstory: str
    height: PositiveInt
    weight: PositiveInt
    eye_color: str
    skin_color: str
    hairstyle: str
    appearance: str
    character_traits: str
    ideals: str
    bonds: str
    weaknesses: str

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasInitialData]:
        if TYPE_CHECKING:

            class BlueprintWithInitialData(Blueprint):
                name: str
                sex: Sex
                age: PositiveInt
                background: Background
                alignment: Alignment
                backstory: str
                height: PositiveInt
                weight: PositiveInt
                eye_color: str
                skin_color: str
                hairstyle: str
                appearance: str
                character_traits: str
                ideals: str
                bonds: str
                weaknesses: str

        else:

            class BlueprintWithInitialData(type(state)):
                name: str
                sex: Sex
                age: PositiveInt
                background: Background
                alignment: Alignment
                backstory: str
                height: PositiveInt
                weight: PositiveInt
                eye_color: str
                skin_color: str
                hairstyle: str
                appearance: str
                character_traits: str
                ideals: str
                bonds: str
                weaknesses: str

        return cast(
            ProtocolIntersection[T, HasInitialData],
            BlueprintWithInitialData.model_validate(
                dict(state)
                | {
                    "name": self.name,
                    "sex": self.sex,
                    "age": self.age,
                    "background": self.background,
                    "alignment": self.alignment,
                    "backstory": self.backstory,
                    "height": self.height,
                    "weight": self.weight,
                    "eye_color": self.eye_color,
                    "skin_color": self.skin_color,
                    "hairstyle": self.hairstyle,
                    "appearance": self.appearance,
                    "character_traits": self.character_traits,
                    "ideals": self.ideals,
                    "bonds": self.bonds,
                    "weaknesses": self.weaknesses,
                }
            ),
        )
