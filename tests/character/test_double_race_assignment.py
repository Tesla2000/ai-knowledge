from dnd_character_creator.character.blueprint.building_blocks import (
    RaceAssigner,
)
from dnd_character_creator.character.builder import Builder
from dnd_character_creator.character.race.race import Race
from dnd_character_creator.character.race.subraces import Subrace


def test_double_race_assignment_fails(base_builder: Builder):
    result = base_builder.add(
        RaceAssigner(
            race=Race.ELF,
            subrace=Subrace.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK,
        )
    ).build()
    error = result.error
    assert isinstance(error, ValueError)
    assert error.args[0].endswith("already has a race assigned")
