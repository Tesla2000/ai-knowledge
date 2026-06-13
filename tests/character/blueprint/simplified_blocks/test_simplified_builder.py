import pytest
from dnd_character_creator.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseAverage,
)
from dnd_character_creator.character.blueprint.building_blocks.level_up.level_incrementer import (
    LevelIncrementer,
)
from dnd_character_creator.character.blueprint.building_blocks.level_up.spell_assignment import (
    RandomSpellAssigner,
)
from dnd_character_creator.character.blueprint.building_blocks.race_assigner import (
    RaceAssigner,
)
from dnd_character_creator.character.blueprint.simplified_blocks.class_to_stats_priority import (
    CLASS_TO_STATS_PRIORITY,
)
from dnd_character_creator.character.blueprint.simplified_blocks.simplified_blocks import (
    Classes,
)
from dnd_character_creator.character.blueprint.simplified_blocks.simplified_blocks import (
    SimplifiedBlocks,
)
from dnd_character_creator.character.builder import Builder
from dnd_character_creator.character.presentable_character import (
    PresentableCharacter,
)
from dnd_character_creator.character.race.subraces import (
    RACE_TO_SUBRACES,
)
from dnd_character_creator.choices.class_creation.character_class import Class
from frozendict import frozendict
from pydantic import ValidationError

RACE_SUBRACE_PAIRS = tuple(
    (race, subrace)
    for race, subraces in RACE_TO_SUBRACES.items()
    for subrace in subraces
)
RACE_SUBRACE_IDS = [
    f"{race.name}-{subrace.name}" for race, subrace in RACE_SUBRACE_PAIRS
]


class TestSimplifiedBuilder:
    def test_default_configuration_builds_presentable_character(self):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 2}))
        blocks = SimplifiedBlocks(classes=classes)
        builder = Builder(building_blocks=(blocks,))
        result = builder.build()
        assert result.error is None
        assert isinstance(result.character, PresentableCharacter)

    def test_default_values_are_derived_from_classes(self):
        classes = Classes(
            class_levels=frozendict({Class.SORCERER: 1, Class.WIZARD: 2})
        )
        blocks = SimplifiedBlocks(classes=classes)
        assert blocks.stats_priority == CLASS_TO_STATS_PRIORITY[Class.WIZARD]
        assert len(blocks.level_incrementers) == classes.get_total_level()
        assert len(blocks.health_increases) == classes.get_total_level()
        assert len(blocks.spell_assigners) == classes.get_total_level()
        assert len(blocks.level_ups) == classes.get_total_level()

    def test_classes_main_class_defaults_to_highest(self):
        classes = Classes(
            class_levels=frozendict({Class.SORCERER: 3, Class.WIZARD: 5})
        )
        assert classes.main_class == Class.WIZARD
        assert classes.get_total_level() == 8

    def test_classes_total_level_limit_error_message(self):
        with pytest.raises(ValidationError) as exc_info:
            Classes(
                class_levels=frozendict({Class.SORCERER: 1, Class.WIZARD: 20})
            )
        assert "Total level of classes" in str(exc_info.value)
        assert "greater than 20" in str(exc_info.value)

    def test_custom_blocks_skip_auto_population(self):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 1}))
        custom_blocks = (LevelIncrementer(class_=Class.WIZARD),)
        blocks = SimplifiedBlocks(classes=classes, blocks=custom_blocks)
        assert blocks.blocks == custom_blocks

    def test_model_validate_existing_instance_keeps_blocks(self):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 1}))
        blocks = SimplifiedBlocks(classes=classes)
        validated = SimplifiedBlocks.model_validate(blocks)
        assert validated.blocks == blocks.blocks

    def test_valid_custom_configuration_builds_presentable_character(self):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 2}))
        blocks = SimplifiedBlocks(
            classes=classes,
            level_incrementers=(
                LevelIncrementer(class_=Class.WIZARD),
                LevelIncrementer(class_=Class.WIZARD),
            ),
            health_increases=(
                HealthIncreaseAverage(class_=Class.WIZARD),
                HealthIncreaseAverage(class_=Class.WIZARD),
            ),
            spell_assigners=(
                RandomSpellAssigner(class_=Class.WIZARD),
                RandomSpellAssigner(class_=Class.WIZARD),
            ),
        )
        builder = Builder(building_blocks=(blocks,))
        result = builder.build()
        assert result.error is None
        assert isinstance(result.character, PresentableCharacter)

    def test_invalid_level_incrementer_length(self):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 2}))
        with pytest.raises(ValidationError):
            SimplifiedBlocks(
                classes=classes,
                level_incrementers=(LevelIncrementer(class_=Class.WIZARD),),
            )

    def test_invalid_level_incrementer_classes(self):
        classes = Classes(
            class_levels=frozendict({Class.WIZARD: 1, Class.SORCERER: 1})
        )
        with pytest.raises(ValidationError) as exc_info:
            SimplifiedBlocks(
                classes=classes,
                level_incrementers=(
                    LevelIncrementer(class_=Class.WIZARD),
                    LevelIncrementer(class_=Class.WIZARD),
                ),
            )
        assert "increment_classes" in str(exc_info.value)
        assert "don't match class_levels" in str(exc_info.value)

    def test_invalid_health_increase_length(self):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 2}))
        with pytest.raises(ValidationError):
            SimplifiedBlocks(
                classes=classes,
                health_increases=(HealthIncreaseAverage(class_=Class.WIZARD),),
            )

    def test_invalid_health_increase_classes(self):
        classes = Classes(
            class_levels=frozendict({Class.WIZARD: 1, Class.SORCERER: 1})
        )
        with pytest.raises(ValidationError) as exc_info:
            SimplifiedBlocks(
                classes=classes,
                health_increases=(
                    HealthIncreaseAverage(class_=Class.WIZARD),
                    HealthIncreaseAverage(class_=Class.WIZARD),
                ),
            )
        assert "increases_classes" in str(exc_info.value)
        assert "don't match class_levels" in str(exc_info.value)

    def test_invalid_spell_assigner_length(self):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 2}))
        with pytest.raises(ValidationError):
            SimplifiedBlocks(
                classes=classes,
                spell_assigners=(RandomSpellAssigner(class_=Class.WIZARD),),
            )

    def test_invalid_spell_assigner_classes(self):
        classes = Classes(
            class_levels=frozendict({Class.WIZARD: 1, Class.SORCERER: 1})
        )
        with pytest.raises(ValidationError) as exc_info:
            SimplifiedBlocks(
                classes=classes,
                spell_assigners=(
                    RandomSpellAssigner(class_=Class.WIZARD),
                    RandomSpellAssigner(class_=Class.WIZARD),
                ),
            )
        assert "spell_assignment_classes" in str(exc_info.value)
        assert "don't match class_levels" in str(exc_info.value)

    def test_level_up_class_mismatch_validation(self):
        classes = Classes(
            class_levels=frozendict({Class.WIZARD: 1, Class.SORCERER: 1})
        )
        with pytest.raises(ValidationError) as exc_info:
            SimplifiedBlocks(
                classes=classes,
                level_incrementers=(
                    LevelIncrementer(class_=Class.WIZARD),
                    LevelIncrementer(class_=Class.SORCERER),
                ),
                health_increases=(
                    HealthIncreaseAverage(class_=Class.SORCERER),
                    HealthIncreaseAverage(class_=Class.WIZARD),
                ),
                spell_assigners=(
                    RandomSpellAssigner(class_=Class.SORCERER),
                    RandomSpellAssigner(class_=Class.WIZARD),
                ),
            )
        assert "Level increment classes don't match for level=1" in str(
            exc_info.value
        )

    @pytest.mark.parametrize(
        ("race", "subrace"),
        RACE_SUBRACE_PAIRS,
        ids=RACE_SUBRACE_IDS,
    )
    def test_all_races_and_subraces_assign(self, race, subrace):
        classes = Classes(class_levels=frozendict({Class.WIZARD: 1}))
        blocks = SimplifiedBlocks(
            classes=classes,
            race_assigner=RaceAssigner(race=race, subrace=subrace),
        )
        builder = Builder(building_blocks=(blocks,))
        result = builder.build()
        assert result.error is None
        assert isinstance(result.character, PresentableCharacter)
        assert result.character.model_dump()
