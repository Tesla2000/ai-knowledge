from __future__ import annotations

from collections.abc import Generator
from typing import Literal

from dnd.character.blueprint.building_blocks.all_choices_resolver.base_resolver import (
    AllChoicesResolverBase,
)
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
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
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver import (
    AnyToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.delta.delta import Delta
from pydantic import Field


class AllChoicesResolver(AllChoicesResolverBase, BuildingBlock):
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

    type: Literal[BuildingBlockType.ALL_CHOICES_RESOLVER] = (
        BuildingBlockType.ALL_CHOICES_RESOLVER
    )

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

    def flatten(self) -> Generator[BuildingBlock]:
        for block in self.blocks:
            yield from block.flatten()

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[Delta, None, BlueprintProtocol]:
        current: BlueprintProtocol = state
        for block in self.flatten():
            current = yield from block.get_change(current)
        return current
