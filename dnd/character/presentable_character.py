from typing import TYPE_CHECKING
from typing import Literal

from dnd.character.armor.armors import ARMORS
from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.character_data import CharacterData
from dnd.character.blueprint.sentinels import AnyClassLevel
from dnd.character.blueprint.sentinels import AnySorcererLevel
from dnd.character.blueprint.sentinels import AnyWizardLevel
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.sentinels import Level
from dnd.character.feature.feats import FeatName
from dnd.character.race.race import Race
from dnd.character.spells import SPELLCASTING_ABILITY_MAP
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import FighterSubclass
from dnd.choices.class_creation.character_class import RogueSubclass

from dnd.choices.stats_creation.statistic import Statistic
from dnd.skill_proficiency import Skill
from dnd.skill_proficiency import skill2ability
from pydantic import ConfigDict
from pydantic import NonNegativeInt
from pydantic import PositiveInt
from typing import ClassVar

if TYPE_CHECKING:
    _cf = property
else:
    from pydantic import computed_field as _cf


class PresentableCharacter(
    Blueprint[
        Race,
        Stats,
        PositiveInt,
        Literal[0],
        Literal[0],
        AnyWizardLevel,
        AnySorcererLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        AnyClassLevel,
        CharacterData,
    ]
):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="allow")
    level: Level

    @_cf
    def abilities(self) -> dict[Skill, int]:
        return {
            s: self._get_modifier(skill2ability[s])
            + (s in self.skill_proficiencies) * self.proficiency_bonus
            for s in Skill
            if s != Skill.ANY_OF_YOUR_CHOICE
        }

    @_cf
    def initiative(self) -> int:
        return self._get_modifier(Statistic.DEXTERITY) + 5 * (
            FeatName.ALERT in self.feats
        )

    @_cf
    def passive_perception(self) -> int:
        return self.abilities[Skill.PERCEPTION] + 10

    @_cf
    def proficiency_bonus(self) -> int:
        return (self.level - 1) // 4 + 2

    @_cf
    def saving_throw_modifiers(self) -> dict[Statistic, int]:
        return {
            s: self._get_modifier(s)
            + self.proficiency_bonus * (s in self.saving_throw_proficiencies)
            for s in Statistic
        }

    @_cf
    def ac(self) -> int:
        return (
            max(
                ARMORS[armor].calc_ac(self)
                for armor in (self.armors + (ArmorName.CLOTHES,))
            )
            + self.ac_bonus
        )

    @_cf
    def capacity(self) -> int:
        return 15 * self.stats.get_stat(Statistic.STRENGTH)

    @_cf
    def spellcasting_ability(self) -> Statistic | None:
        spellcasting_classes = [
            class_
            for class_, _ in self.classes.all_levels()
            if (
                class_ in SPELLCASTING_ABILITY_MAP
                or (
                    class_ is Class.FIGHTER
                    and FighterSubclass.ELDRITCH_KNIGHT in self.subclasses
                )
                or (
                    class_ is Class.ROGUE
                    and RogueSubclass.ARCANE_TRICKSTER in self.subclasses
                )
            )
        ]
        if not spellcasting_classes:
            return None
        return SPELLCASTING_ABILITY_MAP.get(
            max(spellcasting_classes, key=self.classes.get_level),
            Statistic.INTELLIGENCE,
        )

    @_cf
    def spell_save_dc(self) -> int | None:
        if self.spellcasting_ability is None:
            return None
        return (
            8
            + self.proficiency_bonus
            + self._get_modifier(self.spellcasting_ability)
            + self.spell_save_dc_bonus
        )

    @_cf
    def spell_attack_bonus(self) -> int | None:
        if self.spellcasting_ability is None:
            return None
        return (
            self._get_spellcasting_modifier()
            + self.proficiency_bonus
            + self.spellcasting_ability_bonus
        )

    @_cf
    def n_prepared_spells(self) -> NonNegativeInt:
        return self.level + max(0, self._get_spellcasting_modifier())

    @_cf
    def health(self) -> int:
        constitution_modifier = self._get_modifier(Statistic.CONSTITUTION)
        health_increase_per_level = constitution_modifier
        if FeatName.TOUGH in self.feats:
            health_increase_per_level += 2
        if self.race == Race.DWARF:
            health_increase_per_level += 1
        return self.health_base + self.level * health_increase_per_level

    def _get_spellcasting_modifier(self) -> int:
        if self.spellcasting_ability is None:
            return 0
        return self._get_modifier(self.spellcasting_ability)

    def _get_modifier(self, statistic: Statistic) -> int:
        return self.stats.get_modifier(statistic)
