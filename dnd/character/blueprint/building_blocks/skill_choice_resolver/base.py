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
from dnd.skill_proficiency import Skill
from pydantic import ConfigDict


class SkillChoiceResolver(BuildingBlock, ABC):
    """Abstract base class for resolving n_skill_choices.

    When a race/class grants skill proficiencies of the player's choice
    (n_skill_choices > 0), this component determines which skills to select
    from the available skills_to_choose_from.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_skills(self, state: _WideBlueprint) -> frozenset[Skill]: ...

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
        _StCK,
        Literal[0],
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
        if blueprint.n_skill_choices == 0:
            selected: frozenset[Skill] = frozenset()
        else:
            selected = self._select_skills(blueprint)

        return Blueprint[
            _RK,
            _StK,
            _HeK,
            _StCK,
            Literal[0],
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
        ].model_validate(
            dict(blueprint)
            | {
                "skill_proficiencies": blueprint.skill_proficiencies + tuple(selected),
                "n_skill_choices": 0,
                "skills_to_choose_from": frozenset(),
            }
        )
