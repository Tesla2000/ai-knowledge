from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.feat_choice_resolver.base import (
    FeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_priority import (
    StatsPriority,
)
from dnd.character.feature.feats import FeatName
from pydantic import Field


class _AlreadyMaxed(Exception):
    pass


class MaxIfNotMaxedResolver(FeatChoiceResolver):
    """Chooses Ability Score Improvement only if the highest priority stat is not maxed.

    If the highest priority stat is already at its cap, returns an empty blueprint
    instead of choosing a feat. Useful for builds that want ASI when possible but
    skip the feat choice entirely when not needed.

    Example:
        >>> resolver = MaxIfNotMaxedResolver(
        ...     priority=StatsPriority((Statistic.DEX, ...))
        ... )
        >>> # Chooses ASI if DEX < cap, otherwise returns empty blueprint
    """

    priority: StatsPriority = Field(
        description="Ability score priority order for determining which stat to check"
    )

    def select_from_available(
        self, available: list[FeatName], blueprint: Blueprint
    ) -> FeatName:
        highest_priority_stat = self.priority[0]
        if blueprint.stats.get_stat(  # type: ignore[union-attr]
            highest_priority_stat
        ) < blueprint.stats_cup.get_stat(highest_priority_stat):
            return FeatName.ABILITY_SCORE_IMPROVEMENT
        raise _AlreadyMaxed()

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Replace FeatName.ANY_OF_YOUR_CHOICE placeholders.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with feat placeholders replaced and ASI converted
            to n_stat_choices.
        """
        try:
            return super().get_change(blueprint)
        except _AlreadyMaxed:
            return Blueprint()
