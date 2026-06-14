from __future__ import annotations

import random

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.initial_data_filler.base_filler import (
    InitialDataFiller,
)
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import (
    Background,
)
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

    _IDEALS = (
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

    def get_change(self, blueprint: Blueprint):
        """Fill missing required fields with random mock data."""
        random.seed(self.seed)

        return Blueprint(
            sex=blueprint.sex or random.choice(tuple(Sex)),
            backstory=blueprint.backstory or random.choice(self._BACKSTORIES),
            age=blueprint.age or random.randint(18, 80),
            name=blueprint.name or random.choice(self._NAMES),
            background=blueprint.background or random.choice(tuple(Background)),
            alignment=blueprint.alignment or random.choice(tuple(Alignment)),
            height=blueprint.height or random.randint(150, 210),
            weight=blueprint.weight or random.randint(50, 120),
            eye_color=blueprint.eye_color or random.choice(self._EYE_COLORS),
            skin_color=blueprint.skin_color or random.choice(self._SKIN_COLORS),
            hairstyle=blueprint.hairstyle or random.choice(self._HAIRSTYLES),
            appearance=blueprint.appearance or random.choice(self._APPEARANCES),
            character_traits=blueprint.character_traits
            or random.choice(self._CHARACTER_TRAITS),
            ideals=blueprint.ideals or random.choice(self._IDEALS),
            bonds=blueprint.bonds or random.choice(self._BONDS),
            weaknesses=blueprint.weaknesses or random.choice(self._WEAKNESSES),
        )
