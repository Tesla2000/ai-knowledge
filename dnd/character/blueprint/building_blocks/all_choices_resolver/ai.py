"""AI-powered holistic all choices resolver."""

from itertools import filterfalse
from typing import Literal

from dnd.character.blueprint.formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.all_choices_resolver.base_resolver import (
    AllChoicesResolverBase,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.choice_package import (
    ChoicePackage,
)
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
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
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.feature.feats import FeatName
from dnd.choices.language import Language
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import Skill
from pydantic import ConfigDict
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService
from dnd.character.blueprint.sentinels import (
    _RK,
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
from dnd.character.stats import Stats


class AIAllNonStatChoicesResolver(BuildingBlock):
    """AI-powered resolver for non-stat character choices."""

    type: Literal[BuildingBlockType.AI_ALL_NON_STAT_CHOICES_RESOLVER] = (
        BuildingBlockType.AI_ALL_NON_STAT_CHOICES_RESOLVER
    )
    model_config = ConfigDict(frozen=True)

    llm: RaisingService = Field(
        default_factory=lambda: RaisingService(service=OpenAIService()),
    )
    formatter: BlueprintFormatter = Field(default_factory=BlueprintFormatter)

    def _build_prompt(
        self,
        blueprint: _WideBlueprint,
        n_languages_to_choose: int,
        n_skill_profs_to_choose: int,
        n_feats_to_choose: int,
        n_tools_to_choose: int,
    ) -> str:
        system_prompt = (
            "You are making ALL choices for a D&D 5e character in a single, holistic decision.\n"
            "Consider the character's class, race, background, and overall concept when making ALL selections.\n"
        )
        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )
        instructions = ["\n## All Choices to Make\n"]
        has_choices = False

        if n_languages_to_choose > 0:
            has_choices = True
            already_known = {
                lang
                for lang in blueprint.languages
                if lang != Language.ANY_OF_YOUR_CHOICE
            }
            available = [
                lang.value
                for lang in Language
                if lang not in already_known and lang != Language.ANY_OF_YOUR_CHOICE
            ]
            instructions.append(
                f"\n### Languages ({n_languages_to_choose} to select)\n"
                f"Available: {', '.join(available)}"
            )

        if n_skill_profs_to_choose > 0:
            has_choices = True
            already_known_skills = {
                s
                for s in blueprint.skill_proficiencies
                if s != Skill.ANY_OF_YOUR_CHOICE
            }
            available_skills = [
                s.value
                for s in Skill
                if s not in already_known_skills and s != Skill.ANY_OF_YOUR_CHOICE
            ]
            instructions.append(
                f"\n### Skill Proficiencies ({n_skill_profs_to_choose} to select)\n"
                f"Available: {', '.join(available_skills)}"
            )

        if n_feats_to_choose > 0:
            has_choices = True
            classes = dict(blueprint.classes.all_levels())
            ability_score_improvement_allowed = sum(classes.values()) != 1
            available_feats = [
                f.value
                for f in FeatName
                if f not in FeatName.not_choosables()
                and (
                    ability_score_improvement_allowed
                    or f != FeatName.ABILITY_SCORE_IMPROVEMENT
                )
            ]
            instructions.append(
                f"\n### Feats ({n_feats_to_choose} to select)\nAvailable: {', '.join(available_feats)}"
            )

        if n_tools_to_choose > 0:
            has_choices = True
            instructions.append(
                f"\n### Tool Proficiencies ({n_tools_to_choose} to select)"
            )

        if not has_choices:
            return ""
        return character_description + "\n".join(instructions)

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            Stats,
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
        Stats,
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
        languages = blueprint.languages
        skill_proficiencies = blueprint.skill_proficiencies
        feats = blueprint.feats
        tool_proficiencies = blueprint.tool_proficiencies
        n_skill_choices = blueprint.n_skill_choices

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
            return Blueprint[
                _RK,
                Stats,
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
                    "languages": tuple(
                        lang
                        for lang in languages
                        if lang != Language.ANY_OF_YOUR_CHOICE
                    ),
                    "skill_proficiencies": tuple(
                        s for s in skill_proficiencies if s != Skill.ANY_OF_YOUR_CHOICE
                    ),
                    "feats": tuple(
                        f for f in feats if f not in FeatName.not_choosables()
                    ),
                    "tool_proficiencies": tuple(
                        t for t in tool_proficiencies if t not in not_choice
                    ),
                    "n_skill_choices": 0,
                    "skills_to_choose_from": frozenset(),
                }
            )

        prompt = self._build_prompt(
            blueprint,
            n_languages_to_choose,
            n_skill_profs_to_choose,
            n_feats_to_choose,
            n_tools_to_choose,
        )
        choices = self.llm.create_structured_output(prompt, ChoicePackage)

        new_languages = tuple(set(choices.languages))[:n_languages_to_choose]
        new_skill_profs = tuple(set(choices.skill_proficiencies))[
            :n_skill_profs_to_choose
        ]
        new_feats = tuple(set(choices.feats))[:n_feats_to_choose]
        new_tools = tuple(set(choices.tool_proficiencies))[:n_tools_to_choose]

        return Blueprint[
            _RK,
            Stats,
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
                "languages": tuple(
                    filterfalse(
                        Language.ANY_OF_YOUR_CHOICE.__eq__, languages + new_languages
                    )
                ),
                "skill_proficiencies": tuple(
                    filterfalse(
                        Skill.ANY_OF_YOUR_CHOICE.__eq__,
                        skill_proficiencies + new_skill_profs,
                    )
                ),
                "feats": tuple(
                    filterfalse(
                        FeatName.not_choosables().__contains__, feats + new_feats
                    )
                ),
                "tool_proficiencies": tuple(
                    prof
                    for prof in (tool_proficiencies + new_tools)
                    if prof not in not_choice
                ),
                "n_skill_choices": 0,
                "skills_to_choose_from": frozenset(),
            }
        )


class AIAllChoicesResolver(AllChoicesResolverBase, BuildingBlock):
    """AI-powered resolver that makes all character choices holistically."""

    type: Literal[BuildingBlockType.AI_ALL_CHOICES_RESOLVER] = (
        BuildingBlockType.AI_ALL_CHOICES_RESOLVER
    )

    stat_choice_resolver: AnyStatChoiceResolver
    equipment_chooser: AnyEquipmentChooser
    feat_choice_resolver: NullBlock | MaxIfNotMaxedResolver
    all_non_stat_choices_resolver: AIAllNonStatChoicesResolver

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            Stats,
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
        Stats,
        _HeK,
        Literal[0],
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
        r1 = self.stat_choice_resolver.apply(blueprint)
        r2 = self.equipment_chooser.apply(r1)
        r3 = self.feat_choice_resolver.apply(r2)
        return self.all_non_stat_choices_resolver.apply(r3)
