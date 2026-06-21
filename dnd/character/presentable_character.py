from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Mapping
from itertools import filterfalse
from typing import Annotated
from typing import Self

from dnd.character.ability import Ability
from dnd.character.armor.armors import ARMORS
from dnd.character.armor.names import ArmorName
from dnd.character.character import Character
from dnd.character.feature.feats import feat_name_to_feat
from dnd.character.feature.feats import FeatName
from dnd.character.race.race import Race
from dnd.character.spells import SPELLCASTING_ABILITY_MAP
from dnd.choices.abilities.action_type import ActionType
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import (
    FighterSubclass,
)
from dnd.choices.class_creation.character_class import (
    RogueSubclass,
)
from dnd.choices.class_creation.character_class import (
    subclass_level,
)
from dnd.choices.class_creation.character_class import (
    SUBCLASSES,
)
from dnd.choices.language import Language
from dnd.choices.stats_creation.statistic import Statistic
from dnd.config import resource_paths
from dnd.other_profficiencies import ArmorProficiency
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from dnd.skill_proficiency import skill2ability
from frozendict import frozendict
from pydantic import AfterValidator
from pydantic import computed_field
from pydantic import ConfigDict
from pydantic import model_validator
from pydantic import NonNegativeInt


def _conv_to_frozendict(value: object) -> object:
    if not isinstance(value, Mapping):
        return value
    return frozendict(value)


def _language_not_any(language: Language) -> Language:
    if language == Language.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character language mustn't be any of your choice. Choose a languge"
        )
    return language


def _skill_not_any(skill: Skill) -> Skill:
    if skill == Skill.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character skill mustn't be any of your choice. Choose a skill"
        )
    return skill


def _feat_not_any(feat: FeatName) -> FeatName:
    if feat in FeatName.not_choosables():
        raise ValueError("Character feat mustn't be any of your choice. Choose a feat")
    return feat


def _tool_proficiency_not_any(
    tool: ToolProficiency | GamingSet | MusicalInstrument,
) -> ToolProficiency | GamingSet | MusicalInstrument:
    if isinstance(tool, ToolProficiency) and tool == ToolProficiency.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character tool proficiency mustn't be any of your choice. Choose a tool"
        )
    if isinstance(tool, GamingSet) and tool == GamingSet.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character gaming set mustn't be any of your choice. Choose a gaming set"
        )
    if (
        isinstance(tool, MusicalInstrument)
        and tool == MusicalInstrument.ANY_OF_YOUR_CHOICE
    ):
        raise ValueError(
            "Character musical instrument mustn't be any of your choice. Choose a musical instrument"
        )
    return tool


def _weapon_proficiency_not_any(
    weapon: WeaponProficiency,
) -> WeaponProficiency:
    if weapon == WeaponProficiency.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character weapon proficiency mustn't be any of your choice. Choose a weapon"
        )
    return weapon


def _armor_proficiency_not_any(armor: ArmorProficiency) -> ArmorProficiency:
    if armor == ArmorProficiency.ANY_OF_YOUR_CHOICE:
        raise ValueError(
            "Character armor proficiency mustn't be any of your choice. Choose an armor type"
        )
    return armor


NotAnyLanguage = Annotated[Language, AfterValidator(_language_not_any)]
NotAnySkill = Annotated[Skill, AfterValidator(_skill_not_any)]
NotAnyFeat = Annotated[FeatName, AfterValidator(_feat_not_any)]
NotAnyToolProficiency = Annotated[
    ToolProficiency | GamingSet | MusicalInstrument,
    AfterValidator(_tool_proficiency_not_any),
]
NotAnyWeaponProficiency = Annotated[
    WeaponProficiency, AfterValidator(_weapon_proficiency_not_any)
]
NotAnyArmorProficiency = Annotated[
    ArmorProficiency, AfterValidator(_armor_proficiency_not_any)
]


class PresentableCharacter(Character):
    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def _validate_subclass(self) -> Self:
        for class_, level in self.classes.items():
            if level >= subclass_level[class_]:
                subclasses_of_class = set(SUBCLASSES[class_]).intersection(
                    self.subclasses
                )
                if not subclasses_of_class:
                    raise ValueError(f"No subclasses of class {class_}")
                if len(subclasses_of_class) > 1:
                    raise ValueError(
                        f"More than one subclass of {class_} {subclasses_of_class=}"
                    )
        return self

    @computed_field  # type: ignore[prop-decorator]
    @property
    def abilities(self) -> dict[Skill, int]:
        return {
            s: self._get_modifier(skill2ability[s])
            + (s in self.skill_proficiencies) * self.proficiency_bonus
            for s in Skill
            if s != Skill.ANY_OF_YOUR_CHOICE
        }

    @computed_field  # type: ignore[prop-decorator]
    @property
    def initiative(self) -> int:
        return self._get_modifier(Statistic.DEXTERITY) + 5 * (
            FeatName.ALERT in self.feats
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def passive_perception(self) -> int:
        return self.abilities[Skill.PERCEPTION] + 10

    @computed_field  # type: ignore[prop-decorator]
    @property
    def proficiency_bonus(self) -> int:
        return (self.level - 1) // 4 + 2

    @computed_field  # type: ignore[prop-decorator]
    @property
    def saving_throw_modifiers(self) -> dict[Statistic, int]:
        return {
            s: self._get_modifier(s)
            + self.proficiency_bonus * (s in self.saving_throw_proficiencies)
            for s in Statistic
        }

    @computed_field  # type: ignore[prop-decorator]
    @property
    def ac(self) -> int:
        return (
            max(
                ARMORS[armor].calc_ac(self)
                for armor in (self.armors + (ArmorName.CLOTHES,))
            )
            + self.ac_bonus
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def capacity(self) -> int:
        return 15 * self.stats.get_stat(Statistic.STRENGTH)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def spellcasting_ability(self) -> Statistic | None:
        spellcasting_classes = list(
            filter(
                lambda class_: (
                    class_ in SPELLCASTING_ABILITY_MAP
                    or (
                        class_ is Class.FIGHTER
                        and FighterSubclass.ELDRITCH_KNIGHT in self.subclasses
                    )
                    or (
                        class_ is Class.ROGUE
                        and RogueSubclass.ARCANE_TRICKSTER in self.subclasses
                    )
                ),
                self.classes,
            )
        )
        if not spellcasting_classes:
            return None
        return SPELLCASTING_ABILITY_MAP.get(
            max(spellcasting_classes, key=self.classes.__getitem__),
            Statistic.INTELLIGENCE,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def spell_save_dc(self) -> int | None:
        if self.spellcasting_ability is None:
            return None
        return (
            8
            + self.proficiency_bonus
            + self._get_modifier(self.spellcasting_ability)
            + self.spell_save_dc_bonus
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def spell_attack_bonus(self) -> int | None:
        if self.spellcasting_ability is None:
            return None
        return (
            self._get_spellcasting_modifier()
            + self.proficiency_bonus
            + self.spellcasting_ability_bonus
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def n_prepared_spells(self) -> NonNegativeInt:
        return self.level + max(0, self._get_spellcasting_modifier())

    @computed_field  # type: ignore[prop-decorator]
    @property
    def actions(self) -> dict[ActionType, list[Ability]]:
        actions = defaultdict(list)
        for feat in filterfalse(FeatName.ABILITY_SCORE_IMPROVEMENT.__eq__, self.feats):
            ability = feat_name_to_feat(feat).ability
            if ability:
                actions[ability.action_type].append(ability)
        for ability_name in self.other_active_abilities:
            ability_name = ability_name.split(":")[0]
            ability = Ability.model_validate_json(
                resource_paths.race_abilities_root.joinpath(self.race.value)
                .joinpath(f"{ability_name}.json")
                .read_text()
            )
            actions[ability.action_type].append(ability)
        for class_, class_level in self.classes.items():
            for (
                main_class_ability_path
            ) in resource_paths.main_class_abilities_root.joinpath(class_).iterdir():
                self._add_action(
                    actions,
                    json.loads(main_class_ability_path.read_text()),
                    class_level,
                )
            for subclass_name in self.subclasses:
                if subclass_name not in SUBCLASSES[class_]:
                    continue
                for sub_class_ability_path in (
                    resource_paths.sub_class_abilities_root.joinpath(class_)
                    .joinpath(subclass_name)
                    .iterdir()
                ):
                    self._add_action(
                        actions,
                        json.loads(sub_class_ability_path.read_text()),
                        class_level,
                    )
        return actions

    def _add_action(
        self,
        actions: dict[ActionType, list[Ability]],
        data: Mapping[str, object],  # ignore
        class_level: int,
    ) -> None:
        ability = Ability(**data)  # type: ignore[arg-type]
        if not self._is_ability_accessible(ability, class_level):
            return
        actions[ability.action_type].append(ability)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def health(self) -> int:
        constitution_modifier = self._get_modifier(Statistic.CONSTITUTION)
        health_increase_per_level = constitution_modifier
        if FeatName.TOUGH in self.feats:
            health_increase_per_level += 2
        if self.race == Race.DWARF:
            health_increase_per_level += 1
        return self.health_base + self.level * health_increase_per_level

    def _get_spellcasting_modifier(self) -> int:
        return self._get_modifier(self.spellcasting_ability)  # type: ignore[arg-type]

    def _get_modifier(self, statistic: Statistic) -> int:
        return self.stats.get_modifier(statistic)

    @staticmethod
    def _is_ability_accessible(
        ability: Ability,
        class_level: int,
    ) -> bool:
        return (
            ability and ability.combat_related and ability.required_level <= class_level  # type: ignore[return-value]
        )
