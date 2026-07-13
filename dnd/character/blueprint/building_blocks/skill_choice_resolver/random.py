import random


from dnd.character.blueprint.building_blocks.skill_choice_resolver.base import (
    SkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.skill_proficiency import Skill
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import ConfigDict
from pydantic import Field


class RandomSkillChoiceResolver(SkillChoiceResolver):
    """Randomly selects skills from available options.

    Provides deterministic randomness when seed is set, useful for
    reproducible character generation.

    Example:
        >>> resolver = RandomSkillChoiceResolver(seed=42)  # Reproducible
        >>> # or
        >>> resolver = RandomSkillChoiceResolver()  # Truly random
    """

    type: Literal[BuildingBlockType.RANDOM_SKILL_CHOICE_RESOLVER] = (
        BuildingBlockType.RANDOM_SKILL_CHOICE_RESOLVER
    )

    model_config = ConfigDict(frozen=True)

    seed: int | None = Field(
        default=None,
        description="Optional seed for reproducible random selection",
    )

    def _select_skills(self, state: _WideBlueprint) -> frozenset[Skill]:
        random.seed(self.seed)
        n = state.n_skill_choices
        available_skills = state.skills_to_choose_from

        if Skill.ANY_OF_YOUR_CHOICE in available_skills:
            available_seq = tuple(set(Skill).difference((Skill.ANY_OF_YOUR_CHOICE,)))
        else:
            available_seq = tuple(available_skills)
        selected = random.sample(available_seq, n)
        return frozenset(selected)
