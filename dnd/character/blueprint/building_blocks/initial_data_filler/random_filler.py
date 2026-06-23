from __future__ import annotations

import random
from collections.abc import Generator


from dnd.character.blueprint.building_blocks.initial_data_filler.base_filler import (
    InitialDataFiller,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasAge
from dnd.character.blueprint.state import HasAlignment
from dnd.character.blueprint.state import HasAppearance
from dnd.character.blueprint.state import HasBackground
from dnd.character.blueprint.state import HasBackstory
from dnd.character.blueprint.state import HasBonds
from dnd.character.blueprint.state import HasCharacterTraits
from dnd.character.blueprint.state import HasEyeColor
from dnd.character.blueprint.state import HasHairstyle
from dnd.character.blueprint.state import HasHeight
from dnd.character.blueprint.state import HasIdeals
from dnd.character.blueprint.state import HasInitialData
from dnd.character.blueprint.state import HasName
from dnd.character.blueprint.state import HasSex
from dnd.character.blueprint.state import HasSkinColor
from dnd.character.blueprint.state import HasWeaknesses
from dnd.character.blueprint.state import HasWeight
from dnd.character.delta.initial_data_delta import InitialDataDelta
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.sex import Sex
from pydantic import ConfigDict
from pydantic import Field


class RandomInitialDataFiller(InitialDataFiller):
    """Fills missing required Character fields with random mock data.

    Only fills fields that are currently None. Does not overwrite existing values.

    Example:
        >>> filler = RandomInitialDataFiller(seed=42)  # Reproducible
        >>> # or
        >>> filler = RandomInitialDataFiller()  # Truly random
    """

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    _BACKSTORIES: tuple[str, ...] = (
        "A mysterious wanderer with a hidden past.",
        "Raised by wolves in the wilderness.",
        "Former noble seeking redemption.",
        "Orphaned at a young age, learned to survive on the streets.",
        "Trained in a secret monastery high in the mountains.",
        "Escaped from captivity and now seeks freedom.",
        "Born under a bad omen, destined for greatness.",
        "Grew up in a small village, dreaming of adventure.",
    )

    _NAMES: tuple[str, ...] = (
        "Aldric",
        "Theron",
        "Lyra",
        "Kael",
        "Mira",
        "Torin",
        "Sera",
        "Dax",
        "Nyx",
        "Finn",
        "Aria",
        "Rex",
        "Zara",
        "Vale",
        "Nova",
        "Cruz",
    )

    _EYE_COLORS: tuple[str, ...] = (
        "blue",
        "brown",
        "green",
        "hazel",
        "amber",
        "gray",
        "violet",
        "black",
    )

    _SKIN_COLORS: tuple[str, ...] = (
        "pale",
        "fair",
        "olive",
        "tan",
        "bronze",
        "dark",
        "ebony",
        "copper",
    )

    _HAIRSTYLES: tuple[str, ...] = (
        "short and messy",
        "long and flowing",
        "braided",
        "bald",
        "ponytail",
        "wild curls",
        "straight and sleek",
        "spiky",
        "tied back",
    )

    _APPEARANCES: tuple[str, ...] = (
        "Tall and muscular with a commanding presence.",
        "Small and wiry, quick on their feet.",
        "Average height with unremarkable features.",
        "Scarred and battle-worn.",
        "Graceful and elegant in movement.",
        "Rugged with weather-beaten features.",
    )

    _CHARACTER_TRAITS: tuple[str, ...] = (
        "Brave and honorable, always helps those in need.",
        "Cunning and resourceful, always has a plan.",
        "Hot-headed and impulsive, acts before thinking.",
        "Calm and analytical, carefully considers all options.",
        "Friendly and outgoing, makes friends easily.",
        "Mysterious and reserved, keeps secrets.",
    )

    _IDEALS: tuple[str, ...] = (
        "Freedom: Everyone deserves to be free.",
        "Honor: My word is my bond.",
        "Knowledge: The pursuit of knowledge is paramount.",
        "Power: Strength is the only thing that matters.",
        "Redemption: Everyone deserves a second chance.",
        "Justice: Wrongdoers must be punished.",
    )

    _BONDS: tuple[str, ...] = (
        "I would die for my family.",
        "I owe everything to my mentor.",
        "I seek revenge against those who wronged me.",
        "I protect the innocent at all costs.",
        "My homeland will always be my true home.",
        "I have a rival who pushes me to be better.",
    )

    _WEAKNESSES: tuple[str, ...] = (
        "I can't resist a good tavern and strong drink.",
        "I'm terrible with money and always broke.",
        "I trust too easily and get betrayed often.",
        "I hold grudges and never forget a slight.",
        "I'm overconfident and underestimate dangers.",
        "I have a secret that could ruin me if discovered.",
    )

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[InitialDataDelta, None, HasInitialData]:
        """Fill missing required fields with random mock data."""
        random.seed(self.seed)

        delta = InitialDataDelta(
            sex=state.sex if isinstance(state, HasSex) else random.choice(tuple(Sex)),
            backstory=state.backstory
            if isinstance(state, HasBackstory)
            else random.choice(self._BACKSTORIES),
            age=state.age if isinstance(state, HasAge) else random.randint(18, 80),
            name=state.name
            if isinstance(state, HasName)
            else random.choice(self._NAMES),
            background=state.background
            if isinstance(state, HasBackground)
            else random.choice(tuple(Background)),
            alignment=state.alignment
            if isinstance(state, HasAlignment)
            else random.choice(tuple(Alignment)),
            height=state.height
            if isinstance(state, HasHeight)
            else random.randint(150, 210),
            weight=state.weight
            if isinstance(state, HasWeight)
            else random.randint(50, 120),
            eye_color=state.eye_color
            if isinstance(state, HasEyeColor)
            else random.choice(self._EYE_COLORS),
            skin_color=state.skin_color
            if isinstance(state, HasSkinColor)
            else random.choice(self._SKIN_COLORS),
            hairstyle=state.hairstyle
            if isinstance(state, HasHairstyle)
            else random.choice(self._HAIRSTYLES),
            appearance=state.appearance
            if isinstance(state, HasAppearance)
            else random.choice(self._APPEARANCES),
            character_traits=state.character_traits
            if isinstance(state, HasCharacterTraits)
            else random.choice(self._CHARACTER_TRAITS),
            ideals=state.ideals
            if isinstance(state, HasIdeals)
            else random.choice(self._IDEALS),
            bonds=state.bonds
            if isinstance(state, HasBonds)
            else random.choice(self._BONDS),
            weaknesses=state.weaknesses
            if isinstance(state, HasWeaknesses)
            else random.choice(self._WEAKNESSES),
        )
        yield delta
        return delta.apply(state)
