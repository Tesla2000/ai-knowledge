from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import overload
from typing import Protocol
from typing import runtime_checkable
from typing import TYPE_CHECKING

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasNSkillChoices
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasSkillsToChooseFrom
from dnd.character.delta.delta import Delta
from dnd.skill_proficiency import Skill
from pydantic import ConfigDict
from typing import Literal


class SkillsDelta(Delta):
    """Delta produced when SkillChoiceResolver resolves skill choices."""

    delta_type: Literal["SkillsDelta"] = "SkillsDelta"
    skill_proficiencies: tuple[Skill, ...]
    n_skill_choices: int
    skills_to_choose_from: frozenset[Skill]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasSkillProficiencies]:

        if TYPE_CHECKING:

            class BlueprintWithSkills(Blueprint):
                skill_proficiencies: tuple[Skill, ...]
                n_skill_choices: int
                skills_to_choose_from: frozenset[Skill]

        else:

            class BlueprintWithSkills(type(state)):
                skill_proficiencies: tuple[Skill, ...]
                n_skill_choices: int
                skills_to_choose_from: frozenset[Skill]

        return cast(
            ProtocolIntersection[T, HasSkillProficiencies],
            BlueprintWithSkills.model_validate(
                {
                    **dict(state),
                    "skill_proficiencies": self.skill_proficiencies,
                    "n_skill_choices": self.n_skill_choices,
                    "skills_to_choose_from": self.skills_to_choose_from,
                }
            ),
        )


@runtime_checkable
class _SkillT(HasNSkillChoices, HasSkillsToChooseFrom, HasSkillProficiencies, Protocol):
    pass


class SkillChoiceResolver(BuildingBlock, ABC):
    """Abstract base class for resolving n_skill_choices.

    When a race/class grants skill proficiencies of the player's choice
    (n_skill_choices > 0), this component determines which skills to select
    from the available skills_to_choose_from.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_skills(self, state: _SkillT) -> frozenset[Skill]: ...

    @overload
    def get_change[T: _SkillT](
        self, state: T
    ) -> Generator[
        SkillsDelta, None, ProtocolIntersection[T, HasSkillProficiencies]
    ]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasNSkillChoices, HasSkillsToChooseFrom and HasSkillProficiencies for precise return typing"
    )
    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, _SkillT):
            raise TypeError(
                f"{type(self).__name__} requires HasNSkillChoices, HasSkillsToChooseFrom and HasSkillProficiencies, got {type(state).__name__}"
            )
        if state.n_skill_choices == 0:
            delta = SkillsDelta(
                skill_proficiencies=state.skill_proficiencies,
                n_skill_choices=0,
                skills_to_choose_from=frozenset(),
            )
            yield delta
            return delta.apply(state)

        selected = self._select_skills(state)
        delta = SkillsDelta(
            skill_proficiencies=state.skill_proficiencies + tuple(selected),
            n_skill_choices=0,
            skills_to_choose_from=frozenset(),
        )
        yield delta
        return delta.apply(state)
