from collections import Counter
from collections.abc import Generator
from collections.abc import Mapping
from itertools import chain
from typing import Self

from dnd.character.blueprint.building_blocks import Blocks
from dnd.character.blueprint.building_blocks import (
    LevelAssigner,
)
from dnd.character.blueprint.building_blocks import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomInitialDataFiller,
)
from dnd.character.blueprint.building_blocks import (
    RandomLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks import (
    RandomSkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks import (
    RandomToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AnyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import (
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    AnyEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    AnyFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_first import (
    MaxFirstResolver,
)
from dnd.character.blueprint.building_blocks.initial_builder import (
    InitialBuilder,
)
from dnd.character.blueprint.building_blocks.initial_builder import (
    InitialBuilderBlocks,
)
from dnd.character.blueprint.building_blocks.initial_data_filler import (
    AnyInitialDataFiller,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver import (
    AnyLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    AnyHealthIncrease,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    LevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUp,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import (
    LevelUpBlocks,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    AnySpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    RandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser import (
    AnyMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    AnyRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner import (
    RandomRaceAssigner,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    AnySkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    AnyStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_builder import (
    AnyStatsBuilder,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.stats_priority import (
    StatsPriority,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    AnySubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.optional import (
    OptionalSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver import (
    AnyToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.simplified_blocks.class_to_stats_priority import (
    CLASS_TO_STATS_PRIORITY,
)
from dnd.character.character import ClassLevel
from dnd.choices.class_creation.character_class import Class
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import create_model
from pydantic import Field
from pydantic import model_serializer
from pydantic import model_validator
from pydantic_core.core_schema import SerializationInfo
from pydantic_core.core_schema import SerializerFunctionWrapHandler


class Classes(BaseModel):
    """Represents character class and level configuration.

    Handles multiclass combinations with automatic calculation of the main class
    (highest level class) and validation that total level does not exceed 20.
    """

    model_config = ConfigDict(frozen=True)
    class_levels: Mapping[Class, ClassLevel] = Field(
        min_length=1,
        description="Mapping of character classes to their respective levels",
    )
    main_class: Class = Field(
        default_factory=lambda validated_data: max(
            validated_data["class_levels"],
            key=validated_data["class_levels"].__getitem__,
        ),
        exclude=True,
        description="The class with the highest level, automatically calculated",
    )

    @model_validator(mode="after")
    def _validate_max_level(self) -> Self:
        total_level = self.get_total_level()
        if total_level > 20:
            raise ValueError(
                f"Total level of classes {self.class_levels} is greater than 20"
            )
        return self

    def get_total_level(self) -> ClassLevel:
        return sum(self.class_levels.values())


class _SimplifiedBlocksFields(BaseModel):
    """Configuration fields for the simplified character building process.

    Aggregates all the building block resolvers and assigners needed for character
    creation, with sensible defaults based on class selection and stats priority.
    Automatically constructs dependent fields like level_ups, health_increases,
    and spell_assigners based on class levels.
    """

    classes: Classes = Field(description="Character class and level configuration")
    stats_priority: StatsPriority = Field(
        default_factory=lambda validated_data: (
            CLASS_TO_STATS_PRIORITY[validated_data["classes"].main_class]
            if "classes" in validated_data
            else None
        ),
        description="Ability score priority based on main character class",
        validate_default=True,
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver,
        description="Resolver for choosing bonus languages",
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver,
        description="Resolver for choosing skill proficiencies",
    )
    feat_choice_resolver: AnyFeatChoiceResolver = Field(
        default_factory=lambda validated_data: MaxFirstResolver(
            priority=validated_data["stats_priority"],
            then=RandomFeatChoiceResolver(),
        ),
        description="Resolver for choosing feats, prioritizes class-related feats",
    )
    tool_proficiencies_resolver: AnyToolProficiencyChoiceResolver = Field(
        default_factory=RandomToolProficiencyChoiceResolver,
        description="Resolver for choosing tool proficiencies",
    )
    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=lambda validated_data: PriorityStatChoiceResolver(
            priority=validated_data["stats_priority"]
        ),
        description="Resolver for choosing ability score increases",
    )
    equipment_chooser: AnyEquipmentChooser = Field(
        default_factory=RandomEquipmentChooser,
        description="Chooser for selecting equipment from available options",
    )
    all_choices_resolver: AnyChoiceResolver = Field(
        default_factory=lambda validated_data: AllChoicesResolver(
            blocks=(
                validated_data["language_choice_resolver"],
                validated_data["skill_choice_resolver"],
                validated_data["feat_choice_resolver"],
                validated_data["tool_proficiencies_resolver"],
                validated_data["stat_choice_resolver"],
                validated_data["equipment_chooser"],
            ),
        ),
        description="Combined resolver that handles all character choice decisions",
    )
    level_incrementers: tuple[LevelIncrementer, ...] = Field(
        default_factory=lambda validated_data: (
            tuple(
                chain.from_iterable(
                    (
                        level * (LevelIncrementer(class_=class_),)
                        for class_, level in validated_data[
                            "classes"
                        ].class_levels.items()
                    )
                )
            )
            if "classes" in validated_data
            else None
        ),
        description="Level incrementers for each level, one per class per level",
        validate_default=True,
    )

    @model_validator(mode="after")
    def _verify_correct_number_of_increments(self) -> Self:
        if len(self.level_incrementers) != self.classes.get_total_level():
            raise ValueError(
                f"Number of level increments {len(self.level_incrementers)} doesn't match level {self.classes.get_total_level()}"
            )
        return self

    @model_validator(mode="after")
    def _validate_increments_match_classes(self) -> Self:
        increment_classes = dict(
            Counter(increment.class_ for increment in self.level_incrementers)
        )
        class_levels = dict(self.classes.class_levels)
        if increment_classes == class_levels:
            return self
        raise ValueError(f"{increment_classes=} don't match {class_levels=}")

    health_increases: tuple[AnyHealthIncrease, ...] = Field(
        default_factory=lambda validated_data: (
            tuple(
                chain.from_iterable(
                    (
                        level * (HealthIncreaseAverage(class_=class_),)
                        for class_, level in validated_data[
                            "classes"
                        ].class_levels.items()
                    )
                )
            )
            if "classes" in validated_data
            else None
        ),
        description="Health increase methods for each level, one per class per level",
        validate_default=True,
    )

    @model_validator(mode="after")
    def _verify_correct_number_of_health_increases(self) -> Self:
        if len(self.health_increases) != self.classes.get_total_level():
            raise ValueError(
                f"Number of health increases {len(self.health_increases)} doesn't match level {self.classes.get_total_level()}"
            )
        return self

    @model_validator(mode="after")
    def _validate_health_increases_match_classes(self) -> Self:
        increases_classes = dict(
            Counter(increase.class_ for increase in self.health_increases)
        )
        class_levels = dict(self.classes.class_levels)
        if increases_classes == class_levels:
            return self
        raise ValueError(f"{increases_classes=} don't match {class_levels=}")

    spell_assigners: tuple[AnySpellAssigner, ...] = Field(
        default_factory=lambda validated_data: (
            tuple(
                chain.from_iterable(
                    (
                        level * (RandomSpellAssigner(class_=class_),)
                        for class_, level in validated_data[
                            "classes"
                        ].class_levels.items()
                    )
                )
            )
            if "classes" in validated_data
            else None
        ),
        description="Spell assigners for each level, one per class per level",
        validate_default=True,
    )

    @model_validator(mode="after")
    def _verify_correct_number_of_spell_assignments(self) -> Self:
        if len(self.spell_assigners) != self.classes.get_total_level():
            raise ValueError(
                f"Number of health increases {len(self.spell_assigners)} doesn't match level {self.classes.get_total_level()}"
            )
        return self

    @model_validator(mode="after")
    def _validate_spell_assigners_match_classes(self) -> Self:
        spell_assignment_classes = dict(
            Counter(increase.class_ for increase in self.spell_assigners)
        )
        class_levels = dict(self.classes.class_levels)
        if spell_assignment_classes == class_levels:
            return self
        raise ValueError(f"{spell_assignment_classes=} don't match {class_levels=}")

    level_ups: tuple[LevelUp, ...] = Field(
        default_factory=lambda validated_data: (
            tuple(
                LevelUp(
                    blocks=LevelUpBlocks(
                        level_increment=level,
                        health_increase=health,
                        spell_assigner=spell,
                        all_choice_resolver=validated_data["all_choices_resolver"],
                    ),
                )
                for level, health, spell in zip(
                    validated_data["level_incrementers"],
                    validated_data["health_increases"],
                    validated_data["spell_assigners"],
                )
            )
            if all(
                map(
                    validated_data.__contains__,
                    (
                        "level_incrementers",
                        "health_increases",
                        "spell_assigners",
                        "all_choices_resolver",
                    ),
                )
            )
            else None
        ),
        validate_default=True,
        description="Level up blocks combining level increment, health, and spell assignment",
    )

    @model_validator(mode="after")
    def _validate_level_up_classes_correspondence(self) -> Self:
        invalid_level_ups = []
        for level, level_up in enumerate(self.level_ups, 1):
            blocks = level_up.blocks
            if (
                blocks.level_increment.class_
                == blocks.health_increase.class_
                == blocks.spell_assigner.class_
            ):
                continue
            invalid_level_ups.append(
                f"Level increment classes don't match for {level=}"
            )
        if invalid_level_ups:
            raise ValueError("\n".join(invalid_level_ups))
        return self

    stats_builder: AnyStatsBuilder = Field(
        default_factory=lambda validated_data: (
            StandardArray(stats_priority=validated_data["stats_priority"])
            if "stats_priority" in validated_data
            else None
        ),
        validate_default=True,
        description="Builder for generating ability scores using standard array method",
    )
    race_assigner: AnyRaceAssigner = Field(
        default_factory=RandomRaceAssigner,
        validate_default=True,
        description="Assigner for selecting character race and subrace",
    )
    initial_builder: InitialBuilder = Field(
        default_factory=lambda validated_data: (
            InitialBuilder(
                blocks=InitialBuilderBlocks(
                    level_assigner=LevelAssigner(
                        level=validated_data["classes"].get_total_level()
                    ),
                    stats_builder=validated_data["stats_builder"],
                    race_assigner=validated_data["race_assigner"],
                    all_choices_resolver=validated_data["all_choices_resolver"],
                )
            )
            if all(
                map(
                    validated_data.__contains__,
                    (
                        "classes",
                        "stats_builder",
                        "race_assigner",
                        "all_choices_resolver",
                    ),
                )
            )
            else None
        ),
        validate_default=True,
        description="Builder for initial character generation including level, stats, and race",
    )
    initial_data_filler: AnyInitialDataFiller = Field(
        default_factory=RandomInitialDataFiller,
        description="Filler for generating initial character data like name and background",
    )
    subclass_assigners: tuple[AnySubclassAssigner, ...] = Field(
        default_factory=lambda validated_data: (
            tuple(
                OptionalSubclassAssigner(
                    class_=class_,
                    assigner=RandomSubclassAssigner(class_=class_),
                )
                for class_ in validated_data["classes"].class_levels
            )
            if "classes" in validated_data
            else None
        ),
        validate_default=True,
        description="Assigners for selecting subclasses, one per character class",
    )
    magical_items_assigner: AnyMagicalItemChooser = Field(
        default_factory=RandomMagicalItemChooser,
        description="Chooser for assigning magical items to character",
    )


EXCLUDE_FACTORY_DEFAULTS = "exclude_factory_defaults"


class SimplifiedBlocks(CombinedBlock, _SimplifiedBlocksFields):
    """Simplified building blocks pipeline for complete character creation.

    Combines initial character generation, data filling, level progression,
    subclass selection, and magical item assignment into a single orchestrated
    building process. This is the primary entry point for creating fully-formed
    D&D 5e characters with all attributes, choices, and equipment resolved.
    """

    blocks: Blocks = Field(
        default_factory=lambda validated_data: (
            (
                validated_data["initial_builder"],
                validated_data["initial_data_filler"],
                CombinedBlock(blocks=validated_data["level_ups"]),
                CombinedBlock(blocks=validated_data["subclass_assigners"]),
                validated_data["magical_items_assigner"],
            )
            if all(
                map(
                    validated_data.__contains__,
                    (
                        "initial_builder",
                        "initial_data_filler",
                        "level_ups",
                        "subclass_assigners",
                        "magical_items_assigner",
                    ),
                )
            )
            else None
        ),
        validate_default=True,
        description="Ordered building blocks executed sequentially: initial build, data fill, level ups, subclasses, and magic items",
    )

    @model_serializer(mode="wrap")
    def _exclude_factory_defaults(
        self, nxt: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> Mapping[str, object]:  # ignore
        serialized_value = nxt(self)
        context = info.context
        if not (isinstance(context, dict) and context.get(EXCLUDE_FACTORY_DEFAULTS)):
            return serialized_value  # type: ignore[no-any-return]
        differences = {"classes": self.classes}
        for field_name, partial_model in _PARTIAL_MODELS:
            if partial_model.model_validate(
                differences
            ) != partial_model.model_validate(serialized_value):
                differences[field_name] = serialized_value[field_name]
        return differences


def _partial_models_creator() -> Generator[tuple[str, type[BaseModel]], None, None]:
    combined_fields = {}
    for field_name, field_info in SimplifiedBlocks.model_fields.items():
        combined_fields[field_name] = (field_info.annotation, field_info)
        yield field_name, create_model("Partial", **combined_fields)  # type: ignore[call-overload]


_PARTIAL_MODELS: tuple[tuple[str, type[BaseModel]], ...] = tuple(
    _partial_models_creator()
)
