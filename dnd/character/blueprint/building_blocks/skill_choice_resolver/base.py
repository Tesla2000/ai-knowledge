from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.skill_proficiency import Skill
from pydantic import ConfigDict


class SkillChoiceResolver(BuildingBlock, ABC):
    """Abstract base class for resolving n_skill_choices.

    When a race/class grants skill proficiencies of the player's choice
    (n_skill_choices > 0), this component determines which skills to select
    from the available skills_to_choose_from.

    Subclasses must implement _select_skills to determine the
    selection strategy.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_skills(self, blueprint: Blueprint) -> frozenset[Skill]:
        """Select skills from available options based on blueprint context.

        Args:
            blueprint: Current character blueprint containing:
                - n_skill_choices: Number of skills to select
                - skills_to_choose_from: Set of skills to choose from
                - Other character context for informed selection

        Returns:
            Frozenset of selected skills.
        """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Apply skill choices based on n_skill_choices."""
        if not blueprint.n_skill_choices and blueprint.skills_to_choose_from:
            raise ValueError(
                "Skills to choose from present but no skill choices available"
            )

        if blueprint.n_skill_choices == 0:
            return Blueprint()

        if not blueprint.skills_to_choose_from:
            raise ValueError(
                "skills_to_choose_from must not be empty when n_skill_choices > 0"
            )

        if (
            blueprint.n_skill_choices > len(blueprint.skills_to_choose_from)
            and Skill.ANY_OF_YOUR_CHOICE not in blueprint.skills_to_choose_from
        ):
            raise ValueError(
                f"Cannot choose {blueprint.n_skill_choices} skills from "
                f"{len(blueprint.skills_to_choose_from)} available skills"
            )

        # Select skills
        selected_skills = self._select_skills(blueprint)

        # Add to existing skill proficiencies
        new_skill_proficiencies = blueprint.skill_proficiencies + tuple(
            selected_skills
        )

        return Blueprint(
            skill_proficiencies=new_skill_proficiencies,
            n_skill_choices=0,
            skills_to_choose_from=frozenset(),
        )
