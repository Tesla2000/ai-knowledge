"""AI-powered holistic all choices resolver."""

from __future__ import annotations

from collections.abc import Generator
from itertools import filterfalse


from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.all_choices_resolver.base_resolver import (
    AllChoicesResolverBase,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.choice_package import (
    ChoicePackage,
)
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.building_block import CombinedBlock
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    AnyEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    AnyStatChoiceResolver,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasLanguages
from dnd.character.blueprint.state import HasNSkillChoices
from dnd.character.blueprint.state import HasNStatChoices
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasSkillsToChooseFrom
from dnd.character.blueprint.state import HasStats
from dnd.character.blueprint.state import HasStatsCup
from dnd.character.blueprint.state import HasToolProficiencies
from dnd.character.delta.ai_choices_resolution_delta import AIChoicesResolutionDelta
from dnd.character.feature.feats import FeatName
from dnd.choices.language import Language
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import Skill
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

    Example:
        >>> llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        >>> resolver = AIAllChoicesResolver(llm=llm)
        >>> builder = Builder().add(resolver)
    """

    blocks: tuple[
        AnyStatChoiceResolver,
        AnyEquipmentChooser,
        NullBlock | MaxIfNotMaxedResolver,
        AIAllNonStatChoicesResolver,
    ] = Field(
        description="Ordered building blocks: stat resolver, equipment chooser, optional feat resolver, and non-stat choices resolver",
    )


class AIAllNonStatChoicesResolver(
    BuildingBlock[BlueprintProtocol, AIChoicesResolutionDelta, BlueprintProtocol]
):
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
        state: BlueprintProtocol,
        n_languages_to_choose: int,
        n_skill_profs_to_choose: int,
        n_feats_to_choose: int,
        n_tools_to_choose: int,
    ) -> str:
        system_prompt = (
            "You are making ALL choices for a D&D 5e character in a single, "
            "holistic decision.\n"
            "Consider the character's class, race, background, and overall "
            "concept when making ALL selections.\n"
            "Your choices should be coherent and complementary across all "
            "categories.\n"
        )

        character_description = self.formatter.format(
            state, system_prompt=system_prompt
        )

        languages = state.languages if isinstance(state, HasLanguages) else ()
        skill_proficiencies = (
            state.skill_proficiencies
            if isinstance(state, HasSkillProficiencies)
            else ()
        )
        feats = state.feats if isinstance(state, HasFeats) else ()
        tool_proficiencies = (
            state.tool_proficiencies if isinstance(state, HasToolProficiencies) else ()
        )
        n_stat_choices = (
            state.n_stat_choices if isinstance(state, HasNStatChoices) else 0
        )
        n_skill_choices = (
            state.n_skill_choices if isinstance(state, HasNSkillChoices) else 0
        )
        skills_to_choose_from = (
            state.skills_to_choose_from
            if isinstance(state, HasSkillsToChooseFrom)
            else frozenset()
        )
        stats = state.stats if isinstance(state, HasStats) else None
        stats_cup = state.stats_cup if isinstance(state, HasStatsCup) else None
        classes = (
            dict(state.classes.all_levels()) if isinstance(state, HasClasses) else {}
        )

        instructions = ["\n## All Choices to Make\n"]
        has_choices = False

        if n_languages_to_choose > 0:
            has_choices = True
            already_known = {
                lang for lang in languages if lang != Language.ANY_OF_YOUR_CHOICE
            }
            available = [
                lang.value
                for lang in Language
                if lang not in already_known and lang != Language.ANY_OF_YOUR_CHOICE
            ]
            instructions.append(
                f"\n### Languages ({n_languages_to_choose} to select)\n"
                f"Select EXACTLY {n_languages_to_choose} language(s)\n"
                f"Available: {', '.join(available)}\n"
                f"Already known: {', '.join(lang.value for lang in already_known)}"
            )

        if n_skill_profs_to_choose > 0:
            has_choices = True
            already_known_skills = {
                s for s in skill_proficiencies if s != Skill.ANY_OF_YOUR_CHOICE
            }
            available_skills = [
                s.value
                for s in Skill
                if s not in already_known_skills and s != Skill.ANY_OF_YOUR_CHOICE
            ]
            instructions.append(
                f"\n### Skill Proficiencies ({n_skill_profs_to_choose} to select)\n"
                f"Select EXACTLY {n_skill_profs_to_choose} skill proficiency(ies)\n"
                f"Available: {', '.join(available_skills)}\n"
                f"Already known: {', '.join(s.value for s in already_known_skills)}"
            )

        if n_feats_to_choose > 0:
            has_choices = True
            ability_score_improvement_allowed = sum(classes.values()) != 1
            already_known_feats = {
                f for f in feats if f not in FeatName.not_choosables()
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

        if n_tools_to_choose > 0:
            has_choices = True
            not_choice = {
                ToolProficiency.ANY_OF_YOUR_CHOICE,
                GamingSet.ANY_OF_YOUR_CHOICE,
                MusicalInstrument.ANY_OF_YOUR_CHOICE,
            }
            already_known_tools = {t for t in tool_proficiencies if t not in not_choice}
            available_tools = (
                [
                    f"ToolProficiency.{t.value}"
                    for t in ToolProficiency
                    if t not in already_known_tools
                    and t != ToolProficiency.ANY_OF_YOUR_CHOICE
                ]
                + [
                    f"GamingSet.{g.value}"
                    for g in GamingSet
                    if g not in already_known_tools
                    and g != GamingSet.ANY_OF_YOUR_CHOICE
                ]
                + [
                    f"MusicalInstrument.{m.value}"
                    for m in MusicalInstrument
                    if m not in already_known_tools
                    and m != MusicalInstrument.ANY_OF_YOUR_CHOICE
                ]
            )
            instructions.append(
                f"\n### Tool Proficiencies ({n_tools_to_choose} to select)\n"
                f"Select EXACTLY {n_tools_to_choose} tool proficiency(ies)\n"
                f"Available: {', '.join(available_tools)}\n"
                f"Already known: {', '.join(str(t) for t in already_known_tools)}"
            )

        if n_stat_choices > 0:
            has_choices = True
            instructions.append(
                f"\n### Stat Increases ({n_stat_choices} points)\n"
                f"Distribute {n_stat_choices} stat increase points\n"
                f"Current stats: {stats}\n"
                f"Stat cap: {stats_cup}"
            )

        if n_skill_choices > 0:
            has_choices = True
            instructions.append(
                f"\n### Skill Selection ({n_skill_choices} to select)\n"
                f"Select {n_skill_choices} skill(s) from available pool\n"
                f"Available: {', '.join(s.value for s in skills_to_choose_from)}\n"
                f"Already have: {', '.join(s.value for s in skill_proficiencies)}"
            )

        if not has_choices:
            return ""

        instructions.append(
            "\n## Selection Guidelines\n"
            "1. Make ALL choices with a coherent character concept in mind\n"
            "2. Consider synergies between class, race, and background\n"
            "3. Choose complementary skills, feats, and stats\n"
            "4. Avoid duplicates (unless already present)\n"
            "5. Prioritize choices that enhance the character's role/concept"
        )

        return character_description + "\n".join(instructions)

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[AIChoicesResolutionDelta, None, BlueprintProtocol]:
        languages = state.languages if isinstance(state, HasLanguages) else ()
        skill_proficiencies = (
            state.skill_proficiencies
            if isinstance(state, HasSkillProficiencies)
            else ()
        )
        feats = state.feats if isinstance(state, HasFeats) else ()
        tool_proficiencies = (
            state.tool_proficiencies if isinstance(state, HasToolProficiencies) else ()
        )
        n_skill_choices = (
            state.n_skill_choices if isinstance(state, HasNSkillChoices) else 0
        )

        n_languages_to_choose = list(languages).count(Language.ANY_OF_YOUR_CHOICE)
        n_skill_profs_to_choose = list(skill_proficiencies).count(
            Skill.ANY_OF_YOUR_CHOICE
        )
        n_feats_to_choose = sum(map(list(feats).count, FeatName.not_choosables()))
        not_choice = {
            ToolProficiency.ANY_OF_YOUR_CHOICE,
            GamingSet.ANY_OF_YOUR_CHOICE,
            MusicalInstrument.ANY_OF_YOUR_CHOICE,
        }
        n_tools_to_choose = sum(1 for t in tool_proficiencies if t in not_choice)

        if not (
            n_tools_to_choose
            or n_languages_to_choose
            or n_feats_to_choose
            or n_skill_profs_to_choose
            or n_skill_choices
        ):
            delta = AIChoicesResolutionDelta(
                languages=tuple(
                    lang for lang in languages if lang != Language.ANY_OF_YOUR_CHOICE
                ),
                skill_proficiencies=tuple(
                    s for s in skill_proficiencies if s != Skill.ANY_OF_YOUR_CHOICE
                ),
                feats=tuple(f for f in feats if f not in FeatName.not_choosables()),
                tool_proficiencies=tuple(
                    t for t in tool_proficiencies if t not in not_choice
                ),
                n_skill_choices=0,
                skills_to_choose_from=frozenset(),
            )
            yield delta
            return delta.apply(state)

        prompt = self._build_prompt(
            state,
            n_languages_to_choose,
            n_skill_profs_to_choose,
            n_feats_to_choose,
            n_tools_to_choose,
        )

        structured_llm = self.llm.with_structured_output(ChoicePackage)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, ChoicePackage):
            raise TypeError(f"Expected ChoicePackage, got {type(_result)}")
        choices = _result

        new_languages = tuple(set(choices.languages))[:n_languages_to_choose]
        new_skill_profs = tuple(set(choices.skill_proficiencies))[
            :n_skill_profs_to_choose
        ]
        new_feats = tuple(set(choices.feats))[:n_feats_to_choose]
        new_tools = tuple(set(choices.tool_proficiencies))[:n_tools_to_choose]

        delta = AIChoicesResolutionDelta(
            languages=tuple(
                filterfalse(
                    Language.ANY_OF_YOUR_CHOICE.__eq__, languages + new_languages
                )
            ),
            skill_proficiencies=tuple(
                filterfalse(
                    Skill.ANY_OF_YOUR_CHOICE.__eq__,
                    skill_proficiencies + new_skill_profs,
                )
            ),
            feats=tuple(
                filterfalse(FeatName.not_choosables().__contains__, feats + new_feats)
            ),
            tool_proficiencies=tuple(
                prof
                for prof in (tool_proficiencies + new_tools)
                if prof not in not_choice
            ),
            n_skill_choices=0,
            skills_to_choose_from=frozenset(),
        )
        yield delta
        return delta.apply(state)
