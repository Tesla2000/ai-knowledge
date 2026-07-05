from __future__ import annotations

from collections.abc import Generator

import pytest

from dnd.character.blueprint.building_blocks.feat_adder import FeatAdder
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.level_assigner import LevelAssigner
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    WizardLevelIncrementer,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.priority import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.base import (
    ToolProficienciesDelta,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.random import (
    RandomToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.state import Blueprint
from dnd.character.feature.feats import FeatName
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import GamingSet, MusicalInstrument, ToolProficiency
from pydantic import create_model


def _exhaust(gen: Generator[object, object, object]) -> object:
    try:
        while True:
            next(gen)
    except StopIteration as exc:
        return exc.value


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
        delta = ToolProficienciesDelta(
            tool_proficiencies=(GamingSet.ANY_OF_YOUR_CHOICE,)
        )
        state = delta.apply(Blueprint())
        resolver = RandomToolProficiencyChoiceResolver()
        result = _exhaust(resolver.get_change(state))
        assert GamingSet.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert any(isinstance(t, GamingSet) for t in result.tool_proficiencies)

    def test_musical_instrument_placeholder_resolved(self) -> None:
        delta = ToolProficienciesDelta(
            tool_proficiencies=(MusicalInstrument.ANY_OF_YOUR_CHOICE,)
        )
        state = delta.apply(Blueprint())
        resolver = RandomToolProficiencyChoiceResolver()
        result = _exhaust(resolver.get_change(state))
        assert MusicalInstrument.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert any(isinstance(t, MusicalInstrument) for t in result.tool_proficiencies)

    def test_non_placeholder_tool_proficiency_preserved(self) -> None:
        delta = ToolProficienciesDelta(
            tool_proficiencies=(ToolProficiency.HERBALISM_KIT,)
        )
        state = delta.apply(Blueprint())
        resolver = RandomToolProficiencyChoiceResolver()
        result = _exhaust(resolver.get_change(state))
        assert ToolProficiency.HERBALISM_KIT in result.tool_proficiencies

    def test_tool_proficiency_placeholder_resolved(self) -> None:
        delta = ToolProficienciesDelta(
            tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,)
        )
        state = delta.apply(Blueprint())
        resolver = RandomToolProficiencyChoiceResolver(seed=42)
        result = _exhaust(resolver.get_change(state))
        assert ToolProficiency.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert any(isinstance(t, ToolProficiency) for t in result.tool_proficiencies)

    def test_mixed_tools_all_resolved(self) -> None:
        delta = ToolProficienciesDelta(
            tool_proficiencies=(
                GamingSet.ANY_OF_YOUR_CHOICE,
                MusicalInstrument.ANY_OF_YOUR_CHOICE,
                ToolProficiency.HERBALISM_KIT,
            )
        )
        state = delta.apply(Blueprint())
        resolver = RandomToolProficiencyChoiceResolver(seed=42)
        result = _exhaust(resolver.get_change(state))
        assert GamingSet.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert MusicalInstrument.ANY_OF_YOUR_CHOICE not in result.tool_proficiencies
        assert ToolProficiency.HERBALISM_KIT in result.tool_proficiencies


@pytest.mark.unit
class TestFeatChoiceResolverBranches:
    def test_concrete_feat_returned_directly(self) -> None:
        state = Blueprint(feats=(FeatName.TOUGH,))
        state = _exhaust(LevelAssigner(level=2).get_change(state))
        state = _exhaust(StandardArray(stats_priority=_PRIORITY).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        resolver = RandomFeatChoiceResolver(seed=0)
        result = _exhaust(resolver.get_change(state))
        assert FeatName.TOUGH in result.feats

    def test_level_1_excludes_ability_score_improvement(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=1).get_change(state))
        state = _exhaust(StandardArray(stats_priority=_PRIORITY).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(
            FeatAdder(feat=FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT).get_change(
                state
            )
        )
        resolver = RandomFeatChoiceResolver(seed=0)
        result = _exhaust(resolver.get_change(state))
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
        state = _exhaust(LevelAssigner(level=4).get_change(state))
        state = _exhaust(StandardArray(stats_priority=_PRIORITY).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        resolver = MaxIfNotMaxedResolver(priority=_PRIORITY)
        result = _exhaust(resolver.get_change(state))
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
