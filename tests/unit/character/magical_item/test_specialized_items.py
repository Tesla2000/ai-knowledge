from __future__ import annotations

import pytest

from dnd.character.character import Character
from dnd.character.magical_item.level import Level
from dnd.character.magical_item.source import Source
from dnd.character.magical_item.specialized_items.robe_of_archmagi import (
    RobeOfTheArchmagi,
)
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.sex import Sex

_STATS = Stats(
    strength=10,
    dexterity=14,
    constitution=10,
    intelligence=18,
    wisdom=10,
    charisma=10,
)

_BASE_KWARGS: dict[str, object] = dict(
    name="TestChar",
    stats=_STATS,
    speed=30,
    dark_vision_range=0,
    saving_throw_proficiencies=(),
    other_active_abilities=(),
    sex=Sex.FEMALE,
    backstory="A wizard.",
    level=1,
    age=25,
    race=Race.HUMAN,
    subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
    background=Background.SAGE,
    alignment=Alignment.CHAOTIC_GOOD,
    health_base=6,
    height=65,
    weight=130,
    eye_color="blue",
    skin_color="fair",
    hairstyle="long",
    appearance="slender",
    character_traits="curious",
    ideals="knowledge",
    bonds="books",
    weaknesses="overconfident",
)


@pytest.mark.unit
class TestRobeOfTheArchmagi:
    def test_calc_ac_uses_base_plus_dex_modifier(self) -> None:
        char = Character(**_BASE_KWARGS)
        robe = RobeOfTheArchmagi(
            description="Legendary arcane robe",
            level=Level.LEGENDARY,
            source=Source.DMG,
            attuned=True,
        )
        ac = robe.calc_ac(char)
        assert ac == 15 + 2
