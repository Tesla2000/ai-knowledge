from __future__ import annotations

import random

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.skill_choice_resolver.base import (
    SkillChoiceResolver,
)
from dnd.character.blueprint.state import HasNSkillChoices
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasSkillsToChooseFrom
from dnd.skill_proficiency import Skill
from pydantic import ConfigDict
from pydantic import Field


class RandomSkillChoiceResolver[
    T: ProtocolIntersection[
        ProtocolIntersection[HasNSkillChoices, HasSkillsToChooseFrom],
        HasSkillProficiencies,
    ]
](SkillChoiceResolver[T]):
    """Randomly selects skills from available options.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> resolver = RandomSkillChoiceResolver(seed=42)  # Reproducible
        >>> # or
        >>> resolver = RandomSkillChoiceResolver()  # Truly random
    """

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_skills(self, state: T) -> frozenset[Skill]:
        random.seed(self.seed)
        n = state.n_skill_choices
        available_skills = state.skills_to_choose_from

        if Skill.ANY_OF_YOUR_CHOICE in available_skills:
            available_seq = tuple(set(Skill).difference((Skill.ANY_OF_YOUR_CHOICE,)))
        else:
            available_seq = tuple(available_skills)
        selected = random.sample(available_seq, n)
        return frozenset(selected)
