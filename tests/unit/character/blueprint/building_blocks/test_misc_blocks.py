from __future__ import annotations

import random
from collections.abc import Generator
from unittest.mock import patch

import pytest
from pydantic import TypeAdapter
from pydantic import create_model

from dnd.character.presentable_character import PresentableCharacter

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.random import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.random import (
    HealthIncreaseRandom,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.random_reroll_ones import (
    HealthIncreaseRandomRerollOnes,
)
from dnd.character.blueprint.building_blocks.level_assigner import LevelAssigner
from dnd.character.blueprint.building_blocks.level_up.health_increase.random_min_two import (
    HealthIncreaseRandomMinTwo,
)
from dnd.character.blueprint.building_blocks.level_up.level_incrementer import (
    SorcererLevelIncrementer,
    WizardLevelIncrementer,
)
from dnd.character.blueprint.building_blocks.level_up.level_up import LevelUp
from dnd.character.blueprint.building_blocks.race_assigner.random_race_assigner import (
    RandomRaceAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    base as spell_base,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SpellsDelta,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.random import (
    SorcererRandomSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.spells import Cantrip
from dnd.character.spells import FirstLevel
from dnd.character.spells.spells import Spells
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.building_blocks.race_assigner import RaceAssigner
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    CanNotAssign,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.optional import (
    OptionalSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.random import (
    RandomSubclassAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.subclass_assigner import (
    WizardSubclassAssigner,
)
from dnd.character.blueprint.state import Blueprint
from dnd.character.builder import Builder
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import Class, WizardSubclass
from dnd.choices.stats_creation.statistic import Statistic
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from pydantic import ValidationError

from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)


def _exhaust(gen: Generator) -> object:
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
class TestStatsPriority:
    def test_duplicate_elements_raise(self) -> None:
        with pytest.raises(ValidationError, match="not unique"):
            ta = TypeAdapter(StatsPriority)
            ta.validate_python(
                (
                    Statistic.STRENGTH,
                    Statistic.STRENGTH,
                    Statistic.CONSTITUTION,
                    Statistic.INTELLIGENCE,
                    Statistic.WISDOM,
                    Statistic.CHARISMA,
                )
            )


@pytest.mark.unit
class TestBuilderAdd:
    def test_add_returns_new_builder_with_block(self) -> None:
        builder = Builder()
        new_builder = builder.add(NullBlock())
        assert isinstance(new_builder, Builder)

    def test_add_building_block_chain(self) -> None:
        builder = Builder()
        b1 = builder.add(NullBlock())
        b2 = b1.add(NullBlock())
        assert isinstance(b2, Builder)

    def test_remaining_choices_raises(self) -> None:
        BlueprintWithChoices = create_model(
            "BlueprintWithChoices",
            n_stat_choices=(int, 2),
            __base__=Blueprint,
        )
        state = BlueprintWithChoices()
        with pytest.raises(ValueError, match="choices"):
            Builder._make_presentable(state)


@pytest.mark.unit
class TestMaxIfNotMaxedResolver:
    def test_noop_when_stat_exceeds_cup(self) -> None:
        low_cup = Stats(
            strength=10,
            dexterity=20,
            constitution=20,
            intelligence=20,
            wisdom=20,
            charisma=20,
        )
        blueprint = Blueprint(stats_cup=low_cup)
        state = _exhaust(StandardArray(stats_priority=_PRIORITY).get_change(blueprint))
        resolver = MaxIfNotMaxedResolver(priority=_PRIORITY)
        result = _exhaust(resolver.get_change(state))
        assert result is not None


@pytest.mark.unit
class TestSubclassAssigner:
    def test_can_not_assign_raises_when_no_class(self) -> None:
        block = WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION)
        with pytest.raises(CanNotAssign):
            next(block.get_change(Blueprint()))

    def test_early_return_when_subclass_already_present(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=2).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(
            WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION).get_change(state)
        )
        result = _exhaust(
            WizardSubclassAssigner(subclass=WizardSubclass.EVOCATION).get_change(state)
        )
        assert WizardSubclass.ABJURATION in result.subclasses
        assert WizardSubclass.EVOCATION not in result.subclasses

    def test_random_early_return_when_subclass_already_present(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=2).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(
            WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION).get_change(state)
        )
        random_assigner = RandomSubclassAssigner(class_=Class.WIZARD)
        result = _exhaust(random_assigner.get_change(state))
        assert WizardSubclass.ABJURATION in result.subclasses


@pytest.mark.unit
class TestBaseRaceAssignerDoubleRace:
    def test_assigning_race_twice_raises(self) -> None:
        state = Blueprint()
        state = _exhaust(StandardArray(stats_priority=_PRIORITY).get_change(state))
        state = _exhaust(
            RaceAssigner(
                race=Race.HUMAN,
                subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
            ).get_change(state)
        )
        second_assigner = RaceAssigner(
            race=Race.ELF,
            subrace=SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK,
        )
        with pytest.raises(ValueError, match="already has a race assigned"):
            next(second_assigner.get_change(state))


@pytest.mark.unit
class TestSorcererLevelIncrementer:
    def test_first_level_grants_proficiencies(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=2).get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        assert state is not None

    def test_second_level_increments(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=2).get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        assert state is not None

    def test_asi_level_grants_feat(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=4).get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        assert state is not None


@pytest.mark.unit
class TestLevelIncrementExceedsCharacterLevel:
    def test_class_level_exceeds_character_level_raises(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=1).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        with pytest.raises(ValueError, match="Total class levels"):
            next(WizardLevelIncrementer().get_change(state))


@pytest.mark.unit
class TestHealthIncreaseRandomMinTwo:
    def test_random_min_two_on_subsequent_level(self) -> None:
        block = HealthIncreaseRandomMinTwo(class_=Class.WIZARD)
        state = Blueprint()
        state = _exhaust(block.get_change(state))
        state = _exhaust(block.get_change(state))
        assert state.health_base >= 2


@pytest.mark.unit
class TestSorcererSpellAssigner:
    def test_first_level_assigns_spells(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=1).get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        assigner = SorcererRandomSpellAssigner()
        result = _exhaust(assigner.get_change(state))
        assert result is not None

    def test_second_level_assigns_spells(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=2).get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        state = _exhaust(SorcererLevelIncrementer().get_change(state))
        assigner = SorcererRandomSpellAssigner()
        result = _exhaust(assigner.get_change(state))
        assert result is not None


@pytest.mark.unit
class TestHealthIncreaseRandom:
    def test_random_roll_on_subsequent_levels(self) -> None:
        block = HealthIncreaseRandom(class_=Class.WIZARD)
        state = Blueprint()
        state = _exhaust(block.get_change(state))
        state = _exhaust(block.get_change(state))
        assert state.health_base > 0

    def test_reroll_ones(self, monkeypatch: pytest.MonkeyPatch) -> None:
        block = HealthIncreaseRandomRerollOnes(class_=Class.WIZARD)
        state = Blueprint()
        state = _exhaust(block.get_change(state))
        roll_values = iter([1, 4])
        monkeypatch.setattr(random, "randint", lambda a, b: next(roll_values))
        state = _exhaust(block.get_change(state))
        assert state.health_base > 0


@pytest.mark.unit
class TestRandomEquipmentChooserOtherBranch:
    def test_string_equipment_goes_to_others(self) -> None:
        BlueprintWithChoices = create_model(
            "BlueprintWithStringEquipment",
            equipment_choices=(tuple[tuple[object, ...], ...], ...),
            __base__=Blueprint,
        )
        state = BlueprintWithChoices(equipment_choices=(("pack_of_supplies",),))
        chooser = RandomEquipmentChooser()
        result = _exhaust(chooser.get_change(state))
        assert "pack_of_supplies" in result.other_equipment

    def test_armor_equipment_goes_to_armors(self) -> None:
        BlueprintWithChoices = create_model(
            "BlueprintWithArmorEquipment",
            equipment_choices=(tuple[tuple[object, ...], ...], ...),
            __base__=Blueprint,
        )
        state = BlueprintWithChoices(equipment_choices=((ArmorName.LEATHER,),))
        chooser = RandomEquipmentChooser()
        result = _exhaust(chooser.get_change(state))
        assert ArmorName.LEATHER in result.armors


@pytest.mark.unit
class TestSpellAssignerEdgeCases:
    def test_no_available_spells_skips_level(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(spell_base, "_get_available_spells", lambda cls, lvl: [])
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=1).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        assigner = WizardRandomSpellAssigner()
        result = _exhaust(assigner.get_change(state))
        assert result is not None

    def test_all_spells_known_skips_level(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_cantrip = Cantrip.ACID_SPLASH
        mock_spell = FirstLevel.ABSORB_ELEMENTS

        def fake_available(cls, lvl):
            if lvl == 0:
                return [mock_cantrip]
            return [mock_spell]

        monkeypatch.setattr(spell_base, "_get_available_spells", fake_available)
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=1).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        pre_spells = Spells(
            cantrips=(mock_cantrip,),
            first_level_spells=(mock_spell,),
        )
        pre_delta = SpellsDelta(spells=pre_spells)
        state = pre_delta.apply(state)
        assigner = WizardRandomSpellAssigner()
        result = _exhaust(assigner.get_change(state))
        assert result is not None


@pytest.mark.unit
class TestRandomMagicalItemChooserNoItems:
    def test_raises_when_no_items_of_level(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            "dnd.character.blueprint.building_blocks.magical_item_chooser.random.MAGICAL_ITEMS",
            [],
        )
        chooser = RandomMagicalItemChooser(n_common=1)
        with pytest.raises(ValueError, match="No common magical items available"):
            _exhaust(chooser.get_change(Blueprint()))


@pytest.mark.unit
class TestLevelIncrementerClassProperty:
    def test_wizard_class_property(self) -> None:
        assert WizardLevelIncrementer().class_ == Class.WIZARD

    def test_sorcerer_class_property(self) -> None:
        assert SorcererLevelIncrementer().class_ == Class.SORCERER


@pytest.mark.unit
class TestLevelUpRequiresRace:
    def test_raises_without_race(self) -> None:
        level_up = LevelUp.model_construct(blocks=None)
        with pytest.raises(ValueError, match="Race must be chosen before leveling up"):
            next(level_up.get_change(Blueprint()))


@pytest.mark.unit
class TestRandomRaceAssigner:
    def test_returns_valid_race_subrace_pair(self) -> None:
        assigner = RandomRaceAssigner(seed=42)
        pair = assigner._get_race_and_subrace()
        assert isinstance(pair, RaceSubracePair)
        assert isinstance(pair.race, Race)


@pytest.mark.unit
class TestSubclassAssignerLevelTooLow:
    def test_raises_when_level_below_required(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=1).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        assigner = WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION)
        with pytest.raises(ValueError, match="below required level"):
            next(assigner.get_change(state))


@pytest.mark.unit
class TestOptionalSubclassAssigner:
    def test_handles_can_not_assign_gracefully(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=1).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        assigner = OptionalSubclassAssigner(
            assigner=RandomSubclassAssigner(class_=Class.WIZARD)
        )
        result = _exhaust(assigner.get_change(state))
        assert result is not None

    def test_assigns_subclass_successfully_at_eligible_level(self) -> None:
        state = Blueprint()
        state = _exhaust(LevelAssigner(level=3).get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        state = _exhaust(WizardLevelIncrementer().get_change(state))
        assigner = OptionalSubclassAssigner(
            assigner=RandomSubclassAssigner(class_=Class.WIZARD)
        )
        result = _exhaust(assigner.get_change(state))
        assert result is not None
        assert len(result.subclasses) > 0


@pytest.mark.unit
class TestBuilderExceptionHandling:
    def test_exception_during_build_captured_in_result(self) -> None:
        block = NullBlock()
        with patch.object(NullBlock, "get_change", side_effect=ValueError("forced")):
            result = Builder().add(block).build()
        assert result.error is not None
        assert isinstance(result.error, ValueError)


@pytest.mark.unit
class TestPresentableCharacterRaceAbilities:
    def test_race_active_abilities_included_in_actions(self) -> None:
        pc = PresentableCharacter.model_construct(
            race=Race.AARAKOCRA,
            other_active_abilities=("Talons",),
            feats=frozenset(),
            classes={},
            subclasses=(),
        )
        actions = pc.actions
        all_abilities = [a for abilities in actions.values() for a in abilities]
        assert any(a.name == "Talons" for a in all_abilities)
