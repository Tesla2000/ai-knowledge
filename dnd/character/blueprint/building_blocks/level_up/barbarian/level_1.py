from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.level_up.barbarian.base import (
    BarbarianUpgradeLevelBase,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    AnySkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from dnd.character.ac_modifier import BarbarianUnarmoredDefenseAcModifier
from dnd.character.blueprint.sentinels import ClassPreSubclassLevel
from dnd.character.blueprint.sentinels import ThirdSubclassPreLevel
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.abilities.action import BasicAction
from dnd.choices.abilities.action_type import ActionType
from dnd.character.actions._ability_name import AbilityName
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import ArmorProficiency
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill


class BarbarianLevel1(
    BarbarianUpgradeLevelBase[
        ClassPreSubclassLevel[Literal[ThirdSubclassPreLevel.ZEROTH], None],
        ClassPreSubclassLevel[Literal[ThirdSubclassPreLevel.FIRST], None],
    ]
):
    """Increments barbarian to level 1 and grants first-level proficiencies and choices."""

    type: Literal[BuildingBlockType.BARBARIAN_LEVEL_1] = (
        BuildingBlockType.BARBARIAN_LEVEL_1
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )

    def _update_blueprint(self, blueprint: _BPT) -> _BPT:
        is_first_class = blueprint.classes.total_level() == 0
        update: dict[str, object] = {
            "classes": blueprint.classes.model_copy(update={"barbarian": 1}),
            "armor_proficiencies": blueprint.armor_proficiencies
            | frozenset(
                {
                    ArmorProficiency.LIGHT_ARMOR,
                    ArmorProficiency.MEDIUM_ARMOR,
                    ArmorProficiency.SHIELDS,
                }
            ),
            "weapon_proficiencies": blueprint.weapon_proficiencies
            | frozenset(
                {
                    WeaponProficiency.SIMPLE_WEAPON,
                    WeaponProficiency.MARTIAL_WEAPON,
                }
            ),
            "ac_modifiers": blueprint.ac_modifiers
            + (BarbarianUnarmoredDefenseAcModifier(),),
            "actions": blueprint.actions
            + (
                BasicAction(
                    action_type=ActionType.BONUS_ACTION,
                    name=AbilityName.RAGE,
                    range_tails=0,
                    description=(
                        "You can enter a rage as a bonus action. While raging, you gain "
                        "advantage on Strength checks and saving throws, a bonus to melee "
                        "damage rolls using Strength (starting at +2), and resistance to "
                        "bludgeoning, piercing, and slashing damage. Your rage lasts for "
                        "1 minute. You have a limited number of rages per long rest."
                    ),
                ),
                BasicAction(
                    action_type=ActionType.PASSIVE,
                    name="Unarmored Defense",
                    description=(
                        "While you are not wearing any armor, your Armor Class equals "
                        "10 + your Dexterity modifier + your Constitution modifier. "
                        "You can use a shield and still gain this benefit."
                    ),
                ),
            ),
        }
        if is_first_class:
            update["saving_throw_proficiencies"] = (
                blueprint.saving_throw_proficiencies
                + (Statistic.STRENGTH, Statistic.CONSTITUTION)
            )
            update["n_skill_choices"] = blueprint.n_skill_choices + 2
            update["skills_to_choose_from"] = frozenset(
                {
                    Skill.ANIMAL_HANDLING,
                    Skill.ATHLETICS,
                    Skill.INTIMIDATION,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                    Skill.SURVIVAL,
                }
            )
        result = blueprint.model_copy(update=update)
        return self.skill_choice_resolver.apply(result) if is_first_class else result
