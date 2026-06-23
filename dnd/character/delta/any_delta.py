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
from dnd.character.delta.delta import Delta
from dnd.character.delta.feature_delta import FeatureDelta
from dnd.character.delta.initial_data_delta import InitialDataDelta
from dnd.character.delta.magical_items_delta import MagicalItemsDelta
from pydantic import Discriminator
from pydantic import Tag


def _get_delta_type(data: object) -> str | None:
    if isinstance(data, dict):
        return data.get("delta_type")
    if isinstance(data, Delta):
        return data.delta_type
    return None


AnyDelta = Annotated[
    Union[
        Annotated[AgeDelta, Tag("AgeDelta")],
        Annotated[AIChoicesResolutionDelta, Tag("AIChoicesResolutionDelta")],
        Annotated[AlignmentDelta, Tag("AlignmentDelta")],
        Annotated[BackgroundDelta, Tag("BackgroundDelta")],
        Annotated[EquipmentDelta, Tag("EquipmentDelta")],
        Annotated[FeatResolutionDelta, Tag("FeatResolutionDelta")],
        Annotated[FeatsDelta, Tag("FeatsDelta")],
        Annotated[FeatureDelta, Tag("FeatureDelta")],
        Annotated[HealthBaseDelta, Tag("HealthBaseDelta")],
        Annotated[InitialDataDelta, Tag("InitialDataDelta")],
        Annotated[LanguagesDelta, Tag("LanguagesDelta")],
        Annotated[LevelDelta, Tag("LevelDelta")],
        Annotated[MagicalItemsDelta, Tag("MagicalItemsDelta")],
        Annotated[NameDelta, Tag("NameDelta")],
        Annotated[NullDelta, Tag("NullDelta")],
        Annotated[OtherEquipmentDelta, Tag("OtherEquipmentDelta")],
        Annotated[RaceDelta, Tag("RaceDelta")],
        Annotated[SexDelta, Tag("SexDelta")],
        Annotated[SkillsDelta, Tag("SkillsDelta")],
        Annotated[SorcererLevelIncrementDelta, Tag("SorcererLevelIncrementDelta")],
        Annotated[SpellsDelta, Tag("SpellsDelta")],
        Annotated[StatChoiceDelta, Tag("StatChoiceDelta")],
        Annotated[StatsDelta, Tag("StatsDelta")],
        Annotated[SubclassDelta, Tag("SubclassDelta")],
        Annotated[ToolProficienciesDelta, Tag("ToolProficienciesDelta")],
        Annotated[WeaponsDelta, Tag("WeaponsDelta")],
        Annotated[WizardLevelIncrementDelta, Tag("WizardLevelIncrementDelta")],
    ],
    Discriminator(_get_delta_type),
]

__all__ = ["AnyDelta"]
