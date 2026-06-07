from __future__ import annotations

from dnd.character.blueprint.building_blocks.all_choices_resolver.base_resolver import (
    AllChoicesResolverBase,
)
from dnd.character.blueprint.building_blocks.building_block import (
    CombinedBlock,
)
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    AnyEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    AnyFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver import (
    AnyLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    AnySkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    AnyStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver import (
    AnyToolProficiencyChoiceResolver,
)
from pydantic import Field


class AllChoicesResolver(AllChoicesResolverBase, CombinedBlock):
    """Resolves all character choices by chaining individual resolvers sequentially.

    Combines language, skill, feat, tool, stat, and equipment resolvers into a
    single pipeline that processes all character choices in order. Each resolver
    handles its specific choice type independently.

    Example:
        >>> resolver = AllChoicesResolver(blocks=(
        ...     RandomLanguageChoiceResolver(),
        ...     RandomSkillChoiceResolver(),
        ...     RandomFeatChoiceResolver(),
        ...     RandomToolProficiencyChoiceResolver(),
        ...     PriorityStatChoiceResolver(priority=stats_priority),
        ...     RandomEquipmentChooser(),
        ... ))
    """

    blocks: tuple[
        AnyLanguageChoiceResolver,
        AnySkillChoiceResolver,
        AnyFeatChoiceResolver,
        AnyToolProficiencyChoiceResolver,
        AnyStatChoiceResolver,
        AnyEquipmentChooser,
    ] = Field(
        description="Ordered sequence of choice resolvers: language, skill, feat, tool, stat, and equipment",
    )
