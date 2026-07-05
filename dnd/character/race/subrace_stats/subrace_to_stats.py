from __future__ import annotations

from dnd.character.race.subrace_stats.race_statistics import (
    RaceStatistics,
)
from dnd.character.race.subrace_stats.subrace_stats import (
    Subrace,
)
from dnd.character.race.subraces import SubraceName
from dnd.choices.language import Language
from dnd.skill_proficiency import Skill
from typing import assert_never


def _get_subrace_stats(subrace: SubraceName) -> Subrace:
    match subrace:
        case (
            SubraceName.AARAKOCRA_AARAKOCRA_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        ):
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Ability Score Increase",
                    "Creature Type",
                    "Size",
                    # "Flight",
                    "Talons",
                    "Wind Caller",
                ),
            )
        case SubraceName.AASIMAR_FALLEN_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.CELESTIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.DECEPTION, Skill.RELIGION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Healing Hands",
                    "Light Bearer",
                    "Celestial Revelation - Necrotic Shroud",
                ),
            )
        case SubraceName.AASIMAR_PROTECTOR_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.CELESTIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.MEDICINE, Skill.PERSUASION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=2,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Healing Hands",
                    "Light Bearer",
                    "Celestial Revelation - Radiant Soul",
                ),
            )
        case SubraceName.AASIMAR_SCOURGE_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.CELESTIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.INTIMIDATION, Skill.SURVIVAL),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Healing Hands",
                    "Light Bearer",
                    "Celestial Revelation - Radiant Consumption",
                ),
            )
        case SubraceName.AASIMAR_FALLEN_AASIMAR_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.CELESTIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Necrotic Shroud",),
            )
        case SubraceName.AASIMAR_PROTECTOR_AASIMAR_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.CELESTIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Radiant Soul",),
            )
        case SubraceName.AASIMAR_SCOURGE_AASIMAR_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.CELESTIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Radiant Consumption",),
            )
        case SubraceName.BUGBEAR_BUGBEAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.STEALTH,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    "Fey Ancestry",
                    "Long-Limbed",
                    "Powerful Build",
                    "Sneaky",
                    "Surprise Attack",
                ),
            )
        case SubraceName.BUGBEAR_BUGBEAR_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.STEALTH,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Long-Limbed",
                    "Powerful Build",
                    "Sneaky",
                    "Surprise Attack",
                ),
            )
        case SubraceName.CENTAUR_GRUUL_CENTAUR_GUILDMASTERSGUIDETORAVNICA:
            return Subrace(
                speed=40,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.SYLVAN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.MEDICINE,
                    Skill.NATURE,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Charge",
                    "Hooves",
                    "Equine Build",
                    "Survivor",
                ),
            )
        case SubraceName.CENTAUR_SELESNYA_CENTAUR_GUILDMASTERSGUIDETORAVNICA:
            return Subrace(
                speed=40,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.SYLVAN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.MEDICINE,
                    Skill.NATURE,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Charge",
                    "Hooves",
                    "Equine Build",
                    "Survivor",
                ),
            )
        case SubraceName.CENTAUR_CENTAURS_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=40,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.MEDICINE,
                    Skill.NATURE,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Charge",
                    "Equine Build",
                    "Hooves",
                    "Natural Affinity",
                ),
            )
        case SubraceName.CENTAUR_LAGONNA_MYTHICODYSSEYSOFTHEROS:
            return Subrace(
                speed=40,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.SYLVAN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ANIMAL_HANDLING, Skill.SURVIVAL),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Charge",
                    "Hooves",
                    "Equine Build",
                    "Survivor",
                ),
            )
        case SubraceName.CENTAUR_PHERES_MYTHICODYSSEYSOFTHEROS:
            return Subrace(
                speed=40,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.SYLVAN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ANIMAL_HANDLING, Skill.SURVIVAL),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Charge",
                    "Hooves",
                    "Equine Build",
                    "Survivor",
                ),
            )
        case SubraceName.CHANGELING_CHANGELING_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.DECEPTION,
                    Skill.INSIGHT,
                    Skill.INTIMIDATION,
                    Skill.PERSUASION,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=1,
                ),
                other_active_abilities=("Shapechanger", "Changeling Instincts"),
            )
        case SubraceName.CHANGELING_CHANGELING_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.DECEPTION,
                    Skill.INSIGHT,
                    Skill.INTIMIDATION,
                    Skill.PERFORMANCE,
                    Skill.PERSUASION,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=("Shapechanger", "Changeling Instincts"),
            )
        case SubraceName.CHANGELING_CHANGELING_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(Skill.DECEPTION,),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),  # TODO: Parse ['Any of your choice']
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Change Appearance",
                    "Unsettling Visage",
                    "Divergent Persona",
                ),
            )
        case SubraceName.DRAGONBORN_DRACONBLOOD_EXPLORERSGUIDETOWILDEMOUNT:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.DRACONIC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERSUASION, Skill.INTIMIDATION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=2,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Forceful Presence",),
            )
        case SubraceName.DRAGONBORN_RAVENITE_EXPLORERSGUIDETOWILDEMOUNT:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.DRACONIC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ATHLETICS, Skill.INTIMIDATION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Vengeful Assault",),
            )
        case SubraceName.DRAGONBORN_CHROMATIC_FIZBANSTREASURYOFDRAGONS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Chromatic Ancestry",
                    "Breath Weapon",
                    "Draconic Resistance",
                    "Chromatic Warding",
                ),
            )
        case SubraceName.DRAGONBORN_GEM_FIZBANSTREASURYOFDRAGONS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    # "Gem Ancestry",
                    "Breath Weapon",
                    "Draconic Resistance",
                    "Psionic Mind",
                    "Gem Flight",
                ),
            )
        case SubraceName.DRAGONBORN_METALLIC_FIZBANSTREASURYOFDRAGONS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    # "Metallic Ancestry",
                    "Breath Weapon",
                    "Draconic Resistance",
                    "Metallic Breath Weapon",
                ),
            )
        case SubraceName.DRAGONBORN_DRAGONBORN_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.DRACONIC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Draconic Ancestry",
                    "Breath Weapon",
                    "Damage Resistance",
                ),
            )
        case SubraceName.DRAGONBORN_CHROMATIC_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Chromatic Ancestry",
                    "Breath Weapon",
                    "Draconic Resistance",
                    "Chromatic Warding",
                ),
            )
        case SubraceName.DRAGONBORN_GEM_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    # "Gem Ancestry",
                    "Breath Weapon",
                    "Draconic Resistance",
                    "Psionic Mind",
                    "Gem Flight",
                ),
            )
        case SubraceName.DRAGONBORN_METALLIC_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    # "Metallic Ancestry",
                    "Breath Weapon",
                    "Draconic Resistance",
                    "Metallic Breath Weapon",
                ),
            )
        case SubraceName.DWARF_HILL_DWARF_PLAYERSHANDBOOK:
            return Subrace(
                speed=25,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.DWARVISH,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Dwarven Toughness",),
            )
        case SubraceName.DWARF_MOUNTAIN_DWARF_PLAYERSHANDBOOK:
            return Subrace(
                speed=25,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.DWARVISH,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Dwarven Armor Training",),
            )
        case SubraceName.ELF_MARK_OF_SHADOW_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVISH,
                ),
                obligatory_skills=(Skill.STEALTH, Skill.PERFORMANCE),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Cunning Intuition",
                    "Shape Shadows",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.ELF_PALLID_ELF_EXPLORERSGUIDETOWILDEMOUNT:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVISH,
                ),
                obligatory_skills=(Skill.INSIGHT, Skill.INVESTIGATION),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Incisive Sense",
                    "Blessing of the Moonweaver",
                ),
            )
        case SubraceName.ELF_BISHTAHAR_ELF_PLANESHIFTKALADESH:
            return Subrace(
                speed=35,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVISH,
                ),
                obligatory_skills=(Skill.NATURE, Skill.SURVIVAL),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Elf Weapon Training",
                    "Fleet of Foot",
                    "Mask of the Wild",
                ),
            )
        case SubraceName.ELF_TIRAHAR_ELF_PLANESHIFTKALADESH:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVISH,
                ),
                obligatory_skills=(Skill.ANIMAL_HANDLING, Skill.STEALTH),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Elf Weapon Training",),
            )
        case SubraceName.ELF_VAHADAR_ELF_PLANESHIFTKALADESH:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVISH,
                ),
                obligatory_skills=(Skill.ARCANA, Skill.HISTORY),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Elf Weapon Training",
                    "Cantrip",
                ),
            )
        case SubraceName.ELF_JURAGA_PLANESHIFTZENDIKAR:
            return Subrace(
                speed=35,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANY_OF_YOUR_CHOICE,
                    Skill.ANY_OF_YOUR_CHOICE,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Elf Weapon Training",
                    "Fleet of Foot",
                    "Mask of the Wild",
                ),
            )
        case SubraceName.ELF_MUL_DAYA_PLANESHIFTZENDIKAR:
            return Subrace(
                speed=30,
                dark_vision_range=120,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANY_OF_YOUR_CHOICE,
                    Skill.ANY_OF_YOUR_CHOICE,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Superior Darkvision",
                    "Sunlight Sensitivity",
                    "Mul Daya Magic",
                    "Elf Weapon Training",
                ),
            )
        case SubraceName.ELF_TAJURU_PLANESHIFTZENDIKAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANY_OF_YOUR_CHOICE,
                    Skill.ANY_OF_YOUR_CHOICE,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=2,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Skill Versatility",),
            )
        case SubraceName.ELF_DARK_ELF_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=120,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                ),
                obligatory_skills=(Skill.STEALTH,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Superior Darkvision",
                    "Sunlight Sensitivity",
                    "Drow Magic",
                    "Drow Weapon Training",
                ),
            )
        case SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                ),
                obligatory_skills=(Skill.ARCANA,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Cantrip", "Elf Weapon Training"),
            )
        case SubraceName.ELF_WOOD_ELF_PLAYERSHANDBOOK:
            return Subrace(
                speed=35,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                ),
                obligatory_skills=(Skill.PERCEPTION,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Elf Weapon Training",
                    "Fleet of Foot",
                    "Mask of the Wild",
                ),
            )
        case SubraceName.ELF_ASTRAL_ELF_SPELLJAMMERADVENTURESINSPACE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(Skill.PERCEPTION,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    "Astral Fire",
                    "Fey Ancestry",
                    "Keen Senses",
                    "Starlight Step",
                    "Astral Trance",
                ),
            )
        case SubraceName.FIRBOLG_FIRBOLG_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Firbolg Magic",
                    "Hidden Step",
                    "Powerful Build",
                    "Speech of Beast and Leaf",
                ),
            )
        case SubraceName.FIRBOLG_FIRBOLG_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ELVISH,
                    Language.GIANT,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=2,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Firbolg Magic",
                    "Hidden Step",
                    "Powerful Build",
                    "Speech of Beast and Leaf",
                ),
            )
        case SubraceName.GENASI_AIR_AIR_GENASI_ELEMENTALEVILPLAYERSCOMPANION:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.PRIMORDIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=2,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Unending Breath",
                    "Mingle with the Wind",
                ),
            )
        case SubraceName.GENASI_AIR_AIR_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=35,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    "Creature Type",
                    "Size",
                    "Unending Breath",
                    "Lightning Resistance",
                    "Mingle with the Wind",
                ),
            )
        case SubraceName.GENASI_EARTH_EARTH_GENASI_ELEMENTALEVILPLAYERSCOMPANION:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.PRIMORDIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Earth Walk",
                    "Merge with Stone",
                ),
            )
        case SubraceName.GENASI_EARTH_EARTH_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Earth Walk",
                    "Merge with Stone",
                ),
            )
        case SubraceName.GENASI_FIRE_FIRE_GENASI_ELEMENTALEVILPLAYERSCOMPANION:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.PRIMORDIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=2,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Fire Resistance",
                    "Reach to the Blaze",
                ),
            )
        case SubraceName.GENASI_FIRE_FIRE_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Fire Resistance",
                    "Reach to the Blaze",
                ),
            )
        case SubraceName.GENASI_WATER_WATER_GENASI_ELEMENTALEVILPLAYERSCOMPANION:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.PRIMORDIAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Acid Resistance",
                    "Amphibious",
                    "Call to the Wave",
                ),
            )
        case SubraceName.GENASI_WATER_WATER_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Acid Resistance",
                    "Amphibious",
                    "Call to the Wave",
                ),
            )
        case SubraceName.GNOME_MARK_OF_SCRIBING_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.GNOMISH,
                ),
                obligatory_skills=(Skill.ARCANA, Skill.HISTORY),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),  # TODO: Parse ["Calligrapher's supplies"]
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Gifted Scribe",
                    "Scribe's Insight",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.GNOME_FOREST_GNOME_PLAYERSHANDBOOK:
            return Subrace(
                speed=25,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GNOMISH,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=2,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Natural Illusionist",
                    "Speak with Small Beasts",
                ),
            )
        case SubraceName.GNOME_ROCK_GNOME_PLAYERSHANDBOOK:
            return Subrace(
                speed=25,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GNOMISH,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),  # TODO: Parse ["Tinker's tools"]
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=2,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Artificer's Lore",
                    "Tinker",
                ),
            )
        case SubraceName.GOBLIN_DANKWOOD_GOBLIN_ADVENTURESWITHMUKDANKWOOD:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Speak with Small Beasts",
                    "Nimble Escape",
                ),
            )
        case SubraceName.GOBLIN_GOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ACROBATICS, Skill.STEALTH),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=2,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Creature Type",
                    "Size",
                    "Fey Ancestry",
                    "Fury of the Small",
                    "Nimble Escape",
                ),
            )
        case SubraceName.GOBLIN_GOBLIN_PLANESHIFTIXALAN:
            return Subrace(
                speed=25,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Agile Climber", "Darkvision"),
            )
        case SubraceName.GOBLIN_GOBLIN_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Fury of the Small", "Nimble Escape"),
            )
        case SubraceName.GOLIATH_GOLIATH_ELEMENTALEVILPLAYERSGUIDE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.GIANT,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ATHLETICS,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Natural Athlete",
                    "Stone's Endurance",
                    "Powerful Build",
                    "Mountain Born",
                ),
            )
        case SubraceName.GOLIATH_GOLIATH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ATHLETICS,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    "Little Giant",
                    "Mountain Born",
                    "Stone's Endurance",
                ),
            )
        case SubraceName.GRUNG_GRUNG_PLAYERSHANDBOOK:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(Language.GRUNG,),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERCEPTION,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Amphibious",
                    "Poison Immunity",
                    "Poisonous Skin",
                    "Standing Leap",
                    "Water Dependency",
                ),
            )
        case SubraceName.HALF_ELF_AQUATIC_ELF_HERITAGE_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=2,
                ),
                other_active_abilities=(
                    # "Swim",
                ),
            )
        case SubraceName.HALF_ELF_DARK_ELF_HERITAGE_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=2,
                ),
                other_active_abilities=("Drow Magic",),
            )
        case SubraceName.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=2,
                ),
                other_active_abilities=("Cantrip",),
            )
        case SubraceName.HALF_ELF_WOOD_ELF_HERITAGE_PLAYERSHANDBOOK:
            return Subrace(
                speed=35,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ELVEN,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=2,
                ),
                other_active_abilities=(
                    "Fleet of Foot",
                    "Mask of the Wild",
                ),
            )
        case SubraceName.HALF_ORC_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERCEPTION, Skill.SURVIVAL),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=2,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Hunter's Intuition",
                    # "Finder's Magic",
                ),
            )
        case SubraceName.HALF_ORC_HALF_ORC_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ORC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.INTIMIDATION,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Relentless Endurance",
                    "Savage Attacks",
                    "Menacing",
                ),
            )
        case SubraceName.HALFLING_MARK_OF_HEALING_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.HALFLING,
                ),
                obligatory_skills=(Skill.MEDICINE,),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Medical Intuition",
                    "Healing Touch",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.HALFLING_MARK_OF_HOSPITALITY_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.HALFLING,
                ),
                obligatory_skills=(Skill.PERSUASION,),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Ever Hospitable",
                    "Innkeeper's Magic",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.HALFLING_LOTUSDEN_HALFLING_EXPLORERSGUIDETOWILDEMOUNT:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.HALFLING,
                ),
                obligatory_skills=(Skill.NATURE, Skill.SURVIVAL),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Children of the Woods",
                    "Timberwalk",
                ),
            )
        case SubraceName.HALFLING_LIGHTFOOT_PLAYERSHANDBOOK:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.HALFLING,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Naturally Stealthy",),
            )
        case SubraceName.HALFLING_STOUT_PLAYERSHANDBOOK:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.HALFLING,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Stout Resilience",),
            )
        case SubraceName.HALFLING_GHOSTWISE_SWORDCOASTADVENTURERSGUIDE:
            return Subrace(
                speed=25,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.HALFLING,
                ),
                obligatory_skills=(Skill.STEALTH,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Silent Speech",),
            )
        case (
            SubraceName.HOBGOBLIN_HOBGOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        ):
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ATHLETICS,
                    Skill.INTIMIDATION,
                    Skill.ANY_OF_YOUR_CHOICE,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Fey Ancestry",
                    "Fey Gift",
                    "Fortune from the Many",
                ),
            )
        case SubraceName.HOBGOBLIN_HOBGOBLIN_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ATHLETICS, Skill.INTIMIDATION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Martial Training",
                    # "Hobgoblin Resilience",
                ),
            )
        case SubraceName.HOBGOBLIN_HOBGOBLIN_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=2,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Martial Training", "Saving Face"),
            )
        case SubraceName.HUMAN_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                ),
                obligatory_skills=(Skill.PERCEPTION, Skill.SURVIVAL),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=2,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Hunter's Intuition",
                    # "Finder's Magic",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.HUMAN_MARK_OF_HANDLING_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(Language.COMMON,),
                obligatory_skills=(Skill.ANIMAL_HANDLING, Skill.NATURE),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=2,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    "Wild Intuition (Mark of Handling)",
                    # "Primal Connection",
                    # "The Bigger They Are",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.HUMAN_MARK_OF_MAKING_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(Language.COMMON,),
                obligatory_skills=(Skill.ARCANA,),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=2,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    # "Artisan's Intuition",
                    # "Artisan's Gift",
                    # "Spellsmith",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.HUMAN_MARK_OF_PASSAGE_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(Language.COMMON,),
                obligatory_skills=(Skill.ACROBATICS,),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    # "Courier's Speed",
                    # "Intuitive Motion",
                    # "Magical Passage",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.HUMAN_MARK_OF_SENTINEL_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(Language.COMMON,),
                obligatory_skills=(Skill.INSIGHT, Skill.PERCEPTION),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Sentinel's Intuition",
                    # "Guardian's Shield",
                    # "Vigilant Guardian",
                    # "Spells of the Mark",
                ),
            )
        case SubraceName.HUMAN_KELDON_PLANESHIFTDOMINARIA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(Skill.ATHLETICS,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Keldon Resilience (Keldon)",
                    "Icehaven Born (Keldon)",
                ),
            )
        case SubraceName.HUMAN_GAVONY_PLANESHIFTINNISTRAD:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=1,
                    constitution=1,
                    intelligence=1,
                    wisdom=1,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Ability Score Increase",),
            )
        case SubraceName.HUMAN_KESSIG_PLANESHIFTINNISTRAD:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(Skill.SURVIVAL,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Ability Score Increase (Kessig)",
                    "Forest Folk (Kessig)",
                    "Fleet of Foot (Kessig)",
                    "Sure-Footed (Kessig)",
                    "Spring Attack (Kessig)",
                ),
            )
        case SubraceName.HUMAN_NEPHALIA_PLANESHIFTINNISTRAD:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Ability Score Increase (Nephalia)",
                    "Breadth of Knowledge (Nephalia)",
                ),
            )
        case SubraceName.HUMAN_STENSIA_PLANESHIFTINNISTRAD:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(Skill.INTIMIDATION,),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Ability Score Increase (Stensia)",
                    "Daunting (Stensia)",
                    "Tough (Stensia)",
                ),
            )
        case SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=1,
                    constitution=1,
                    intelligence=1,
                    wisdom=1,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(),
            )
        case SubraceName.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=True,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=2,
                ),
                other_active_abilities=(),
            )
        case SubraceName.KENKU_KENKU_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANY_OF_YOUR_CHOICE,
                    Skill.ANY_OF_YOUR_CHOICE,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Expert Duplication",
                    "Kenku Recall",
                    "Mimicry",
                ),
            )
        case SubraceName.KALASHTAR_KALASHTAR_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.QUORI,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=2,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Dual Mind",
                    "Mental Discipline",
                    "Mind Link",
                    "Severed from Dreams",
                ),
            )
        case SubraceName.KALASHTAR_KALASHTAR_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.QUORI,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=1,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    "Dual Mind (Unearthed Arcana)",
                    "Mental Discipline",
                    "Mind Link",
                    "Psychic Glamour",
                    "Severed from Dreams",
                ),
            )
        case SubraceName.KOBOLD_KOBOLD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ARCANA,
                    Skill.INVESTIGATION,
                    Skill.MEDICINE,
                    Skill.SLEIGHT_OF_HAND,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=2,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Draconic Cry",
                    # "Kobold Legacy",
                ),
            )
        case SubraceName.KOBOLD_KOBOLD_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.DRACONIC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.STEALTH,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Draconic Legacy",
                    "Draconic Roar",
                ),
            )
        case SubraceName.KOBOLD_KOBOLD_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.DRACONIC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Grovel, Cower, and Beg",
                    "Pack Tactics",
                    "Sunlight Sensitivity",
                ),
            )
        case SubraceName.LEONIN_LEONIN_LEONINFEATURES:
            return Subrace(
                speed=35,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.LEONIN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ATHLETICS,
                    Skill.INTIMIDATION,
                    Skill.PERCEPTION,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Claws",
                    "Hunter's Instincts",
                    "Daunting Roar",
                ),
            )
        case SubraceName.LIZARDFOLK_LIZARDFOLK_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                    Skill.STEALTH,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Bite",
                    "Hold Breath",
                    "Hungry Jaws",
                    "Natural Armor",
                    "Nature's Intuition",
                ),
            )
        case SubraceName.LIZARDFOLK_LIZARDFOLK_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.DRACONIC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                    Skill.STEALTH,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Bite",
                    "Cunning Artisan",
                    "Hold Breath",
                    "Hunter's Lore",
                    "Natural Armor",
                    "Hungry Jaws",
                ),
            )
        case SubraceName.MINOTAUR_MINOTAUR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Horns",
                    "Goring Rush",
                    "Hammering Horns",
                    "Labyrinthine Recall",
                ),
            )
        case SubraceName.ORC_ORC_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ORC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.INSIGHT,
                    Skill.INTIMIDATION,
                    Skill.MEDICINE,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Aggressive",
                    "Powerful Build",
                    "Primal Intuition",
                ),
            )
        case SubraceName.ORC_ORC_EXPLORERSGUIDETOWILDEMOUNT:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ORC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.INSIGHT,
                    Skill.INTIMIDATION,
                    Skill.MEDICINE,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Aggressive",
                    "Powerful Build",
                    "Primal Intuition",
                ),
            )
        case SubraceName.ORC_ORC_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Adrenaline Rush",
                    "Powerful Build",
                    "Relentless Endurance",
                ),
            )
        case SubraceName.ORC_ORC_PLANESHIFTIXALAN:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ORC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.INTIMIDATION,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Menacing",
                    "Relentless Endurance",
                    "Savage Attacks",
                ),
            )
        case SubraceName.ORC_ORC_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ORC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.INTIMIDATION,
                    Skill.MEDICINE,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Aggressive",
                    "Primal Intuition",
                    "Powerful Build",
                ),
            )
        case SubraceName.YUAN_TI_PUREBLOOD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Creature Type",
                    "Size",
                    "Magic Resistance",
                    "Poison Resilience",
                    "Serpentine Spellcasting",
                ),
            )
        case SubraceName.YUAN_TI_PUREBLOOD_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ABYSSAL,
                    Language.DRACONIC,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Innate Spellcasting",
                    "Magic Resistance",
                    "Poison Immunity",
                ),
            )
        case SubraceName.SATYR_SATYR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=35,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(Skill.PERFORMANCE, Skill.PERSUASION),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),  # TODO: Parse ['Any of your choice']
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Ram",
                    "Magic Resistance",
                    "Mirthful Leaps",
                    "Reveler",
                ),
            )
        case SubraceName.SATYR_SATYR_MYTHICODYSSEYSOFTHEROS:
            return Subrace(
                speed=35,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.SYLVAN,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERFORMANCE, Skill.PERSUASION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Fey (Satyrs)",
                    "Ram (Satyrs)",
                    "Magic Resistance",
                    "Mirthful Leaps (Satyrs)",
                    "Reveler (Satyrs)",
                ),
            )
        case SubraceName.SHIFTER_BEASTHIDE_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(Language.COMMON,),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ATHLETICS,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Beasthide",),
            )
        case SubraceName.SHIFTER_LONGTOOTH_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(Language.COMMON,),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.INTIMIDATION,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Longtooth",),
            )
        case SubraceName.SHIFTER_SWIFTSTRIDE_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(Language.COMMON,),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ACROBATICS,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Swiftstride",),
            )
        case SubraceName.SHIFTER_WILDHUNT_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(Language.COMMON,),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.SURVIVAL,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=2,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Mark the Scent",),
            )
        case SubraceName.SHIFTER_BEASTHIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.SURVIVAL,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=2,
                ),
                other_active_abilities=("Beasthide",),
            )
        case SubraceName.SHIFTER_LONGTOOTH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ATHLETICS,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=2,
                ),
                other_active_abilities=("Longtooth",),
            )
        case (
            SubraceName.SHIFTER_SWIFTSTRIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        ):
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ACROBATICS,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=2,
                ),
                other_active_abilities=("Swiftstride",),
            )
        case SubraceName.SHIFTER_WILDHUNT_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.INSIGHT,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=2,
                ),
                other_active_abilities=("Wildhunt",),
            )
        case SubraceName.SHIFTER_CLIFFWALK_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Cliffwalk",),
            )
        case SubraceName.SHIFTER_RAZORCLAW_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Razorclaw",),
            )
        case SubraceName.TABAXI_TABAXI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERCEPTION, Skill.STEALTH),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Cat's Claws",
                    "Cat's Talent",
                    "Feline Agility",
                ),
            )
        case SubraceName.TABAXI_TABAXI_VOLOSGUIDETOMONSTERS:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERCEPTION, Skill.STEALTH),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=1,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Feline Agility",
                    "Cat's Claws",
                    "Cat's Talent",
                ),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_BAALZEBUL_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ARCANA, Skill.DECEPTION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Maladomini",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_DISPATER_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.INVESTIGATION, Skill.STEALTH),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Dis",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_FIERNA_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERSUASION, Skill.INSIGHT),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=1,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Phlegethos",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_GLASYA_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.SLEIGHT_OF_HAND, Skill.DECEPTION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=1,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Malbolge",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_LEVISTUS_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.SURVIVAL, Skill.INTIMIDATION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Stygia",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_MAMMON_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.INSIGHT, Skill.PERSUASION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Minauros",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_MEPHISTOPHELES_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ARCANA, Skill.HISTORY),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Cania",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_ZARIEL_MORDENKAINENSTOMEOFFOES:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ATHLETICS, Skill.INTIMIDATION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=1,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Legacy of Avernus",),
            )
        case SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=("Infernal Legacy",),
            )
        case SubraceName.TIEFLING_DEVILS_TONGUE_SWORDCOASTADVENTURERSGUIDE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.DECEPTION, Skill.PERSUASION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Vicious Mockery cantrip",
                    # "Charm Person spell (2nd-level once)",
                    # "Enthrall spell (once)",
                ),
            )
        case SubraceName.TIEFLING_FERAL_SWORDCOASTADVENTURERSGUIDE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.DECEPTION, Skill.STEALTH),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=0,
                    intelligence=1,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Replace Ability Score Increase trait",
                ),
            )
        case SubraceName.TIEFLING_HELLFIRE_SWORDCOASTADVENTURERSGUIDE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ARCANA, Skill.INTIMIDATION),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Burning Hands spell (2nd-level once,2",
                ),
            )
        case SubraceName.TIEFLING_WINGED_SWORDCOASTADVENTURERSGUIDE:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.INFERNAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ACROBATICS, Skill.ATHLETICS),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    # "Flight",
                ),
            )
        case SubraceName.TIEFLING_ABYSSAL_TIEFLING_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=60,
                languages=(
                    Language.COMMON,
                    Language.ABYSSAL,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Abyssal Arcana",
                    "Abyssal Fortitude",
                ),
            )
        case SubraceName.TORTLE_TORTLE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(
                    Skill.ANIMAL_HANDLING,
                    Skill.MEDICINE,
                    Skill.NATURE,
                    Skill.PERCEPTION,
                    Skill.STEALTH,
                    Skill.SURVIVAL,
                ),
                n_skills=2,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=0,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=3,
                ),
                other_active_abilities=(
                    "Claws",
                    "Hold Breath",
                    "Natural Armor",
                    "Nature's Intuition",
                    "Shell Defense",
                ),
            )
        case SubraceName.VERDAN_VERDAN_PLAYERSHANDBOOK:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.GOBLIN,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.PERSUASION,),
                n_skills=1,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=2,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Black Blood Healing",
                    "Limited Telepathy",
                    "Telepathic Insight",
                ),
            )
        case SubraceName.WARFORGED_WARFORGED_EBERRONRISINGFROMTHELASTWAR:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(
                    Language.COMMON,
                    Language.ANY_OF_YOUR_CHOICE,
                ),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),  # TODO: Parse ['Any of your choice']
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=2,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=1,
                ),
                other_active_abilities=(
                    "Constructed Resilience",
                    "Sentry's Rest",
                    "Integrated Protection",
                    "Specialized Design",
                ),
            )
        case SubraceName.WARFORGED_ENVOY_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(Language.COMMON,),
                obligatory_skills=(),
                skills_to_choose_from=(Skill.ANY_OF_YOUR_CHOICE,),
                n_skills=1,
                tool_proficiencies=(),  # TODO: Parse ['Any of your choice']
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=2,
                ),
                other_active_abilities=(
                    "Specialized Design",
                    "Integrated Tool",
                ),
            )
        case SubraceName.WARFORGED_JUGGERNAUT_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(Language.COMMON,),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=2,
                    dexterity=0,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Iron Fists",
                    "Powerful Build",
                ),
            )
        case SubraceName.WARFORGED_SKIRMISHER_UNEARTHEDARCANA:
            return Subrace(
                speed=30,
                dark_vision_range=0,
                languages=(Language.COMMON,),
                obligatory_skills=(),
                skills_to_choose_from=(),
                n_skills=0,
                tool_proficiencies=(),
                additional_feat=False,
                statistics=RaceStatistics(
                    strength=0,
                    dexterity=2,
                    constitution=1,
                    intelligence=0,
                    wisdom=0,
                    charisma=0,
                    any_of_your_choice=0,
                ),
                other_active_abilities=(
                    "Swift",
                    "Light Step",
                ),
            )
        case _ as never:
            assert_never(never)
