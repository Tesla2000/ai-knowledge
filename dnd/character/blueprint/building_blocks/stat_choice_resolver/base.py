from abc import ABC
from abc import abstractmethod
from typing import Literal

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.sentinels import (
    _RK,
    _StK,
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
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic
from pydantic import ConfigDict


class StatChoiceResolver(BuildingBlock, ABC):
    """Abstract base for resolving n_stat_choices.

    When a race/subrace grants ability score increases of the player's choice
    (n_stat_choices > 0), this component determines which stats to increase.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def select_stats_to_increase(
        self, state: _WideBlueprint
    ) -> dict[Statistic, int]: ...

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            _StK,
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
        _StK,
        _HeK,
        Literal[0],
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
        if blueprint.n_stat_choices == 0 or blueprint.stats is None:
            return Blueprint[
                _RK,
                _StK,
                _HeK,
                Literal[0],
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
            ].model_validate(dict(blueprint) | {"n_stat_choices": 0})

        stat_increases = self.select_stats_to_increase(blueprint)
        new_stats = Stats(
            strength=blueprint.stats.strength
            + stat_increases.get(Statistic.STRENGTH, 0),
            dexterity=blueprint.stats.dexterity
            + stat_increases.get(Statistic.DEXTERITY, 0),
            constitution=blueprint.stats.constitution
            + stat_increases.get(Statistic.CONSTITUTION, 0),
            intelligence=blueprint.stats.intelligence
            + stat_increases.get(Statistic.INTELLIGENCE, 0),
            wisdom=blueprint.stats.wisdom + stat_increases.get(Statistic.WISDOM, 0),
            charisma=blueprint.stats.charisma
            + stat_increases.get(Statistic.CHARISMA, 0),
        )
        return Blueprint[
            _RK,
            _StK,
            _HeK,
            Literal[0],
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
        ].model_validate(dict(blueprint) | {"stats": new_stats, "n_stat_choices": 0})
