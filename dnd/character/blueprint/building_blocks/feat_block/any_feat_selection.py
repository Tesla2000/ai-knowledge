from __future__ import annotations

from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.abstract_feat_block import (
    AbstractFeatBlock,
)
from dnd.character.blueprint.building_blocks.feat_block.ability_score_improvement import (
    AbilityScoreImprovementFeatBlock,
)
from dnd.character.blueprint.building_blocks.feat_block import feats as _feat_blocks
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    AnyFeatChoiceResolver,
    MaxFirstResolver,
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
from dnd.character.stats import Stats


def _feat_block_for(feat: FeatName) -> AbstractFeatBlock:  # noqa: PLR0911
    match feat:
        case FeatName.ABILITY_SCORE_IMPROVEMENT:
            return AbilityScoreImprovementFeatBlock()
        case FeatName.ABERRANT_DRAGONMARK:
            return _feat_blocks.AberrantDragonmarkFeatBlock()
        case FeatName.ACTOR:
            return _feat_blocks.ActorFeatBlock()
        case FeatName.ALERT:
            return _feat_blocks.AlertFeatBlock()
        case FeatName.ARTIFICER_INITIATE:
            return _feat_blocks.ArtificerInitiateFeatBlock()
        case FeatName.ATHLETE:
            return _feat_blocks.AthleteFeatBlock()
        case FeatName.CARTOMANCER:
            return _feat_blocks.CartomancerFeatBlock()
        case FeatName.CHARGER:
            return _feat_blocks.ChargerFeatBlock()
        case FeatName.CHEF:
            return _feat_blocks.ChefFeatBlock()
        case FeatName.CROSSBOW_EXPERT:
            return _feat_blocks.CrossbowExpertFeatBlock()
        case FeatName.CRUSHER:
            return _feat_blocks.CrusherFeatBlock()
        case FeatName.DEFENSIVE_DUELIST:
            return _feat_blocks.DefensiveDuelistFeatBlock()
        case FeatName.DUAL_WIELDER:
            return _feat_blocks.DualWielderFeatBlock()
        case FeatName.DUNGEON_DELVER:
            return _feat_blocks.DungeonDelverFeatBlock()
        case FeatName.DURABLE:
            return _feat_blocks.DurableFeatBlock()
        case FeatName.ELDRITCH_ADEPT:
            return _feat_blocks.EldritchAdeptFeatBlock()
        case FeatName.ELEMENTAL_ADEPT:
            return _feat_blocks.ElementalAdeptFeatBlock()
        case FeatName.EMBER_OF_THE_FIRE_GIANT:
            return _feat_blocks.EmberOfTheFireGiantFeatBlock()
        case FeatName.FEY_TOUCHED:
            return _feat_blocks.FeyTouchedFeatBlock()
        case FeatName.FIGHTING_INITIATE:
            return _feat_blocks.FightingInitiateFeatBlock()
        case FeatName.FURY_OF_THE_FROST_GIANT:
            return _feat_blocks.FuryOfTheFrostGiantFeatBlock()
        case FeatName.GIFT_OF_THE_CHROMATIC_DRAGON:
            return _feat_blocks.GiftOfTheChromaticDragonFeatBlock()
        case FeatName.GIFT_OF_THE_GEM_DRAGON:
            return _feat_blocks.GiftOfTheGemDragonFeatBlock()
        case FeatName.GIFT_OF_THE_METALLIC_DRAGON:
            return _feat_blocks.GiftOfTheMetallicDragonFeatBlock()
        case FeatName.GRAPPLER:
            return _feat_blocks.GrapplerFeatBlock()
        case FeatName.GREAT_WEAPON_MASTER:
            return _feat_blocks.GreatWeaponMasterFeatBlock()
        case FeatName.GUILE_OF_THE_CLOUD_GIANT:
            return _feat_blocks.GuileOfTheCloudGiantFeatBlock()
        case FeatName.GUNNER:
            return _feat_blocks.GunnerFeatBlock()
        case FeatName.HEALER:
            return _feat_blocks.HealerFeatBlock()
        case FeatName.HEAVILY_ARMORED:
            return _feat_blocks.HeavilyArmoredFeatBlock()
        case FeatName.HEAVY_ARMOR_MASTER:
            return _feat_blocks.HeavyArmorMasterFeatBlock()
        case FeatName.INSPIRING_LEADER:
            return _feat_blocks.InspiringLeaderFeatBlock()
        case FeatName.KEEN_MIND:
            return _feat_blocks.KeenMindFeatBlock()
        case FeatName.KEENNESS_OF_THE_STONE_GIANT:
            return _feat_blocks.KeennessOfTheStoneGiantFeatBlock()
        case FeatName.LIGHTLY_ARMORED:
            return _feat_blocks.LightlyArmoredFeatBlock()
        case FeatName.LINGUIST:
            return _feat_blocks.LinguistFeatBlock()
        case FeatName.LUCKY:
            return _feat_blocks.LuckyFeatBlock()
        case FeatName.MAGE_SLAYER:
            return _feat_blocks.MageSlayerFeatBlock()
        case FeatName.MAGIC_INITIATE:
            return _feat_blocks.MagicInitiateFeatBlock()
        case FeatName.MARTIAL_ADEPT:
            return _feat_blocks.MartialAdeptFeatBlock()
        case FeatName.MEDIUM_ARMOR_MASTER:
            return _feat_blocks.MediumArmorMasterFeatBlock()
        case FeatName.METAMAGIC_ADEPT:
            return _feat_blocks.MetamagicAdeptFeatBlock()
        case FeatName.MOBILE:
            return _feat_blocks.MobileFeatBlock()
        case FeatName.MODERATELY_ARMORED:
            return _feat_blocks.ModeratelyArmoredFeatBlock()
        case FeatName.MOUNTED_COMBATANT:
            return _feat_blocks.MountedCombatantFeatBlock()
        case FeatName.OBSERVANT:
            return _feat_blocks.ObservantFeatBlock()
        case FeatName.PIERCER:
            return _feat_blocks.PiercerFeatBlock()
        case FeatName.POISONER:
            return _feat_blocks.PoisonerFeatBlock()
        case FeatName.POLEARM_MASTER:
            return _feat_blocks.PolearmMasterFeatBlock()
        case FeatName.RESILIENT:
            return _feat_blocks.ResilientFeatBlock()
        case FeatName.RITUAL_CASTER:
            return _feat_blocks.RitualCasterFeatBlock()
        case FeatName.RUNE_SHAPER:
            return _feat_blocks.RuneShaperFeatBlock()
        case FeatName.SAVAGE_ATTACKER:
            return _feat_blocks.SavageAttackerFeatBlock()
        case FeatName.SENTINEL:
            return _feat_blocks.SentinelFeatBlock()
        case FeatName.SHADOW_TOUCHED:
            return _feat_blocks.ShadowTouchedFeatBlock()
        case FeatName.SHARPSHOOTER:
            return _feat_blocks.SharpshooterFeatBlock()
        case FeatName.SHIELD_MASTER:
            return _feat_blocks.ShieldMasterFeatBlock()
        case FeatName.SKILL_EXPERT:
            return _feat_blocks.SkillExpertFeatBlock()
        case FeatName.SKILLED:
            return _feat_blocks.SkilledFeatBlock()
        case FeatName.SKULKER:
            return _feat_blocks.SkulkerFeatBlock()
        case FeatName.SLASHER:
            return _feat_blocks.SlasherFeatBlock()
        case FeatName.SOUL_OF_THE_STORM_GIANT:
            return _feat_blocks.SoulOfTheStormGiantFeatBlock()
        case FeatName.SPELL_SNIPER:
            return _feat_blocks.SpellSniperFeatBlock()
        case FeatName.STRIKE_OF_THE_GIANTS:
            return _feat_blocks.StrikeOfTheGiantsFeatBlock()
        case FeatName.TAVERN_BRAWLER:
            return _feat_blocks.TavernBrawlerFeatBlock()
        case FeatName.TELEKINETIC:
            return _feat_blocks.TelekineticFeatBlock()
        case FeatName.TELEPATHIC:
            return _feat_blocks.TelepathicFeatBlock()
        case FeatName.TOUGH:
            return _feat_blocks.ToughFeatBlock()
        case FeatName.VIGOR_OF_THE_HILL_GIANT:
            return _feat_blocks.VigorOfTheHillGiantFeatBlock()
        case FeatName.WAR_CASTER:
            return _feat_blocks.WarCasterFeatBlock()
        case FeatName.WEAPON_MASTER:
            return _feat_blocks.WeaponMasterFeatBlock()
        case _:
            raise ValueError(f"No feat block for {feat}")


class AnyFeatSelectionBlock(AbstractFeatBlock):
    """Picks any feat (including ASI) at apply-time and dispatches to that feat's block.

    Uses feat_resolver to determine which feat to take, then calls apply() on the
    corresponding feat block. Each feat owns its own resolution logic.
    """

    type: Literal[BuildingBlockType.ANY_FEAT_SELECTION_BLOCK] = (
        BuildingBlockType.ANY_FEAT_SELECTION_BLOCK
    )
    feat_resolver: AnyFeatChoiceResolver = Field(default_factory=MaxFirstResolver)

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
        with_placeholder = blueprint.model_copy(
            update={"feats": blueprint.feats + (FeatName.ANY_OF_YOUR_CHOICE,)}
        )
        resolved = self.feat_resolver.apply(with_placeholder)

        if resolved.n_stat_choices > blueprint.n_stat_choices:
            chosen = FeatName.ABILITY_SCORE_IMPROVEMENT
        else:
            original = frozenset(blueprint.feats)
            chosen = next(f for f in resolved.feats if f not in original)

        return _feat_block_for(chosen).apply(blueprint)
