from __future__ import annotations

import json
from enum import StrEnum
from typing import Self

from dnd.character.feature.feature import Feature
from dnd.config import resource_paths


class FeatName(StrEnum):
    ABERRANT_DRAGONMARK = "Aberrant Dragonmark"
    ACTOR = "Actor"
    ALERT = "Alert"
    ARTIFICER_INITIATE = "Artificer Initiate"
    ATHLETE = "Athlete"
    CARTOMANCER = "Cartomancer"
    CHARGER = "Charger"
    CHEF = "Chef"
    CROSSBOW_EXPERT = "Crossbow Expert"
    CRUSHER = "Crusher"
    DEFENSIVE_DUELIST = "Defensive Duelist"
    DUAL_WIELDER = "Dual Wielder"
    DUNGEON_DELVER = "Dungeon Delver"
    DURABLE = "Durable"
    ELDRITCH_ADEPT = "Eldritch Adept"
    ELEMENTAL_ADEPT = "Elemental Adept"
    EMBER_OF_THE_FIRE_GIANT = "Ember of the Fire Giant"
    FEY_TOUCHED = "Fey Touched"
    FIGHTING_INITIATE = "Fighting Initiate"
    FURY_OF_THE_FROST_GIANT = "Fury of the Frost Giant"
    GIFT_OF_THE_CHROMATIC_DRAGON = "Gift of the Chromatic Dragon"
    GIFT_OF_THE_GEM_DRAGON = "Gift of the Gem Dragon"
    GIFT_OF_THE_METALLIC_DRAGON = "Gift of the Metallic Dragon"
    GRAPPLER = "Grappler"
    GREAT_WEAPON_MASTER = "Great Weapon Master"
    GUILE_OF_THE_CLOUD_GIANT = "Guile of the Cloud Giant"
    GUNNER = "Gunner"
    HEALER = "Healer"
    HEAVILY_ARMORED = "Heavily Armored"
    HEAVY_ARMOR_MASTER = "Heavy Armor Master"
    INSPIRING_LEADER = "Inspiring Leader"
    KEEN_MIND = "Keen Mind"
    KEENNESS_OF_THE_STONE_GIANT = "Keenness of the Stone Giant"
    LIGHTLY_ARMORED = "Lightly Armored"
    LINGUIST = "Linguist"
    LUCKY = "Lucky"
    MAGE_SLAYER = "Mage Slayer"
    MAGIC_INITIATE = "Magic Initiate"
    MARTIAL_ADEPT = "Martial Adept"
    MEDIUM_ARMOR_MASTER = "Medium Armor Master"
    METAMAGIC_ADEPT = "Metamagic Adept"
    MOBILE = "Mobile"
    MODERATELY_ARMORED = "Moderately Armored"
    MOUNTED_COMBATANT = "Mounted Combatant"
    OBSERVANT = "Observant"
    PIERCER = "Piercer"
    POISONER = "Poisoner"
    POLEARM_MASTER = "Polearm Master"
    RESILIENT = "Resilient"
    RITUAL_CASTER = "Ritual Caster"
    RUNE_SHAPER = "Rune Shaper"
    SAVAGE_ATTACKER = "Savage Attacker"
    SENTINEL = "Sentinel"
    SHADOW_TOUCHED = "Shadow Touched"
    SHARPSHOOTER = "Sharpshooter"
    SHIELD_MASTER = "Shield Master"
    SKILL_EXPERT = "Skill Expert"
    SKILLED = "Skilled"
    SKULKER = "Skulker"
    SLASHER = "Slasher"
    SOUL_OF_THE_STORM_GIANT = "Soul of the Storm Giant"
    SPELL_SNIPER = "Spell Sniper"
    STRIKE_OF_THE_GIANTS = "Strike of the Giants"
    TAVERN_BRAWLER = "Tavern Brawler"
    TELEKINETIC = "Telekinetic"
    TELEPATHIC = "Telepathic"
    TOUGH = "Tough"
    VIGOR_OF_THE_HILL_GIANT = "Vigor of the Hill Giant"
    WAR_CASTER = "War Caster"
    WEAPON_MASTER = "Weapon Master"
    ABILITY_SCORE_IMPROVEMENT = "Ability Score Improvement"
    ANY_OF_YOUR_CHOICE = "Any feat of your choice"
    ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT = "Any except ability score improvement"

    @classmethod
    def not_choosables(cls) -> tuple[Self, ...]:
        return cls.ANY_OF_YOUR_CHOICE, cls.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT


def feat_name_to_feat(feat: FeatName) -> Feature:
    return Feature(
        **json.loads(
            resource_paths.feats_root.joinpath(f"{feat.value}.json").read_text()
        )
    )
