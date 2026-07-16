"""AI-powered skill choice resolver for intelligent skill selection."""

from dnd.character.blueprint.building_blocks.skill_choice_resolver.base import (
    SkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.skill_proficiency import Skill
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import BaseModel
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService


class AISkillChoiceResolver(SkillChoiceResolver):
    """AI-powered skill choice resolver that selects skills based on character context."""

    type: Literal[BuildingBlockType.AI_SKILL_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_SKILL_CHOICE_RESOLVER
    )

    llm: RaisingService[BaseModel] = Field(
        exclude=True,
        default_factory=lambda: RaisingService(service=OpenAIService()),
        description="Language model for making AI-powered decisions",
    )

    def _build_prompt(self, state: _WideBlueprint) -> str:
        n = state.n_skill_choices
        available_skills = state.skills_to_choose_from

        parts = [
            f"You are selecting {n} skill proficiencies for a D&D 5e character.",
            "Choose skills that best fit the character's class, background, "
            "ability scores, and overall concept.",
        ]

        parts.append("\n## Available Skills")
        parts.append(f"Select exactly {n} skills from the following options:\n")

        actual_skills = [
            skill for skill in available_skills if skill != Skill.ANY_OF_YOUR_CHOICE
        ]

        for skill in sorted(actual_skills, key=lambda s: s.value):
            parts.append(f"  - {skill.value}")

        parts.append("\n## Selection Instructions")
        parts.append(f"Return exactly {n} skills from the available options above.")
        parts.append(
            "Consider:"
            "\n  - Which skills complement the character's primary ability scores"
            "\n  - Which skills fit the character's class and background"
            "\n  - Which skills support the character's role in a party"
            "\n  - The character's backstory and personality"
        )

        return "\n".join(parts)

    def _select_skills(self, state: _WideBlueprint) -> frozenset[Skill]:
        prompt = self._build_prompt(state)
        n = state.n_skill_choices

        class SkillSelection(BaseModel):
            selected_skills: list[Skill] = Field(min_length=n, max_length=n)

        selection = self.llm.create_structured_output(prompt, SkillSelection)

        actual_available = frozenset(
            skill
            for skill in state.skills_to_choose_from
            if skill != Skill.ANY_OF_YOUR_CHOICE
        )

        for skill in selection.selected_skills:
            if skill not in actual_available:
                raise ValueError(
                    f"AI selected {skill.value} which is not in available skills"
                )

        return frozenset(selection.selected_skills)
