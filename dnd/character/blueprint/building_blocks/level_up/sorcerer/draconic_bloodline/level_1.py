from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.base import (
    SorcererLevel1Base,
)
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import SorcererSubclass
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    AnySkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from pydantic import Field

from dnd.character._ability_name import AbilityName


class SorcererLevel1DraconicBloodline(
    SorcererLevel1Base[Literal[SorcererSubclass.DRACONIC_BLOODLINE]]
):
    """Increments sorcerer to level 1 and assigns Draconic Bloodline origin."""

    type: Literal[BuildingBlockType.SORCERER_LEVEL_1_DRACONIC_BLOODLINE] = (
        BuildingBlockType.SORCERER_LEVEL_1_DRACONIC_BLOODLINE
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        is_first_class = blueprint.classes.total_level() == 0
        update: dict[str, object] = {
            "classes": blueprint.classes.model_copy(update={"sorcerer": 1}),
            "weapon_proficiencies": blueprint.weapon_proficiencies
            | frozenset(
                {
                    WeaponProficiency.DAGGER,
                    WeaponProficiency.DART,
                    WeaponProficiency.SLING,
                    WeaponProficiency.QUARTERSTAFF,
                    WeaponProficiency.LIGHT_CROSSBOW,
                }
            ),
            "actions": blueprint.actions
            + (AbilityName.DRAGON_ANCESTOR, AbilityName.DRACONIC_RESILIENCE),
        }
        if is_first_class:
            update["n_skill_choices"] = blueprint.n_skill_choices + 2
            update["skills_to_choose_from"] = frozenset(
                {
                    Skill.ARCANA,
                    Skill.DECEPTION,
                    Skill.INSIGHT,
                    Skill.INTIMIDATION,
                    Skill.PERSUASION,
                    Skill.RELIGION,
                }
            )
            update["saving_throw_proficiencies"] = (
                blueprint.saving_throw_proficiencies
                + (Statistic.CHARISMA, Statistic.CONSTITUTION)
            )
            update["equipment_choices"] = blueprint.equipment_choices + (
                (WeaponName.CROSSBOW_LIGHT, WeaponName.DAGGER),
                ("component pouch", "arcane focus"),
                ("dungeoneer's pack", "explorer's pack"),
            )
            update["other_equipment"] = blueprint.other_equipment + (
                WeaponName.DAGGER,
                WeaponName.DAGGER,
            )
        result = blueprint.model_copy(update=update)
        return self.skill_choice_resolver.apply(result) if is_first_class else result
