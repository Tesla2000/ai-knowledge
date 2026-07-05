from __future__ import annotations

from dnd.character.blueprint.building_blocks import (
    RaceAssigner,
)
from dnd.character.blueprint.simplified_blocks import (
    SimplifiedBlocks,
)
from dnd.character.blueprint.simplified_blocks.simplified_blocks import (
    Classes,
)
from dnd.character.builder import Builder
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.choices.class_creation.character_class import Class
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
                        subrace=SubraceName.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK,
                    ),
                ),
            )
        ).build()
        assert result.character.feats
