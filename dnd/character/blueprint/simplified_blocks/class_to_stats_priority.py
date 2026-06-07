from dnd.character.blueprint.building_blocks.stats_priority import (
    StatsPriority,
)
from dnd.choices.class_creation.character_class import Class
from dnd.choices.stats_creation.statistic import Statistic
from frozendict import frozendict
from pydantic import TypeAdapter

_stats_priority_validator = TypeAdapter(StatsPriority)
CLASS_TO_STATS_PRIORITY: frozendict[Class, StatsPriority] = frozendict(
    {
        Class.WIZARD: _stats_priority_validator.validate_python(
            (
                Statistic.INTELLIGENCE,
                Statistic.CONSTITUTION,
                Statistic.WISDOM,
                Statistic.DEXTERITY,
                Statistic.CHARISMA,
                Statistic.STRENGTH,
            )
        ),
        Class.SORCERER: _stats_priority_validator.validate_python(
            (
                Statistic.CHARISMA,
                Statistic.CONSTITUTION,
                Statistic.WISDOM,
                Statistic.DEXTERITY,
                Statistic.INTELLIGENCE,
                Statistic.STRENGTH,
            )
        ),
    }
)
