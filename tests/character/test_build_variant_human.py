from __future__ import annotations

from dnd_character_creator.character.blueprint.building_blocks import (
    RaceAssigner,
)
from dnd_character_creator.character.blueprint.simplified_blocks import (
    SimplifiedBlocks,
)
from dnd_character_creator.character.blueprint.simplified_blocks.simplified_blocks import (
    Classes,
)
from dnd_character_creator.character.builder import Builder
from dnd_character_creator.character.race.race import Race
from dnd_character_creator.character.race.subraces import Subrace
from dnd_character_creator.choices.class_creation.character_class import Class
from dotenv import load_dotenv

load_dotenv()


class TestBuildVariantHuman:
    def test_build_variant_human(self):
        result = Builder(
            building_blocks=(
                SimplifiedBlocks(
                    classes=Classes(class_levels={Class.WIZARD: 1}),
                    race_assigner=RaceAssigner(
                        race=Race.HUMAN,
                        subrace=Subrace.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK,
                    ),
                ),
            )
        ).build()
        assert result.character.feats
