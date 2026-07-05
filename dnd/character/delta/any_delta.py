from __future__ import annotations

from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.alignment_assigner import AlignmentDelta
from dnd.character.blueprint.building_blocks.age_assigner import AgeDelta
from dnd.character.blueprint.building_blocks.background_assigner import BackgroundDelta
from dnd.character.blueprint.building_blocks.equipment_adder import OtherEquipmentDelta
from dnd.character.blueprint.building_blocks.equipment_chooser.base import (
    EquipmentDelta,
)
from dnd.character.blueprint.building_blocks.feat_adder import FeatsDelta
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatResolutionDelta,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.base import (
    LanguagesDelta,
)
from dnd.character.blueprint.building_blocks.level_assigner import LevelDelta
from dnd.character.blueprint.building_blocks.level_up.health_increase.base import (
    HealthBaseDelta,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    SorcererLevelIncrementDelta,
    WizardLevelIncrementDelta,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SpellsDelta,
)
from dnd.character.blueprint.building_blocks.name_assigner import NameDelta
from dnd.character.blueprint.building_blocks.null_block import NullDelta
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceDelta,
)
from dnd.character.blueprint.building_blocks.sex_assigner import SexDelta
from dnd.character.blueprint.building_blocks.skill_choice_resolver.base import (
    SkillsDelta,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.base import (
    StatChoiceDelta,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StatsDelta,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassDelta,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficienciesDelta,
)
from dnd.character.blueprint.building_blocks.weapon_adder import WeaponsDelta
from dnd.character.delta.ai_choices_resolution_delta import AIChoicesResolutionDelta
from dnd.character.delta.feature_delta import FeatureDelta
from dnd.character.delta.initial_data_delta import InitialDataDelta
from dnd.character.delta.magical_items_delta import MagicalItemsDelta
from pydantic import Field


AnyDelta = Annotated[
    Union[
        AgeDelta,
        AIChoicesResolutionDelta,
        AlignmentDelta,
        BackgroundDelta,
        EquipmentDelta,
        FeatResolutionDelta,
        FeatsDelta,
        FeatureDelta,
        HealthBaseDelta,
        InitialDataDelta,
        LanguagesDelta,
        LevelDelta,
        MagicalItemsDelta,
        NameDelta,
        NullDelta,
        OtherEquipmentDelta,
        RaceDelta,
        SexDelta,
        SkillsDelta,
        SorcererLevelIncrementDelta,
        SpellsDelta,
        StatChoiceDelta,
        StatsDelta,
        SubclassDelta,
        ToolProficienciesDelta,
        WeaponsDelta,
        WizardLevelIncrementDelta,
    ],
    Field(discriminator="delta_type"),
]

__all__ = ["AnyDelta"]
