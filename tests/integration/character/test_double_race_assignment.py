from dnd.character.blueprint.building_blocks import (
    RaceAssigner,
)
from dnd.character.builder import Builder
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName


def test_double_race_assignment_fails(base_builder: Builder):
    result = base_builder.add(
        RaceAssigner(
            race=Race.ELF,
            subrace=SubraceName.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK,
        )
    ).build()
    error = result.error
    assert isinstance(error, ValueError)
    assert error.args[0].endswith("already has a race assigned")
