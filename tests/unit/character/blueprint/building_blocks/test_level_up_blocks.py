from typing import Any

import pytest

from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    HealthIncreaseAverage,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    SorcererRandomSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_3 import WizardLevel3
from dnd.character.blueprint.building_blocks.level_up.wizard.level_4 import WizardLevel4
from dnd.character.blueprint.building_blocks.level_up.wizard.level_5 import WizardLevel5
from dnd.character.blueprint.building_blocks.level_up.wizard.level_7 import WizardLevel7
from dnd.character.blueprint.building_blocks.level_up.wizard.level_8 import WizardLevel8
from dnd.character.blueprint.building_blocks.level_up.wizard.level_9 import WizardLevel9
from dnd.character.blueprint.building_blocks.level_up.wizard.level_11 import (
    WizardLevel11,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_12 import (
    WizardLevel12,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_13 import (
    WizardLevel13,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_15 import (
    WizardLevel15,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_16 import (
    WizardLevel16,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_17 import (
    WizardLevel17,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_18 import (
    WizardLevel18,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_19 import (
    WizardLevel19,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.level_20 import (
    WizardLevel20,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_2 import (
    WizardLevel2Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_6 import (
    WizardLevel6Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_10 import (
    WizardLevel10Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.abjuration.level_14 import (
    WizardLevel14Abjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_2 import (
    WizardLevel2Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_6 import (
    WizardLevel6Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_10 import (
    WizardLevel10Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.bladesinging.level_14 import (
    WizardLevel14Bladesinging,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_2 import (
    WizardLevel2Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_6 import (
    WizardLevel6Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_10 import (
    WizardLevel10Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.chronurgy.level_14 import (
    WizardLevel14Chronurgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_2 import (
    WizardLevel2Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_6 import (
    WizardLevel6Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_10 import (
    WizardLevel10Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.conjuration.level_14 import (
    WizardLevel14Conjuration,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_2 import (
    WizardLevel2Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_6 import (
    WizardLevel6Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_10 import (
    WizardLevel10Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.divination.level_14 import (
    WizardLevel14Divination,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_2 import (
    WizardLevel2Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_6 import (
    WizardLevel6Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_10 import (
    WizardLevel10Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.enchantment.level_14 import (
    WizardLevel14Enchantment,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.evocation.level_6 import (
    WizardLevel6Evocation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.evocation.level_10 import (
    WizardLevel10Evocation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.evocation.level_14 import (
    WizardLevel14Evocation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_2 import (
    WizardLevel2Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_6 import (
    WizardLevel6Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_10 import (
    WizardLevel10Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.graviturgy.level_14 import (
    WizardLevel14Graviturgy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_2 import (
    WizardLevel2Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_6 import (
    WizardLevel6Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_10 import (
    WizardLevel10Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.illusion.level_14 import (
    WizardLevel14Illusion,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_2 import (
    WizardLevel2Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_6 import (
    WizardLevel6Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_10 import (
    WizardLevel10Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.necromancy.level_14 import (
    WizardLevel14Necromancy,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_2 import (
    WizardLevel2Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_6 import (
    WizardLevel6Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_10 import (
    WizardLevel10Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.scribes.level_14 import (
    WizardLevel14Scribes,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_2 import (
    WizardLevel2Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_6 import (
    WizardLevel6Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_10 import (
    WizardLevel10Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.transmutation.level_14 import (
    WizardLevel14Transmutation,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_2 import (
    WizardLevel2WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_6 import (
    WizardLevel6WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_10 import (
    WizardLevel10WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.wizard.war_magic.level_14 import (
    WizardLevel14WarMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_2 import (
    SorcererLevel2,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_3 import (
    SorcererLevel3,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_4 import (
    SorcererLevel4,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_5 import (
    SorcererLevel5,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_7 import (
    SorcererLevel7,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_8 import (
    SorcererLevel8,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_9 import (
    SorcererLevel9,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_10 import (
    SorcererLevel10,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_11 import (
    SorcererLevel11,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_12 import (
    SorcererLevel12,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_13 import (
    SorcererLevel13,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_15 import (
    SorcererLevel15,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_16 import (
    SorcererLevel16,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_17 import (
    SorcererLevel17,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_19 import (
    SorcererLevel19,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.level_20 import (
    SorcererLevel20,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_1 import (
    SorcererLevel1AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_6 import (
    SorcererLevel6AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_14 import (
    SorcererLevel14AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.aberrant_mind.level_18 import (
    SorcererLevel18AberrantMind,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_1 import (
    SorcererLevel1ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_6 import (
    SorcererLevel6ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_14 import (
    SorcererLevel14ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.clockwork_soul.level_18 import (
    SorcererLevel18ClockworkSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_1 import (
    SorcererLevel1DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_6 import (
    SorcererLevel6DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_14 import (
    SorcererLevel14DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.divine_soul.level_18 import (
    SorcererLevel18DivineSoul,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_1 import (
    SorcererLevel1DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_6 import (
    SorcererLevel6DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_14 import (
    SorcererLevel14DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.draconic_bloodline.level_18 import (
    SorcererLevel18DraconicBloodline,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_1 import (
    SorcererLevel1LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_6 import (
    SorcererLevel6LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_14 import (
    SorcererLevel14LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.lunar_sorcery.level_18 import (
    SorcererLevel18LunarSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_1 import (
    SorcererLevel1ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_6 import (
    SorcererLevel6ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_14 import (
    SorcererLevel14ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.shadow_magic.level_18 import (
    SorcererLevel18ShadowMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_1 import (
    SorcererLevel1StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_6 import (
    SorcererLevel6StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_14 import (
    SorcererLevel14StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.storm_sorcery.level_18 import (
    SorcererLevel18StormSorcery,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_1 import (
    SorcererLevel1WildMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_6 import (
    SorcererLevel6WildMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_14 import (
    SorcererLevel14WildMagic,
)
from dnd.character.blueprint.building_blocks.level_up.sorcerer.wild_magic.level_18 import (
    SorcererLevel18WildMagic,
)
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard.base import WizardBlueprint
from dnd.character.blueprint.states.wizard.level18 import WizardLevel18Blueprint
from dnd.character.race.race import Race
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import Class
from dnd.character.blueprint.states.wizard.level20 import WizardLevel20Blueprint

_WIZ_HEALTH = HealthIncreaseAverage(class_=Class.WIZARD)
_WIZ_SPELLS = WizardRandomSpellAssigner()
_SORC_HEALTH = HealthIncreaseAverage(class_=Class.SORCERER)
_SORC_SPELLS = SorcererRandomSpellAssigner()

_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=16,
    wisdom=12,
    charisma=8,
)
_WIZ_BP = WizardBlueprint(
    race=Race.HUMAN,
    stats=_STATS,
    health_base=6,
    spell_slots=FULL_CASTER_SPELL_SLOTS[16],
    caster_level=17,
)
_WIZ_L18_BP = WizardLevel18Blueprint(
    race=Race.HUMAN,
    stats=_STATS,
    health_base=6,
    spell_slots=FULL_CASTER_SPELL_SLOTS[17],
    caster_level=18,
)
_WIZ_L19_BP = WizardLevel18Blueprint(
    race=Race.HUMAN,
    stats=_STATS,
    health_base=6,
    spell_slots=FULL_CASTER_SPELL_SLOTS[18],
    caster_level=19,
)
_SORC_BP = SorcererBlueprint(
    race=Race.HUMAN,
    stats=_STATS,
    health_base=6,
    spell_slots=FULL_CASTER_SPELL_SLOTS[18],
    caster_level=19,
)
_SORC_INPUT_BP = Blueprint(race=Race.HUMAN, stats=_STATS, health_base=6)


@pytest.mark.unit
@pytest.mark.parametrize(
    "block",
    [
        WizardLevel3(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel4(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel5(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel7(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel8(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel9(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel11(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel12(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel13(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel15(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel16(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel17(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
    ],
)
def test_wizard_shared_level_apply(block: Any) -> None:
    result = block.apply(_WIZ_BP)
    assert result is not None


@pytest.mark.unit
def test_wizard_level18_apply() -> None:
    block = WizardLevel18(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS)
    result = block.apply(_WIZ_BP)
    assert result is not None
    assert isinstance(result, WizardLevel18Blueprint)
    assert result.spell_slots == FULL_CASTER_SPELL_SLOTS[17]


@pytest.mark.unit
def test_wizard_level19_apply() -> None:
    block = WizardLevel19(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS)
    result = block.apply(_WIZ_L18_BP)
    assert result is not None
    assert isinstance(result, WizardLevel18Blueprint)
    assert result.spell_slots == FULL_CASTER_SPELL_SLOTS[18]


@pytest.mark.unit
def test_wizard_level20_apply() -> None:
    block = WizardLevel20(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS)
    result = block.apply(_WIZ_L19_BP)
    assert result is not None
    assert isinstance(result, WizardLevel20Blueprint)
    assert result.spell_slots == FULL_CASTER_SPELL_SLOTS[19]


@pytest.mark.unit
@pytest.mark.parametrize(
    "block",
    [
        WizardLevel2Abjuration(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel2Bladesinging(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel2Chronurgy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel2Conjuration(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel2Divination(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel2Enchantment(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel2Graviturgy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel2Illusion(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel2Necromancy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel2Scribes(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel2Transmutation(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel2WarMagic(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
    ],
)
def test_wizard_subclass_level2_apply(block: Any) -> None:
    result = block.apply(_WIZ_BP)
    assert result is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    "block",
    [
        WizardLevel6Abjuration(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Abjuration(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Abjuration(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6Bladesinging(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel10Bladesinging(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Bladesinging(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6Chronurgy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Chronurgy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel14Chronurgy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel6Conjuration(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel10Conjuration(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Conjuration(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6Divination(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Divination(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Divination(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6Enchantment(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel10Enchantment(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Enchantment(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6Evocation(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Evocation(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel14Evocation(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel6Graviturgy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Graviturgy(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Graviturgy(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6Illusion(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Illusion(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel14Illusion(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel6Necromancy(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Necromancy(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Necromancy(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6Scribes(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10Scribes(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel14Scribes(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel6Transmutation(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel10Transmutation(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel14Transmutation(
            health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS
        ),
        WizardLevel6WarMagic(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel10WarMagic(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
        WizardLevel14WarMagic(health_increase=_WIZ_HEALTH, spell_assigner=_WIZ_SPELLS),
    ],
)
def test_wizard_subclass_feature_level_apply(block: Any) -> None:
    result = block.apply(_WIZ_BP)
    assert result is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    "block",
    [
        SorcererLevel1AberrantMind(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel1ClockworkSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel1DivineSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel1DraconicBloodline(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel1LunarSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel1ShadowMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel1StormSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel1WildMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
    ],
)
def test_sorcerer_level1_subclass_apply(block: Any) -> None:
    result = block.apply(_SORC_INPUT_BP)
    assert result is not None
    assert isinstance(result, SorcererBlueprint)


@pytest.mark.unit
@pytest.mark.parametrize(
    "block",
    [
        SorcererLevel2(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel3(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel4(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel5(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel7(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel8(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel9(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel10(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel11(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel12(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel13(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel15(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel16(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel17(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel19(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
        SorcererLevel20(health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS),
    ],
)
def test_sorcerer_shared_level_apply(block: Any) -> None:
    result = block.apply(_SORC_BP)
    assert result is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    "block",
    [
        SorcererLevel6AberrantMind(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14AberrantMind(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18AberrantMind(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel6ClockworkSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14ClockworkSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18ClockworkSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel6DivineSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14DivineSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18DivineSoul(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel6DraconicBloodline(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14DraconicBloodline(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18DraconicBloodline(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel6LunarSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14LunarSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18LunarSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel6ShadowMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14ShadowMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18ShadowMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel6StormSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14StormSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18StormSorcery(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel6WildMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel14WildMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
        SorcererLevel18WildMagic(
            health_increase=_SORC_HEALTH, spell_assigner=_SORC_SPELLS
        ),
    ],
)
def test_sorcerer_subclass_feature_level_apply(block: Any) -> None:
    result = block.apply(_SORC_BP)
    assert result is not None


@pytest.mark.unit
class TestSpellAssignerEarlyReturn:
    def test_wizard_spell_assigner_skips_when_no_wizard_levels(self) -> None:
        assigner = WizardRandomSpellAssigner()
        state = Blueprint()
        result = assigner.apply(state)
        assert result is state

    def test_sorcerer_spell_assigner_skips_when_no_sorcerer_levels(self) -> None:
        assigner = SorcererRandomSpellAssigner()
        result = assigner.apply(_SORC_BP)
        assert result is _SORC_BP
