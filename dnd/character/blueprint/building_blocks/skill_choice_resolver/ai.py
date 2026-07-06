"""AI-powered skill choice resolver for intelligent skill selection."""

from __future__ import annotations


from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.skill_choice_resolver.base import (
    SkillChoiceResolver,
    _SkillT,
)
from dnd.skill_proficiency import Skill
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import BaseModel
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService


class SkillSelection(BaseModel):
    """Schema for AI to select skills."""

    selected_skills: tuple[Skill, ...] = Field(
        description="Selected skill proficiencies"
    )


class AISkillChoiceResolver(SkillChoiceResolver):
    """AI-powered skill choice resolver that selects skills based on character context.

    Uses an LLM to make intelligent skill selections based on the character's
    class, background, stats, and overall concept. The AI considers which skills
    best fit the character's role and abilities.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> resolver = AISkillChoiceResolver(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
        >>> builder = Builder().add(resolver)
    """

    type: Literal[BuildingBlockType.AI_SKILL_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_SKILL_CHOICE_RESOLVER
    )

    llm: RaisingService = Field(
        default_factory=lambda: RaisingService(service=OpenAIService()),
        description="Language model for making AI-powered decisions",
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_prompt(self, state: _SkillT) -> str:
        n = state.n_skill_choices
        available_skills = state.skills_to_choose_from

        parts = [
            f"You are selecting {n} skill proficiencies for a D&D 5e character.",
            "Choose skills that best fit the character's class, background, "
            "ability scores, and overall concept.",
        ]

        character_description = self.formatter.format(state)
        if character_description:
            parts.append(character_description)

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

    def _select_skills(self, state: _SkillT) -> frozenset[Skill]:
        prompt = self._build_prompt(state)

        selection = self.llm.create_structured_output(prompt, SkillSelection)

        if len(selection.selected_skills) != state.n_skill_choices:
            raise ValueError(
                f"AI returned {len(selection.selected_skills)} skills "
                f"but expected {state.n_skill_choices}"
            )

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
