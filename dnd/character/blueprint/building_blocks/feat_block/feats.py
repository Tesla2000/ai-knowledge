from __future__ import annotations

from abc import abstractmethod
from typing import Literal

from dnd.character.blueprint.building_blocks.abstract_feat_block import (
    AbstractFeatBlock,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.sentinels import (
    AnyClassLevel,
    AnySorcererLevel,
    AnyStatChoices,
    AnyWizardLevel,
    MaybeCharacterData,
    MaybeHealth,
    MaybeRace,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.character.feature.feats import FeatName
from dnd.character.health_modifier import ToughHealthModifier
from dnd.character.stats import Stats


class SimpleFeatBlock(AbstractFeatBlock):
    """Base for feats that only add themselves to the feats list (no extra choices)."""

    @abstractmethod
    def _feat_name(self) -> FeatName: ...

    def apply[
        _RK_: MaybeRace,
        _HeK_: MaybeHealth,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
        _BAK_: AnyClassLevel,
        _ROK_: AnyClassLevel,
        _CLK_: AnyClassLevel,
        _DRK_: AnyClassLevel,
        _PAK_: AnyClassLevel,
        _RAK_: AnyClassLevel,
        _MOK_: AnyClassLevel,
        _BDK_: AnyClassLevel,
        _WAK_: AnyClassLevel,
        _ARK_: AnyClassLevel,
        _CDK_: MaybeCharacterData,
    ](
        self,
        blueprint: Blueprint[
            _RK_,
            Stats,
            _HeK_,
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            _BAK_,
            _ROK_,
            _CLK_,
            _DRK_,
            _PAK_,
            _RAK_,
            _MOK_,
            _BDK_,
            _WAK_,
            _ARK_,
            _CDK_,
        ],
    ) -> Blueprint[
        _RK_,
        Stats,
        _HeK_,
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        _BAK_,
        _ROK_,
        _CLK_,
        _DRK_,
        _PAK_,
        _RAK_,
        _MOK_,
        _BDK_,
        _WAK_,
        _ARK_,
        _CDK_,
    ]:
        # TODO: implement feat-specific choices and effects
        return blueprint.model_copy(
            update={"feats": blueprint.feats + (self._feat_name(),)}
        )


class AberrantDragonmarkFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.ABERRANT_DRAGONMARK_FEAT_BLOCK] = (
        BuildingBlockType.ABERRANT_DRAGONMARK_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.ABERRANT_DRAGONMARK


class ActorFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.ACTOR_FEAT_BLOCK] = (
        BuildingBlockType.ACTOR_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.ACTOR


class AlertFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.ALERT_FEAT_BLOCK] = (
        BuildingBlockType.ALERT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.ALERT


class ArtificerInitiateFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.ARTIFICER_INITIATE_FEAT_BLOCK] = (
        BuildingBlockType.ARTIFICER_INITIATE_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.ARTIFICER_INITIATE


class AthleteFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.ATHLETE_FEAT_BLOCK] = (
        BuildingBlockType.ATHLETE_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.ATHLETE


class CartomancerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.CARTOMANCER_FEAT_BLOCK] = (
        BuildingBlockType.CARTOMANCER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.CARTOMANCER


class ChargerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.CHARGER_FEAT_BLOCK] = (
        BuildingBlockType.CHARGER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.CHARGER


class ChefFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.CHEF_FEAT_BLOCK] = BuildingBlockType.CHEF_FEAT_BLOCK

    def _feat_name(self) -> FeatName:
        return FeatName.CHEF


class CrossbowExpertFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.CROSSBOW_EXPERT_FEAT_BLOCK] = (
        BuildingBlockType.CROSSBOW_EXPERT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.CROSSBOW_EXPERT


class CrusherFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.CRUSHER_FEAT_BLOCK] = (
        BuildingBlockType.CRUSHER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.CRUSHER


class DefensiveDuelistFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.DEFENSIVE_DUELIST_FEAT_BLOCK] = (
        BuildingBlockType.DEFENSIVE_DUELIST_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.DEFENSIVE_DUELIST


class DualWielderFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.DUAL_WIELDER_FEAT_BLOCK] = (
        BuildingBlockType.DUAL_WIELDER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.DUAL_WIELDER


class DungeonDelverFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.DUNGEON_DELVER_FEAT_BLOCK] = (
        BuildingBlockType.DUNGEON_DELVER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.DUNGEON_DELVER


class DurableFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.DURABLE_FEAT_BLOCK] = (
        BuildingBlockType.DURABLE_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.DURABLE


class EldritchAdeptFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.ELDRITCH_ADEPT_FEAT_BLOCK] = (
        BuildingBlockType.ELDRITCH_ADEPT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.ELDRITCH_ADEPT


class ElementalAdeptFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.ELEMENTAL_ADEPT_FEAT_BLOCK] = (
        BuildingBlockType.ELEMENTAL_ADEPT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.ELEMENTAL_ADEPT


class EmberOfTheFireGiantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.EMBER_OF_THE_FIRE_GIANT_FEAT_BLOCK] = (
        BuildingBlockType.EMBER_OF_THE_FIRE_GIANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.EMBER_OF_THE_FIRE_GIANT


class FeyTouchedFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.FEY_TOUCHED_FEAT_BLOCK] = (
        BuildingBlockType.FEY_TOUCHED_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.FEY_TOUCHED


class FightingInitiateFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.FIGHTING_INITIATE_FEAT_BLOCK] = (
        BuildingBlockType.FIGHTING_INITIATE_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.FIGHTING_INITIATE


class FuryOfTheFrostGiantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.FURY_OF_THE_FROST_GIANT_FEAT_BLOCK] = (
        BuildingBlockType.FURY_OF_THE_FROST_GIANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.FURY_OF_THE_FROST_GIANT


class GiftOfTheChromaticDragonFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.GIFT_OF_THE_CHROMATIC_DRAGON_FEAT_BLOCK] = (
        BuildingBlockType.GIFT_OF_THE_CHROMATIC_DRAGON_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.GIFT_OF_THE_CHROMATIC_DRAGON


class GiftOfTheGemDragonFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.GIFT_OF_THE_GEM_DRAGON_FEAT_BLOCK] = (
        BuildingBlockType.GIFT_OF_THE_GEM_DRAGON_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.GIFT_OF_THE_GEM_DRAGON


class GiftOfTheMetallicDragonFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.GIFT_OF_THE_METALLIC_DRAGON_FEAT_BLOCK] = (
        BuildingBlockType.GIFT_OF_THE_METALLIC_DRAGON_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.GIFT_OF_THE_METALLIC_DRAGON


class GrapplerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.GRAPPLER_FEAT_BLOCK] = (
        BuildingBlockType.GRAPPLER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.GRAPPLER


class GreatWeaponMasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.GREAT_WEAPON_MASTER_FEAT_BLOCK] = (
        BuildingBlockType.GREAT_WEAPON_MASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.GREAT_WEAPON_MASTER


class GuileOfTheCloudGiantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.GUILE_OF_THE_CLOUD_GIANT_FEAT_BLOCK] = (
        BuildingBlockType.GUILE_OF_THE_CLOUD_GIANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.GUILE_OF_THE_CLOUD_GIANT


class GunnerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.GUNNER_FEAT_BLOCK] = (
        BuildingBlockType.GUNNER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.GUNNER


class HealerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.HEALER_FEAT_BLOCK] = (
        BuildingBlockType.HEALER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.HEALER


class HeavilyArmoredFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.HEAVILY_ARMORED_FEAT_BLOCK] = (
        BuildingBlockType.HEAVILY_ARMORED_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.HEAVILY_ARMORED


class HeavyArmorMasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.HEAVY_ARMOR_MASTER_FEAT_BLOCK] = (
        BuildingBlockType.HEAVY_ARMOR_MASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.HEAVY_ARMOR_MASTER


class InspiringLeaderFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.INSPIRING_LEADER_FEAT_BLOCK] = (
        BuildingBlockType.INSPIRING_LEADER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.INSPIRING_LEADER


class KeenMindFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.KEEN_MIND_FEAT_BLOCK] = (
        BuildingBlockType.KEEN_MIND_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.KEEN_MIND


class KeennessOfTheStoneGiantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.KEENNESS_OF_THE_STONE_GIANT_FEAT_BLOCK] = (
        BuildingBlockType.KEENNESS_OF_THE_STONE_GIANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.KEENNESS_OF_THE_STONE_GIANT


class LightlyArmoredFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.LIGHTLY_ARMORED_FEAT_BLOCK] = (
        BuildingBlockType.LIGHTLY_ARMORED_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.LIGHTLY_ARMORED


class LinguistFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.LINGUIST_FEAT_BLOCK] = (
        BuildingBlockType.LINGUIST_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.LINGUIST


class LuckyFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.LUCKY_FEAT_BLOCK] = (
        BuildingBlockType.LUCKY_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.LUCKY


class MageSlayerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.MAGE_SLAYER_FEAT_BLOCK] = (
        BuildingBlockType.MAGE_SLAYER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.MAGE_SLAYER


class MagicInitiateFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.MAGIC_INITIATE_FEAT_BLOCK] = (
        BuildingBlockType.MAGIC_INITIATE_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.MAGIC_INITIATE


class MartialAdeptFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.MARTIAL_ADEPT_FEAT_BLOCK] = (
        BuildingBlockType.MARTIAL_ADEPT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.MARTIAL_ADEPT


class MediumArmorMasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.MEDIUM_ARMOR_MASTER_FEAT_BLOCK] = (
        BuildingBlockType.MEDIUM_ARMOR_MASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.MEDIUM_ARMOR_MASTER


class MetamagicAdeptFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.METAMAGIC_ADEPT_FEAT_BLOCK] = (
        BuildingBlockType.METAMAGIC_ADEPT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.METAMAGIC_ADEPT


class MobileFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.MOBILE_FEAT_BLOCK] = (
        BuildingBlockType.MOBILE_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.MOBILE


class ModeratelyArmoredFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.MODERATELY_ARMORED_FEAT_BLOCK] = (
        BuildingBlockType.MODERATELY_ARMORED_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.MODERATELY_ARMORED


class MountedCombatantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.MOUNTED_COMBATANT_FEAT_BLOCK] = (
        BuildingBlockType.MOUNTED_COMBATANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.MOUNTED_COMBATANT


class ObservantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.OBSERVANT_FEAT_BLOCK] = (
        BuildingBlockType.OBSERVANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.OBSERVANT


class PiercerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.PIERCER_FEAT_BLOCK] = (
        BuildingBlockType.PIERCER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.PIERCER


class PoisonerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.POISONER_FEAT_BLOCK] = (
        BuildingBlockType.POISONER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.POISONER


class PolearmMasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.POLEARM_MASTER_FEAT_BLOCK] = (
        BuildingBlockType.POLEARM_MASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.POLEARM_MASTER


class ResilientFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.RESILIENT_FEAT_BLOCK] = (
        BuildingBlockType.RESILIENT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.RESILIENT


class RitualCasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.RITUAL_CASTER_FEAT_BLOCK] = (
        BuildingBlockType.RITUAL_CASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.RITUAL_CASTER


class RuneShaperFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.RUNE_SHAPER_FEAT_BLOCK] = (
        BuildingBlockType.RUNE_SHAPER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.RUNE_SHAPER


class SavageAttackerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SAVAGE_ATTACKER_FEAT_BLOCK] = (
        BuildingBlockType.SAVAGE_ATTACKER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SAVAGE_ATTACKER


class SentinelFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SENTINEL_FEAT_BLOCK] = (
        BuildingBlockType.SENTINEL_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SENTINEL


class ShadowTouchedFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SHADOW_TOUCHED_FEAT_BLOCK] = (
        BuildingBlockType.SHADOW_TOUCHED_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SHADOW_TOUCHED


class SharpshooterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SHARPSHOOTER_FEAT_BLOCK] = (
        BuildingBlockType.SHARPSHOOTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SHARPSHOOTER


class ShieldMasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SHIELD_MASTER_FEAT_BLOCK] = (
        BuildingBlockType.SHIELD_MASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SHIELD_MASTER


class SkillExpertFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SKILL_EXPERT_FEAT_BLOCK] = (
        BuildingBlockType.SKILL_EXPERT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SKILL_EXPERT


class SkilledFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SKILLED_FEAT_BLOCK] = (
        BuildingBlockType.SKILLED_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SKILLED


class SkulkerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SKULKER_FEAT_BLOCK] = (
        BuildingBlockType.SKULKER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SKULKER


class SlasherFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SLASHER_FEAT_BLOCK] = (
        BuildingBlockType.SLASHER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SLASHER


class SoulOfTheStormGiantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SOUL_OF_THE_STORM_GIANT_FEAT_BLOCK] = (
        BuildingBlockType.SOUL_OF_THE_STORM_GIANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SOUL_OF_THE_STORM_GIANT


class SpellSniperFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.SPELL_SNIPER_FEAT_BLOCK] = (
        BuildingBlockType.SPELL_SNIPER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.SPELL_SNIPER


class StrikeOfTheGiantsFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.STRIKE_OF_THE_GIANTS_FEAT_BLOCK] = (
        BuildingBlockType.STRIKE_OF_THE_GIANTS_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.STRIKE_OF_THE_GIANTS


class TavernBrawlerFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.TAVERN_BRAWLER_FEAT_BLOCK] = (
        BuildingBlockType.TAVERN_BRAWLER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.TAVERN_BRAWLER


class TelekineticFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.TELEKINETIC_FEAT_BLOCK] = (
        BuildingBlockType.TELEKINETIC_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.TELEKINETIC


class TelepathicFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.TELEPATHIC_FEAT_BLOCK] = (
        BuildingBlockType.TELEPATHIC_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.TELEPATHIC


class ToughFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.TOUGH_FEAT_BLOCK] = (
        BuildingBlockType.TOUGH_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.TOUGH

    def apply[
        _RK_: MaybeRace,
        _HeK_: MaybeHealth,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
        _BAK_: AnyClassLevel,
        _ROK_: AnyClassLevel,
        _CLK_: AnyClassLevel,
        _DRK_: AnyClassLevel,
        _PAK_: AnyClassLevel,
        _RAK_: AnyClassLevel,
        _MOK_: AnyClassLevel,
        _BDK_: AnyClassLevel,
        _WAK_: AnyClassLevel,
        _ARK_: AnyClassLevel,
        _CDK_: MaybeCharacterData,
    ](
        self,
        blueprint: Blueprint[
            _RK_,
            Stats,
            _HeK_,
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            _BAK_,
            _ROK_,
            _CLK_,
            _DRK_,
            _PAK_,
            _RAK_,
            _MOK_,
            _BDK_,
            _WAK_,
            _ARK_,
            _CDK_,
        ],
    ) -> Blueprint[
        _RK_,
        Stats,
        _HeK_,
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        _BAK_,
        _ROK_,
        _CLK_,
        _DRK_,
        _PAK_,
        _RAK_,
        _MOK_,
        _BDK_,
        _WAK_,
        _ARK_,
        _CDK_,
    ]:
        result = super().apply(blueprint)
        return result.model_copy(
            update={
                "health_modifiers": (
                    *result.health_modifiers,
                    ToughHealthModifier(),
                )
            }
        )


class VigorOfTheHillGiantFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.VIGOR_OF_THE_HILL_GIANT_FEAT_BLOCK] = (
        BuildingBlockType.VIGOR_OF_THE_HILL_GIANT_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.VIGOR_OF_THE_HILL_GIANT


class WarCasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.WAR_CASTER_FEAT_BLOCK] = (
        BuildingBlockType.WAR_CASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.WAR_CASTER


class WeaponMasterFeatBlock(SimpleFeatBlock):
    type: Literal[BuildingBlockType.WEAPON_MASTER_FEAT_BLOCK] = (
        BuildingBlockType.WEAPON_MASTER_FEAT_BLOCK
    )

    def _feat_name(self) -> FeatName:
        return FeatName.WEAPON_MASTER
