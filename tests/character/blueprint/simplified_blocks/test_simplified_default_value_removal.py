from dnd_character_creator.character.blueprint.building_blocks.race_assigner import (
    RaceAssigner,
)
from dnd_character_creator.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd_character_creator.character.blueprint.simplified_blocks.class_to_stats_priority import (
    CLASS_TO_STATS_PRIORITY,
)
from dnd_character_creator.character.blueprint.simplified_blocks.simplified_blocks import (
    Classes,
)
from dnd_character_creator.character.blueprint.simplified_blocks.simplified_blocks import (
    EXCLUDE_FACTORY_DEFAULTS,
)
from dnd_character_creator.character.blueprint.simplified_blocks.simplified_blocks import (
    SimplifiedBlocks,
)
from dnd_character_creator.character.race.race import Race
from dnd_character_creator.character.race.subraces import Subrace
from dnd_character_creator.choices.class_creation.character_class import Class
from dnd_character_creator.choices.stats_creation.statistic import Statistic
from frozendict import frozendict


class TestSimplifiedBuilder:
    def test_default_values_removal_all_defaults(self):
        """Test that all default values are excluded when nothing is customized."""
        classes = Classes(class_levels={Class.WIZARD: 1})
        blocks = SimplifiedBlocks(classes=classes)
        blocks = SimplifiedBlocks.model_validate(blocks.model_dump())
        result = blocks.model_dump(context={EXCLUDE_FACTORY_DEFAULTS: True})
        assert result == {"classes": classes.model_dump()}

    def test_default_values_removal_with_custom_stats_priority(self):
        """Test that all default values are excluded when nothing is customized."""
        classes = Classes(class_levels={Class.WIZARD: 1})
        default_priority = CLASS_TO_STATS_PRIORITY[Class.WIZARD]
        custom_priority = (
            Statistic.INTELLIGENCE,
            Statistic.CONSTITUTION,
            Statistic.DEXTERITY,
            Statistic.WISDOM,
            Statistic.CHARISMA,
            Statistic.STRENGTH,
        )

        assert (
            custom_priority != default_priority
        ), "Custom priority should differ from default"

        blocks = SimplifiedBlocks(
            classes=classes, stats_priority=custom_priority
        )
        blocks = SimplifiedBlocks.model_validate(blocks.model_dump())
        result = blocks.model_dump(
            context={EXCLUDE_FACTORY_DEFAULTS: True},
            exclude={"blocks"},
        )
        assert result == {
            "classes": classes.model_dump(),
            "stats_priority": custom_priority,
        }

    def test_default_values_removal_with_custom_stats_priorities(self):
        """Test that all default values are excluded when nothing is customized."""
        classes = Classes(class_levels={Class.WIZARD: 1})
        default_priority = CLASS_TO_STATS_PRIORITY[Class.WIZARD]
        custom_priority = (
            Statistic.INTELLIGENCE,
            Statistic.CONSTITUTION,
            Statistic.DEXTERITY,
            Statistic.WISDOM,
            Statistic.CHARISMA,
            Statistic.STRENGTH,
        )

        assert (
            custom_priority != default_priority
        ), "Custom priority should differ from default"

        default_stat_choice_resolver = SimplifiedBlocks(
            classes=classes
        ).stat_choice_resolver
        blocks = SimplifiedBlocks(
            classes=classes,
            stats_priority=custom_priority,
            stat_choice_resolver=default_stat_choice_resolver,
        )
        blocks = SimplifiedBlocks.model_validate(blocks.model_dump())
        result = blocks.model_dump(
            context={EXCLUDE_FACTORY_DEFAULTS: True},
            exclude={"blocks"},
        )
        assert result == {
            "classes": classes.model_dump(),
            "stats_priority": custom_priority,
            "stat_choice_resolver": default_stat_choice_resolver.model_dump(),
        }

    def test_default_values_removal_with_custom_race_assigner(self):
        """Test that custom race_assigner is preserved in the diff."""
        classes = Classes(class_levels={Class.WIZARD: 1})

        # Provide a specific race instead of random
        custom_race_assigner = RaceAssigner(
            race=Race.HUMAN,
            subrace=Subrace.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
        )

        blocks = SimplifiedBlocks(
            classes=classes, race_assigner=custom_race_assigner
        )

        result = blocks.model_dump(context={EXCLUDE_FACTORY_DEFAULTS: True})

        # The result should contain race_assigner since it's not the default RandomRaceAssigner
        assert (
            "race_assigner" in result
        ), "Custom race_assigner should be in result"

    def test_default_values_removal_with_custom_stats_builder(self):
        """Test that custom stats_builder with different priority is preserved."""
        classes = Classes(class_levels=frozendict({Class.SORCERER: 1}))

        # Create a stats builder with custom priority
        custom_priority = (
            Statistic.CHARISMA,
            Statistic.INTELLIGENCE,
            Statistic.WISDOM,
            Statistic.STRENGTH,
            Statistic.DEXTERITY,
            Statistic.CONSTITUTION,
        )
        custom_stats_builder = StandardArray(stats_priority=custom_priority)

        blocks = SimplifiedBlocks(
            classes=classes, stats_builder=custom_stats_builder
        )

        result = blocks.model_dump(context={EXCLUDE_FACTORY_DEFAULTS: True})

        # The result should contain stats_builder since the priority differs
        assert (
            "stats_builder" in result
        ), "Custom stats_builder should be in result"

    def test_roundtrip_validation(self):
        """Test that difference dict can be used to reconstruct the object."""
        classes = Classes(class_levels={Class.WIZARD: 1})
        blocks = SimplifiedBlocks(classes=classes)

        # Get the difference (should be empty for all defaults)
        difference = blocks.model_dump(
            context={EXCLUDE_FACTORY_DEFAULTS: True}
        )

        # Reconstruct from difference
        reconstructed = SimplifiedBlocks.model_validate(
            {"classes": classes, **difference}
        )

        # Should be equal
        assert blocks == reconstructed
