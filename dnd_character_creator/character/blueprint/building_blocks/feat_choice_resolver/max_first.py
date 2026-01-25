from typing import Union

from dnd_character_creator.character.blueprint.blueprint import Blueprint
from dnd_character_creator.character.blueprint.building_blocks.feat_choice_resolver.ai import (
    AIFeatChoiceResolver,
)
from dnd_character_creator.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd_character_creator.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd_character_creator.character.blueprint.building_blocks.stats_priority import (
    StatsPriority,
)
from dnd_character_creator.character.feature.feats import FeatName
from pydantic import Field


class MaxFirstResolver(FeatChoiceResolver):
    """Prioritizes maxing the highest priority stat before choosing other feats.

    Checks if the highest priority stat is below its cap and selects Ability Score
    Improvement if so. Otherwise, delegates to the fallback resolver (random or AI).

    Example:
        >>> resolver = MaxFirstResolver(
        ...     priority=StatsPriority((Statistic.STR, ...)),
        ...     then=RandomFeatChoiceResolver()
        ... )
        >>> # Will choose ASI if STR < cap, otherwise random feat
    """

    priority: StatsPriority = Field(
        description="Ability score priority order for determining which stat to max"
    )
    then: Union[RandomFeatChoiceResolver, AIFeatChoiceResolver] = Field(
        description="Fallback resolver to use when highest priority stat is already maxed"
    )

    def select_from_available(
        self, available: list[FeatName], blueprint: Blueprint
    ) -> FeatName:
        highest_priority_stat = self.priority[0]
        if blueprint.stats.get_stat(
            highest_priority_stat
        ) < blueprint.stats_cup.get_stat(highest_priority_stat):
            return FeatName.ABILITY_SCORE_IMPROVEMENT
        return self.then.select_from_available(available, blueprint)

    def _resolve_feat(self, feat: FeatName, blueprint: Blueprint):
        if feat not in FeatName.not_choosables():
            return feat
        available = [f for f in FeatName if f not in FeatName.not_choosables()]
        if feat == FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT:
            return self.then.select_from_available(available, blueprint)
        return self.select_from_available(available, blueprint)
