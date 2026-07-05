from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

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


class SkillsDelta(Delta):
    """Delta produced when SkillChoiceResolver resolves skill choices."""

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


class SkillChoiceResolver[
    T: ProtocolIntersection[
        ProtocolIntersection[HasNSkillChoices, HasSkillsToChooseFrom],
        HasSkillProficiencies,
    ]
](BuildingBlock[T, SkillsDelta, HasSkillProficiencies], ABC):
    """Abstract base class for resolving n_skill_choices.

    When a race/class grants skill proficiencies of the player's choice
    (n_skill_choices > 0), this component determines which skills to select
    from the available skills_to_choose_from.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_skills(self, state: T) -> frozenset[Skill]: ...

    def get_change(
        self, state: T
    ) -> Generator[SkillsDelta, None, ProtocolIntersection[T, HasSkillProficiencies]]:
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
