# from __future__ import annotations
#
# from collections.abc import Mapping
# from typing import Self
#
# from typing_extensions import TypeIs
#
# from dnd.character.armor.names import ArmorName
# from dnd.character.character import ClassLevel
# from dnd.character.feature.feats import FeatName
# from dnd.character.magical_item.item import MagicalItem
# from dnd.character.race.race import Race
# from dnd.character.race.subraces import Subrace
# from dnd.character.spells.spells import Spells
# from dnd.character.stats import Stats
# from dnd.choices.alignment import Alignment
# from dnd.choices.background_creatrion.background import (
#     Background,
# )
# from dnd.choices.class_creation.character_class import AnySubclass
# from dnd.choices.class_creation.character_class import Class
# from dnd.choices.equipment_creation.weapons import WeaponName
# from dnd.choices.language import Language
# from dnd.choices.sex import Sex
# from dnd.choices.stats_creation.statistic import Statistic
# from dnd.other_profficiencies import ArmorProficiency
# from dnd.other_profficiencies import GamingSet
# from dnd.other_profficiencies import MusicalInstrument
# from dnd.other_profficiencies import ToolProficiency
# from dnd.other_profficiencies import WeaponProficiency
# from dnd.skill_proficiency import Skill
# from frozendict import frozendict
# from pydantic import BaseModel
# from pydantic import ConfigDict
# from pydantic import Field
# from pydantic import NonNegativeInt
# from pydantic import PositiveInt
#
# type Equipment = WeaponName | ArmorName | str
#
#
# class Blueprint(BaseModel):
#     """Blueprint for building a Character with optional fields.
#
#     All required fields from Character are optional in Blueprint, allowing
#     incremental character construction through building blocks.
#     """
#
#     model_config = ConfigDict(frozen=True)
#
#     # Fields optional in Blueprint, required in Character/_CreatureBase
#     name: str | None = None
#     stats: Stats | None = None
#     speed: PositiveInt | None = None
#     dark_vision_range: NonNegativeInt | None = None
#     sex: Sex | None = None
#     backstory: str | None = None
#     level: ClassLevel | None = None
#     age: PositiveInt | None = None
#     race: Race | None = None
#     subrace: Subrace | None = None
#     background: Background | None = None
#     alignment: Alignment | None = None
#     health_base: PositiveInt | None = None
#     height: PositiveInt | None = None
#     weight: PositiveInt | None = None
#     eye_color: str | None = None
#     skin_color: str | None = None
#     hairstyle: str | None = None
#     appearance: str | None = None
#     character_traits: str | None = None
#     ideals: str | None = None
#     bonds: str | None = None
#     weaknesses: str | None = None
#     base_description: str | None = None
#
#     # Fields with defaults in both Blueprint and Character
#     classes: Mapping[Class, PositiveInt] = Field(default_factory=frozendict)
#     stats_cup: Stats = Field(
#         default=Stats(
#             strength=20,
#             dexterity=20,
#             constitution=20,
#             intelligence=20,
#             wisdom=20,
#             charisma=20,
#         )
#     )
#     saving_throw_bonuses: Stats = Field(
#         default=Stats(
#             strength=0,
#             dexterity=0,
#             constitution=0,
#             intelligence=0,
#             wisdom=0,
#             charisma=0,
#         )
#     )
#     initiative_bonus: int = 0
#     ac_bonus: NonNegativeInt = 0
#     spell_save_dc_bonus: NonNegativeInt = 0
#     spellcasting_ability_bonus: NonNegativeInt = 0
#     feats: tuple[FeatName, ...] = Field(
#         description="Feats from a list fitting description of the character if"
#         " race is variant human at least one must be different "
#         "than ability score improvement",
#         default=(),
#     )
#     subclasses: tuple[AnySubclass, ...] = ()
#     armors: tuple[ArmorName, ...] = ()
#     weapons: tuple[WeaponName, ...] = ()
#     other_equipment: tuple[str, ...] = ()
#     spells: Spells = Field(default_factory=Spells)
#     languages: tuple[Language, ...] = Field(default=())
#     skill_proficiencies: tuple[Skill, ...] = Field(
#         default=(), description="Skills the character is proficient in"
#     )
#     tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...] = (
#         Field(default=(), description="Tool proficiencies")
#     )
#     weapon_proficiencies: frozenset[WeaponProficiency] = frozenset()
#     armor_proficiencies: frozenset[ArmorProficiency] = frozenset()
#     magical_items: tuple[MagicalItem, ...] = ()
#     saving_throw_proficiencies: tuple[Statistic, ...] = ()
#     other_active_abilities: tuple[str, ...] = ()
#
#     # Blueprint-specific fields
#     n_stat_choices: NonNegativeInt = 0
#     n_skill_choices: NonNegativeInt = 0
#     skills_to_choose_from: frozenset[Skill] = Field(
#         default_factory=frozenset,
#         description="Skills from which n_skill_choices can be chosen",
#     )
#     equipment_choices: tuple[tuple[Equipment, ...], ...] = ()
#
#     def add_diff(self, diff: Self) -> Self:
#         return self.model_copy(
#             update={
#                 field_name: field_value
#                 for field_name, field_value in diff
#                 if field_name in diff.model_fields_set
#             }
#         )
#
#
# class BlueprintWithStats(Blueprint):
#     stats: Stats
#
#
# def has_stats(blueprint: Blueprint) -> TypeIs[BlueprintWithStats]:
#     return blueprint.stats is not None
