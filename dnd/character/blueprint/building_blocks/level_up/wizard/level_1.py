from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.base import (
    WizardUpgradeLevelBase,
)
from dnd.character.blueprint.sentinels import SecondSubclassPreLevel
from dnd.character.blueprint.sentinels import WizardPreSubclassLevel
from dnd.character.blueprint.states.state import _BPT
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


class WizardLevel1(
    WizardUpgradeLevelBase[
        WizardPreSubclassLevel[Literal[SecondSubclassPreLevel.FIRST], None],
    ]
):
    """Increments wizard to level 1 and grants first-level proficiencies and choices."""

    type: Literal[BuildingBlockType.WIZARD_LEVEL_1] = BuildingBlockType.WIZARD_LEVEL_1
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        is_first_class = blueprint.classes.total_level() == 0
        update: dict[str, object] = {
            "classes": blueprint.classes.model_copy(update={"wizard": 1}),
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
            "actions": blueprint.actions + (AbilityName.ARCANE_RECOVERY,),
        }
        if is_first_class:
            update["n_skill_choices"] = blueprint.n_skill_choices + 2
            update["skills_to_choose_from"] = frozenset(
                {
                    Skill.ARCANA,
                    Skill.HISTORY,
                    Skill.INSIGHT,
                    Skill.INVESTIGATION,
                    Skill.MEDICINE,
                    Skill.RELIGION,
                }
            )
            update["saving_throw_proficiencies"] = (
                blueprint.saving_throw_proficiencies
                + (Statistic.INTELLIGENCE, Statistic.WISDOM)
            )
            update["equipment_choices"] = blueprint.equipment_choices + (
                (WeaponName.QUARTERSTAFF, WeaponName.DAGGER),
                ("component pouch", "arcane focus"),
                ("scholar's pack", "explorer's pack"),
            )
            update["other_equipment"] = blueprint.other_equipment + ("spellbook",)
        result = blueprint.model_copy(update=update)
        return self.skill_choice_resolver.apply(result) if is_first_class else result
