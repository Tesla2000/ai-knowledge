from typing import Annotated

from dnd.choices.stats_creation.statistic import Statistic
from pydantic import AfterValidator

_Stats = tuple[Statistic, Statistic, Statistic, Statistic, Statistic, Statistic]


def _validate_uniqueness(stats_priority: _Stats) -> _Stats:
    if len(stats_priority) != len(set(stats_priority)):
        raise ValueError(f"Elements of {stats_priority=} are not unique")
    return stats_priority


StatsPriority = Annotated[
    tuple[Statistic, Statistic, Statistic, Statistic, Statistic, Statistic],
    AfterValidator(_validate_uniqueness),
]
