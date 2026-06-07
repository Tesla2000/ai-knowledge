from __future__ import annotations

from dnd.character.race.race import Race
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import (
    Background,
)
from dnd.choices.sex import Sex
from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt


class CharacterBaseTemplate(BaseModel):
    """Template for AI-generated basic character parameters.

    This model defines the structure for generating core character attributes
    using LLM structured output. All fields have descriptions to guide the AI
    in making appropriate choices.
    """

    name: str = Field(
        description="Character's full name, appropriate for their race and background."
    )

    sex: Sex = Field(description="Character's biological sex.")

    age: PositiveInt = Field(
        description="Character's age in years, appropriate for their race. "
        "Consider racial lifespans: elves live centuries, humans decades."
    )

    race: Race = Field(
        description="Character's race. Choose based on character concept and setting."
    )

    background: Background = Field(
        description="Character's background representing their life before adventuring. "
        "Should align with character concept and backstory."
    )

    alignment: Alignment = Field(
        description="Character's moral and ethical outlook. Should fit personality and backstory."
    )

    backstory: str = Field(
        description="Character's personal history, motivations, and life story before adventuring."
    )

    height: PositiveInt = Field(
        description="Character's height in inches. Should be appropriate for their race and sex."
    )

    weight: PositiveInt = Field(
        description="Character's weight in pounds. Should be appropriate for their race and sex."
    )

    eye_color: str = Field(
        description="Color of character's eyes. Can be typical or exotic based on race."
    )

    skin_color: str = Field(
        description="Character's skin tone or color. Should be appropriate for their race."
    )

    hairstyle: str = Field(
        description="Description of character's hairstyle and hair color."
    )

    appearance: str = Field(
        description="Overall physical description of the character, including distinctive features."
    )

    character_traits: str = Field(
        description="Personality traits that define how the character behaves and interacts."
    )

    ideals: str = Field(
        description="Core beliefs and principles that guide the character's actions."
    )

    bonds: str = Field(
        description="Connections to people, places, or things that the character cares about."
    )

    weaknesses: str = Field(
        description="Flaws or weaknesses in the character's personality or past."
    )
