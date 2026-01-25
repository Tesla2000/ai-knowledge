"""AI-powered holistic all choices resolver."""

from __future__ import annotations

from itertools import filterfalse
from typing import Union

from dnd_character_creator.character.blueprint.blueprint import Blueprint
from dnd_character_creator.character.blueprint.blueprint_formatter import (
    BlueprintFormatter,
)
from dnd_character_creator.character.blueprint.building_blocks.all_choices_resolver.base_resolver import (
    AllChoicesResolverBase,
)
from dnd_character_creator.character.blueprint.building_blocks.all_choices_resolver.choice_package import (
    ChoicePackage,
)
from dnd_character_creator.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd_character_creator.character.blueprint.building_blocks.building_block import (
    CombinedBlock,
)
from dnd_character_creator.character.blueprint.building_blocks.equipment_chooser import (
    AnyEquipmentChooser,
)
from dnd_character_creator.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd_character_creator.character.blueprint.building_blocks.null_block import (
    NullBlock,
)
from dnd_character_creator.character.blueprint.building_blocks.stat_choice_resolver import (
    AnyStatChoiceResolver,
)
from dnd_character_creator.character.feature.feats import FeatName
from dnd_character_creator.choices.language import Language
from dnd_character_creator.other_profficiencies import GamingSet
from dnd_character_creator.other_profficiencies import MusicalInstrument
from dnd_character_creator.other_profficiencies import ToolProficiency
from dnd_character_creator.skill_proficiency import Skill
from langchain_openai import ChatOpenAI
from pydantic import ConfigDict
from pydantic import Field


class AIAllChoicesResolver(AllChoicesResolverBase, CombinedBlock):
    """AI-powered resolver that makes all character choices holistically.

    Unlike the standard AllChoicesResolver which chains individual resolvers,
    this resolver uses a single LLM call to make all choices simultaneously.
    This allows the AI to consider the full character concept and make
    coherent, interconnected decisions across all choice types.

    Resolves:
    - Language ANY_OF_YOUR_CHOICE placeholders
    - Skill proficiency ANY_OF_YOUR_CHOICE placeholders
    - Feat ANY_OF_YOUR_CHOICE placeholders
    - Tool proficiency ANY_OF_YOUR_CHOICE placeholders
    - Stat choices (n_stat_choices distribution)
    - Skill choices (n_skill_choices from available pool)

    Note: Initial data (name, backstory) and equipment choices should be
    handled separately before or after this resolver.

    Example:
        >>> llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        >>> resolver = AIAllChoicesResolver(llm=llm)
        >>> builder = Builder().add(resolver)
    """

    blocks: tuple[
        AnyStatChoiceResolver,
        AnyEquipmentChooser,
        Union[NullBlock, MaxIfNotMaxedResolver],
        AIAllNonStatChoicesResolver,
    ] = Field(
        description="Ordered building blocks: stat resolver, equipment chooser, optional feat resolver, and non-stat choices resolver",
    )


class AIAllNonStatChoicesResolver(BuildingBlock):
    """AI-powered resolver for non-stat character choices (languages, skills, feats, tools).

    Handles all non-stat character choices in a single AI call, making coherent
    decisions across languages, skill proficiencies, feats, and tool proficiencies.
    Used internally by AIAllChoicesResolver after stat choices are handled separately.

    Example:
        >>> llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        >>> resolver = AIAllNonStatChoicesResolver(llm=llm)
    """

    model_config = ConfigDict(frozen=True)

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_prompt(
        self,
        blueprint: Blueprint,
        n_languages_to_choose: int,
        n_skill_profs_to_choose: int,
        n_feats_to_choose: int,
        n_tools_to_choose: int,
    ) -> str:
        """Build comprehensive prompt for all choice resolution.

        Args:
            blueprint: Current character blueprint.
            n_languages_to_choose: Number of languages to select.
            n_skill_profs_to_choose: Number of skill proficiencies to select.
            n_feats_to_choose: Number of feats to select.
            n_tools_to_choose: Number of tool proficiencies to select.

        Returns:
            Formatted prompt string.
        """
        system_prompt = (
            "You are making ALL choices for a D&D 5e character in a single, "
            "holistic decision.\n"
            "Consider the character's class, race, background, and overall "
            "concept when making ALL selections.\n"
            "Your choices should be coherent and complementary across all "
            "categories.\n"
        )

        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )

        instructions = ["\n## All Choices to Make\n"]

        # Track if there are any choices to make
        has_choices = False

        # Language choices
        if n_languages_to_choose > 0:
            has_choices = True
            already_known_languages = {
                lang
                for lang in blueprint.languages
                if lang != Language.ANY_OF_YOUR_CHOICE
            }
            available_languages = [
                lang.value
                for lang in Language
                if lang not in already_known_languages
                and lang != Language.ANY_OF_YOUR_CHOICE
            ]
            instructions.append(
                f"\n### Languages ({n_languages_to_choose} to select)\n"
                f"Select EXACTLY {n_languages_to_choose} language(s)\n"
                f"Available: {', '.join(available_languages)}\n"
                f"Already known: {', '.join(lang.value for lang in already_known_languages)}"
            )

        # Skill proficiency choices
        if n_skill_profs_to_choose > 0:
            has_choices = True
            already_known_skills = {
                skill
                for skill in blueprint.skill_proficiencies
                if skill != Skill.ANY_OF_YOUR_CHOICE
            }
            available_skills = [
                skill.value
                for skill in Skill
                if skill not in already_known_skills
                and skill != Skill.ANY_OF_YOUR_CHOICE
            ]
            instructions.append(
                f"\n### Skill Proficiencies ({n_skill_profs_to_choose} to select)\n"
                f"Select EXACTLY {n_skill_profs_to_choose} skill proficiency(ies)\n"
                f"Available: {', '.join(available_skills)}\n"
                f"Already known: {', '.join(skill.value for skill in already_known_skills)}"
            )

        # Feat choices
        if n_feats_to_choose > 0:
            has_choices = True
            ability_score_improvement_allowed = (
                sum(blueprint.classes.values()) != 1
            )
            already_known_feats = {
                feat
                for feat in blueprint.feats
                if feat not in FeatName.not_choosables()
            }
            available_feats = [
                f.value
                for f in FeatName
                if f not in already_known_feats
                and f not in FeatName.not_choosables()
                and (
                    f not in FeatName.not_choosables()
                    or ability_score_improvement_allowed
                )
            ]
            instructions.append(
                f"\n### Feats ({n_feats_to_choose} to select)\n"
                f"Select EXACTLY {n_feats_to_choose} feat(s)\n"
                f"Available: {', '.join(available_feats)}\n"
                f"Already known: {', '.join(f.value for f in already_known_feats)}"
            )
            if not ability_score_improvement_allowed:
                instructions.append(
                    "\nNote: ABILITY_SCORE_IMPROVEMENT not available at level 1"
                )

        # Tool proficiency choices
        if n_tools_to_choose > 0:
            has_choices = True
            already_known_tools = {
                tool
                for tool in blueprint.tool_proficiencies
                if not (
                    (
                        isinstance(tool, ToolProficiency)
                        and tool == ToolProficiency.ANY_OF_YOUR_CHOICE
                    )
                    or (
                        isinstance(tool, GamingSet)
                        and tool == GamingSet.ANY_OF_YOUR_CHOICE
                    )
                    or (
                        isinstance(tool, MusicalInstrument)
                        and tool == MusicalInstrument.ANY_OF_YOUR_CHOICE
                    )
                )
            }
            available_tools = []
            for tool in ToolProficiency:
                if (
                    tool not in already_known_tools
                    and tool != ToolProficiency.ANY_OF_YOUR_CHOICE
                ):
                    available_tools.append(f"ToolProficiency.{tool.value}")
            for gaming in GamingSet:
                if (
                    gaming not in already_known_tools
                    and gaming != GamingSet.ANY_OF_YOUR_CHOICE
                ):
                    available_tools.append(f"GamingSet.{gaming.value}")
            for instrument in MusicalInstrument:
                if (
                    instrument not in already_known_tools
                    and instrument != MusicalInstrument.ANY_OF_YOUR_CHOICE
                ):
                    available_tools.append(
                        f"MusicalInstrument.{instrument.value}"
                    )

            instructions.append(
                f"\n### Tool Proficiencies ({n_tools_to_choose} to select)\n"
                f"Select EXACTLY {n_tools_to_choose} tool proficiency(ies)\n"
                f"Available: {', '.join(available_tools)}\n"
                f"Already known: {', '.join(str(t) for t in already_known_tools)}"
            )

        # Stat choices
        if blueprint.n_stat_choices > 0:
            has_choices = True
            instructions.append(
                f"\n### Stat Increases ({blueprint.n_stat_choices} points)\n"
                f"Distribute {blueprint.n_stat_choices} stat increase "
                f"points\n"
                f"Current stats: {blueprint.stats}\n"
                f"Stat cap: {blueprint.stats_cup}"
            )

        # Skill selection from pool
        if blueprint.n_skill_choices > 0:
            has_choices = True
            instructions.append(
                f"\n### Skill Selection ({blueprint.n_skill_choices} to select)\n"
                f"Select {blueprint.n_skill_choices} skill(s) from "
                f"available pool\n"
                f"Available: {', '.join(s.value for s in blueprint.skills_to_choose_from)}\n"
                f"Already have: {', '.join(s.value for s in blueprint.skill_proficiencies)}"
            )

        if not has_choices:
            return ""  # No choices to make

        instructions.append(
            "\n## Selection Guidelines\n"
            "1. Make ALL choices with a coherent character concept in mind\n"
            "2. Consider synergies between class, race, and background\n"
            "3. Choose complementary skills, feats, and stats\n"
            "4. Avoid duplicates (unless already present)\n"
            "5. Prioritize choices that enhance the character's role/concept"
        )

        return character_description + "\n".join(instructions)

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Make all character choices using AI in a single call.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with all choices resolved.
        """
        # Build prompt
        n_languages_to_choose = list(blueprint.languages).count(
            Language.ANY_OF_YOUR_CHOICE
        )
        n_skill_profs_to_choose = list(blueprint.skill_proficiencies).count(
            Skill.ANY_OF_YOUR_CHOICE
        )
        n_feats_to_choose = sum(
            map(list(blueprint.feats).count, FeatName.not_choosables())
        )
        n_tools_to_choose = sum(
            1
            for t in blueprint.tool_proficiencies
            if (
                (
                    isinstance(t, ToolProficiency)
                    and t == ToolProficiency.ANY_OF_YOUR_CHOICE
                )
                or (
                    isinstance(t, GamingSet)
                    and t == GamingSet.ANY_OF_YOUR_CHOICE
                )
                or (
                    isinstance(t, MusicalInstrument)
                    and t == MusicalInstrument.ANY_OF_YOUR_CHOICE
                )
            )
        )
        if not (
            n_tools_to_choose
            or n_languages_to_choose
            or n_feats_to_choose
            or n_skill_profs_to_choose
            or blueprint.n_skill_choices
        ):
            return Blueprint()  # No choices to make
        prompt = self._build_prompt(
            blueprint,
            n_languages_to_choose,
            n_skill_profs_to_choose,
            n_feats_to_choose,
            n_tools_to_choose,
        )

        # Get AI selections
        structured_llm = self.llm.with_structured_output(ChoicePackage)

        choices: ChoicePackage = structured_llm.invoke(prompt)

        # Apply language choices
        new_languages = tuple(set(choices.languages))[:n_languages_to_choose]

        # Apply skill proficiency choices
        new_skill_profs = tuple(set(choices.skill_proficiencies))[
            :n_skill_profs_to_choose
        ]

        # Apply feat choices and convert ASI
        new_feats = tuple(set(choices.feats))[:n_feats_to_choose]

        # Apply tool proficiency choices
        new_tools = tuple(set(choices.tool_proficiencies))[:n_tools_to_choose]

        return Blueprint(
            languages=set(
                filterfalse(
                    Language.ANY_OF_YOUR_CHOICE.__eq__,
                    blueprint.languages + new_languages,
                )
            ),
            skill_proficiencies=set(
                filterfalse(
                    Skill.ANY_OF_YOUR_CHOICE.__eq__,
                    blueprint.skill_proficiencies + new_skill_profs,
                )
            ),
            feats=set(
                filterfalse(
                    FeatName.not_choosables().__contains__,
                    blueprint.feats + new_feats,
                )
            ),
            tool_proficiencies=set(
                prof
                for prof in (blueprint.tool_proficiencies + new_tools)
                if prof
                in (
                    ToolProficiency.ANY_OF_YOUR_CHOICE,
                    GamingSet.ANY_OF_YOUR_CHOICE,
                    MusicalInstrument.ANY_OF_YOUR_CHOICE,
                )
            ),
            n_skill_choices=0,  # All skill choices consumed
            skills_to_choose_from=frozenset(),
        )
