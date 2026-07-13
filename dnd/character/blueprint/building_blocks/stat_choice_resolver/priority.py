from dnd.character.blueprint.building_blocks.stat_choice_resolver.base import (
    StatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.choices.stats_creation.statistic import Statistic
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import ConfigDict
from pydantic import Field


class PriorityStatChoiceResolver(StatChoiceResolver):
    """Resolves stat choices based on a priority order.

    Uses logic similar to ability score improvements: prioritizes making odd
    stats even (for better modifier bonuses) while respecting priority order.

    In D&D 5e, ability modifiers are calculated as (stat - 10) / 2 rounded down.
    This means increasing an odd stat to even provides a modifier improvement,
    while increasing an even stat by just 1 doesn't help. This resolver optimizes
    stat distribution by preferring odd stats when possible.

    Example:
        >>> resolver = PriorityStatChoiceResolver(
        ...     priority=(
        ...         Statistic.STRENGTH,
        ...         Statistic.CONSTITUTION,
        ...         Statistic.DEXTERITY,
        ...         Statistic.WISDOM,
        ...         Statistic.INTELLIGENCE,
        ...         Statistic.CHARISMA,
        ...     )
        ... )
    """

    type: Literal[BuildingBlockType.PRIORITY_STAT_CHOICE_RESOLVER] = (
        BuildingBlockType.PRIORITY_STAT_CHOICE_RESOLVER
    )

    model_config = ConfigDict(frozen=True)

    priority: StatsPriority = Field(
        description="Ability scores ranked by priority for stat increase allocation"
    )

    def select_stats_to_increase(self, state: _WideBlueprint) -> dict[Statistic, int]:
        """Select stats to increase based on priority order."""
        assert state.stats is not None
        stats = state.stats
        increases = {stat: 0 for stat in self.priority}
        stats_cup = state.stats_cup

        def _get_current_value(stat: Statistic) -> int:
            return stats.get_stat(stat) + increases[stat]

        def _get_stat_cap(stat: Statistic) -> int:
            return stats_cup.get_stat(stat)

        n_stats = state.n_stat_choices
        improvable_stats = tuple(
            stat
            for stat in self.priority
            if _get_current_value(stat) < _get_stat_cap(stat) // 2
        )
        for stat in improvable_stats:
            if not n_stats:
                return increases
            is_odd = _get_current_value(stat) % 2 == 1
            if is_odd:
                point_to_improve_by = 1 if _get_current_value(stat) % 2 == 1 else 2
                n_stats -= point_to_improve_by
                increases[stat] += point_to_improve_by
            while n_stats >= 2:
                point_to_improve_by = 2
                n_stats -= point_to_improve_by
                increases[stat] += point_to_improve_by
        for _ in range(n_stats):
            for stat in self.priority:
                if _get_current_value(stat) < _get_stat_cap(stat):
                    increases[stat] += 1
                    break
        return increases
