from typing import Literal
from typing import ClassVar

from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.building_blocks.stats_builder.stats_builder import (
    StatsBuilder,
)
from dnd.character.stats import Stats
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.sentinels import (
    _RK,
    _HeK,
    _StCK,
    _SkCK,
    _WZK,
    _SOK,
    _FGK,
    _BAK,
    _ROK,
    _CLK,
    _DRK,
    _PAK,
    _RAK,
    _MOK,
    _BDK,
    _WAK,
    _ARK,
    _CDK,
)


class StandardArray(StatsBuilder):
    """Assigns ability scores using the standard array method (15, 14, 13, 12, 10, 8).

    Distributes the standard D&D 5e ability score array to the six ability scores
    based on the provided stats priority, assigning higher values to more important stats.

    Example:
        >>> stats_priority = StatsPriority((Statistic.STR, Statistic.CON, ...))
        >>> builder = StandardArray(stats_priority=stats_priority)
        >>> # Will assign 15 to STR, 14 to CON, etc.
    """

    type: Literal[BuildingBlockType.STANDARD_ARRAY] = BuildingBlockType.STANDARD_ARRAY

    _standard_array_descending: ClassVar[tuple[int, int, int, int, int, int]] = (
        15,
        14,
        13,
        12,
        10,
        8,
    )

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            None,
            _HeK,
            _StCK,
            _SkCK,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ],
    ) -> Blueprint[
        _RK,
        Stats,
        _HeK,
        _StCK,
        _SkCK,
        _WZK,
        _SOK,
        _FGK,
        _BAK,
        _ROK,
        _CLK,
        _DRK,
        _PAK,
        _RAK,
        _MOK,
        _BDK,
        _WAK,
        _ARK,
        _CDK,
    ]:
        stats = Stats.from_mapping(
            dict(zip(self.stats_priority, self._standard_array_descending))
        )
        return Blueprint[
            _RK,
            Stats,
            _HeK,
            _StCK,
            _SkCK,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ].model_validate(dict(blueprint) | {"stats": stats})
