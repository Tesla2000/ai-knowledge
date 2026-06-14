from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.stat_choice_resolver.base import (
    StatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_priority import (
    StatsPriority,
)
from dnd.choices.stats_creation.statistic import Statistic
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
        >>> # Distributes points intelligently based on current stat values
        >>> # Prioritizes odd stats to maximize modifier improvements
    """

    model_config = ConfigDict(frozen=True)

    priority: StatsPriority = Field(
        description="Ability scores ranked by priority for stat increase allocation"
    )

    def select_stats_to_increase(self, blueprint: Blueprint) -> dict[Statistic, int]:
        """Select stats to increase based on priority order.

        Simple logic: for each point, add to odd stat if possible (in priority
        order), otherwise add to highest priority stat below cap.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Dictionary mapping statistics to their increases.
        """
        increases = {stat: 0 for stat in self.priority}

        def _get_current_value(stat: Statistic) -> int:
            """Get current value including already-applied increases."""
            return blueprint.stats.get_stat(stat) + increases[stat]

        def _get_stat_cap(stat: Statistic) -> int:
            """Get the cap for a stat."""
            return blueprint.stats_cup.get_stat(stat)

        n_stats = blueprint.n_stat_choices
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
