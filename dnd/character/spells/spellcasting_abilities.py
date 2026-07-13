from dnd.choices.class_creation.character_class import (
    Class,
)
from dnd.choices.stats_creation.statistic import (
    Statistic,
)
from frozendict import frozendict

SPELLCASTING_ABILITY_MAP: frozendict[Class, Statistic] = frozendict(
    {
        Class.BARD: Statistic.CHARISMA,
        Class.CLERIC: Statistic.WISDOM,
        Class.DRUID: Statistic.WISDOM,
        Class.PALADIN: Statistic.CHARISMA,
        Class.RANGER: Statistic.WISDOM,
        Class.SORCERER: Statistic.CHARISMA,
        Class.WARLOCK: Statistic.CHARISMA,
        Class.WIZARD: Statistic.INTELLIGENCE,
        Class.ARTIFICER: Statistic.INTELLIGENCE,
    }
)
