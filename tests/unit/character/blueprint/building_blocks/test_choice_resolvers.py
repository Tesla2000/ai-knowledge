import pytest

from dnd.character.blueprint.building_blocks.metamagic_choice_resolver.random import (
    RandomMetamagicChoiceResolver,
)
from dnd.character.blueprint.building_blocks.signature_spell_choice_resolver.random import (
    RandomSignatureSpellChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feat_adder import FeatAdder
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_assigner import LevelAssigner
from dnd.character.blueprint.building_blocks.stat_choice_resolver.priority import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.random import (
    RandomToolProficiencyChoiceResolver,
)
from dnd.character.class_levels import ClassLevels
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard.level20 import WizardLevel20Blueprint
from dnd.character.race.race import Race
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.spells.spell_slots import ThirdLevel
from dnd.character.spells.spells import Spells
from dnd.choices.abilities.metamagic import MetamagicOption
from dnd.character.feature.feats import FeatName
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import GamingSet, MusicalInstrument, ToolProficiency
from pydantic import create_model


_PRIORITY: StatsPriority = (
    Statistic.STRENGTH,
    Statistic.DEXTERITY,
    Statistic.CONSTITUTION,
    Statistic.INTELLIGENCE,
    Statistic.WISDOM,
    Statistic.CHARISMA,
)


@pytest.mark.unit
class TestToolProficiencyChoiceResolverBranches:
    def test_gaming_set_placeholder_resolved(self) -> None:
        state = Blueprint(tool_proficiencies=(GamingSet.ANY_OF_YOUR_CHOICE,))
        resolver = RandomToolProficiencyChoiceResolver()
        result = resolver.apply(state)
        assert GamingSet.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert any(isinstance(t, GamingSet) for t in result.tool_proficiencies)

    def test_musical_instrument_placeholder_resolved(self) -> None:
        state = Blueprint(tool_proficiencies=(MusicalInstrument.ANY_OF_YOUR_CHOICE,))
        resolver = RandomToolProficiencyChoiceResolver()
        result = resolver.apply(state)
        assert MusicalInstrument.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert any(isinstance(t, MusicalInstrument) for t in result.tool_proficiencies)

    def test_non_placeholder_tool_proficiency_preserved(self) -> None:
        state = Blueprint(tool_proficiencies=(ToolProficiency.HERBALISM_KIT,))
        resolver = RandomToolProficiencyChoiceResolver()
        result = resolver.apply(state)
        assert ToolProficiency.HERBALISM_KIT in result.tool_proficiencies

    def test_tool_proficiency_placeholder_resolved(self) -> None:
        state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
        resolver = RandomToolProficiencyChoiceResolver(seed=42)
        result = resolver.apply(state)
        assert ToolProficiency.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert any(isinstance(t, ToolProficiency) for t in result.tool_proficiencies)

    def test_mixed_tools_all_resolved(self) -> None:
        state = Blueprint(
            tool_proficiencies=(
                GamingSet.ANY_OF_YOUR_CHOICE,
                MusicalInstrument.ANY_OF_YOUR_CHOICE,
                ToolProficiency.HERBALISM_KIT,
            )
        )
        resolver = RandomToolProficiencyChoiceResolver(seed=42)
        result = resolver.apply(state)
        assert GamingSet.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert MusicalInstrument.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert ToolProficiency.HERBALISM_KIT in result.tool_proficiencies


@pytest.mark.unit
class TestFeatChoiceResolverBranches:
    def test_concrete_feat_returned_directly(self) -> None:
        state = Blueprint(feats=(FeatName.TOUGH,))
        state = LevelAssigner(level=2).apply(state)
        state = StandardArray(stats_priority=_PRIORITY).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=2)})
        resolver = RandomFeatChoiceResolver(seed=0)
        result = resolver.apply(state)
        assert FeatName.TOUGH in result.feats

    def test_level_1_excludes_ability_score_improvement(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=1).apply(state)
        state = StandardArray(stats_priority=_PRIORITY).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=1)})
        state = FeatAdder(feat=FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT).apply(
            state
        )
        resolver = RandomFeatChoiceResolver(seed=0)
        result = resolver.apply(state)
        assert FeatName.ABILITY_SCORE_IMPROVEMENT not in result.feats


@pytest.mark.unit
class TestMaxIfNotMaxedResolverASI:
    def test_returns_asi_when_stat_below_cup(self) -> None:
        high_cup = Stats(
            strength=20,
            dexterity=20,
            constitution=20,
            intelligence=20,
            wisdom=20,
            charisma=20,
        )
        state = Blueprint(stats_cup=high_cup)
        state = LevelAssigner(level=4).apply(state)
        state = StandardArray(stats_priority=_PRIORITY).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=4)})
        resolver = MaxIfNotMaxedResolver(priority=_PRIORITY)
        result = resolver.apply(state)
        assert result is not None


@pytest.mark.unit
class TestPriorityStatChoiceResolverBranches:
    def _make_state_with_stats_and_choices(
        self, stats: Stats, n_stat_choices: int
    ) -> object:
        BlueprintWithChoices = create_model(
            "BlueprintWithChoices",
            stats=(Stats, ...),
            n_stat_choices=(int, ...),
            __base__=Blueprint,
        )
        return BlueprintWithChoices(stats=stats, n_stat_choices=n_stat_choices)

    def test_early_return_when_n_stats_is_zero(self) -> None:
        low_stats = Stats(
            strength=8,
            dexterity=8,
            constitution=8,
            intelligence=8,
            wisdom=8,
            charisma=8,
        )
        state = self._make_state_with_stats_and_choices(low_stats, 0)
        resolver = PriorityStatChoiceResolver(priority=_PRIORITY)
        result = resolver.select_stats_to_increase(state)
        assert all(v == 0 for v in result.values())

    def test_odd_stat_gets_plus_one_first(self) -> None:
        odd_stats = Stats(
            strength=9,
            dexterity=9,
            constitution=9,
            intelligence=9,
            wisdom=9,
            charisma=9,
        )
        state = self._make_state_with_stats_and_choices(odd_stats, 2)
        resolver = PriorityStatChoiceResolver(priority=_PRIORITY)
        result = resolver.select_stats_to_increase(state)
        assert sum(result.values()) >= 1


_SORC_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=10,
    wisdom=10,
    charisma=16,
)
_SORC_BP = SorcererBlueprint(
    race=Race.HUMAN,
    stats=_SORC_STATS,
    health_base=6,
    spell_slots=FULL_CASTER_SPELL_SLOTS[0],
    caster_level=1,
)


@pytest.mark.unit
class TestMetamagicChoiceResolver:
    def test_selects_n_options(self) -> None:
        bp = _SORC_BP.model_copy(update={"n_metamagic_choices": 2})
        resolver = RandomMetamagicChoiceResolver(seed=0)
        result = resolver.apply(bp)
        assert len(result.metamagic_options) == 2
        assert result.n_metamagic_choices == 0

    def test_no_duplicates_with_existing(self) -> None:
        bp = _SORC_BP.model_copy(
            update={
                "metamagic_options": (MetamagicOption.CAREFUL,),
                "n_metamagic_choices": 3,
            }
        )
        resolver = RandomMetamagicChoiceResolver(seed=1)
        result = resolver.apply(bp)
        assert MetamagicOption.CAREFUL in result.metamagic_options
        assert len(result.metamagic_options) == 4
        assert len(set(result.metamagic_options)) == 4

    def test_skips_when_no_choices(self) -> None:
        resolver = RandomMetamagicChoiceResolver()
        result = resolver.apply(_SORC_BP)
        assert result.n_metamagic_choices == 0
        assert result.metamagic_options == _SORC_BP.metamagic_options


_WIZ_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=18,
    wisdom=10,
    charisma=10,
)
_WIZ_L20_BP = WizardLevel20Blueprint(
    race=Race.HUMAN,
    stats=_WIZ_STATS,
    health_base=6,
    spell_slots=FULL_CASTER_SPELL_SLOTS[19],
    caster_level=20,
    n_signature_spell_choices=2,
    spells=Spells(
        third_level_spells=(
            ThirdLevel.FIREBALL,
            ThirdLevel.COUNTERSPELL,
            ThirdLevel.HASTE,
        )
    ),
)


@pytest.mark.unit
class TestSignatureSpellChoiceResolver:
    def test_selects_n_spells(self) -> None:
        resolver = RandomSignatureSpellChoiceResolver(seed=0)
        result = resolver.apply(_WIZ_L20_BP)
        assert len(result.signature_spells) == 2
        assert result.n_signature_spell_choices == 0

    def test_no_duplicates_with_existing(self) -> None:
        bp = _WIZ_L20_BP.model_copy(
            update={
                "signature_spells": (ThirdLevel.FIREBALL,),
                "n_signature_spell_choices": 1,
            }
        )
        resolver = RandomSignatureSpellChoiceResolver(seed=1)
        result = resolver.apply(bp)
        assert ThirdLevel.FIREBALL in result.signature_spells
        assert len(set(result.signature_spells)) == len(result.signature_spells)

    def test_skips_when_no_choices(self) -> None:
        bp = _WIZ_L20_BP.model_copy(update={"n_signature_spell_choices": 0})
        resolver = RandomSignatureSpellChoiceResolver()
        result = resolver.apply(bp)
        assert result.n_signature_spell_choices == 0
        assert result.signature_spells == bp.signature_spells
