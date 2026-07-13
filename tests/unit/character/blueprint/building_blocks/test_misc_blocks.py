import random
from unittest.mock import patch

import pytest
from pydantic import TypeAdapter
from pydantic import create_model

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.random import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.level_up.health_increase.average import (
    HealthIncreaseAverage,
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
from dnd.character.blueprint.building_blocks.race_assigner.random_race_assigner import (
    RandomRaceAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    base as spell_base,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.random import (
    SorcererRandomSpellAssigner,
    WizardRandomSpellAssigner,
)
from dnd.character.class_levels import ClassLevels
from dnd.character.spells import Cantrip
from dnd.character.spells import FirstLevel
from dnd.character.spells.spells import Spells
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.null_block import NullBlock
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
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.stats import Stats
from dnd.choices.class_creation.character_class import Class, WizardSubclass
from dnd.choices.stats_creation.statistic import Statistic
from dnd.character.race.race import Race
from pydantic import ValidationError

from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)


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
        state = StandardArray(stats_priority=_PRIORITY).apply(blueprint)
        resolver = MaxIfNotMaxedResolver(priority=_PRIORITY)
        result = resolver.apply(state)
        assert result is not None


@pytest.mark.unit
class TestSubclassAssigner:
    def test_can_not_assign_raises_when_no_class(self) -> None:
        block = WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION)
        with pytest.raises(CanNotAssign):
            block.apply(Blueprint())

    def test_early_return_when_subclass_already_present(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=2).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=2)})
        state = WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION).apply(state)
        result = WizardSubclassAssigner(subclass=WizardSubclass.EVOCATION).apply(state)
        assert WizardSubclass.ABJURATION in result.subclasses
        assert WizardSubclass.EVOCATION not in result.subclasses

    def test_random_early_return_when_subclass_already_present(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=2).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=2)})
        state = WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION).apply(state)
        random_assigner = RandomSubclassAssigner(class_=Class.WIZARD)
        result = random_assigner.apply(state)
        assert WizardSubclass.ABJURATION in result.subclasses


@pytest.mark.unit
class TestHealthIncreaseRandomMinTwo:
    def test_random_min_two_on_subsequent_level(self) -> None:
        block = HealthIncreaseRandomMinTwo(class_=Class.WIZARD)
        state = Blueprint()
        state = block.apply(state)
        state = block.apply(state)
        assert state.health_base >= 2


@pytest.mark.unit
class TestSorcererSpellAssigner:
    def test_first_level_assigns_spells(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=1).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(sorcerer=1)})
        assigner = SorcererRandomSpellAssigner()
        result = assigner.apply(state)
        assert result is not None

    def test_second_level_assigns_spells(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=2).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(sorcerer=2)})
        assigner = SorcererRandomSpellAssigner()
        result = assigner.apply(state)
        assert result is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    "class_, expected_die",
    [
        (Class.BARBARIAN, 12),
        (Class.FIGHTER, 10),
        (Class.BARD, 8),
    ],
)
def test_class_hit_die_branches(class_: Class, expected_die: int) -> None:
    block = HealthIncreaseAverage(class_=class_)
    state = Blueprint()
    result = block.apply(state)
    assert result.health_base == expected_die


@pytest.mark.unit
class TestHealthIncreaseRandom:
    def test_random_roll_on_subsequent_levels(self) -> None:
        block = HealthIncreaseRandom(class_=Class.WIZARD)
        state = Blueprint()
        state = block.apply(state)
        state = block.apply(state)
        assert state.health_base > 0

    def test_reroll_ones(self, monkeypatch: pytest.MonkeyPatch) -> None:
        block = HealthIncreaseRandomRerollOnes(class_=Class.WIZARD)
        state = Blueprint()
        state = block.apply(state)
        roll_values = iter([1, 4])
        monkeypatch.setattr(random, "randint", lambda a, b: next(roll_values))
        state = block.apply(state)
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
        result = chooser.apply(state)
        assert "pack_of_supplies" in result.other_equipment

    def test_armor_equipment_goes_to_armors(self) -> None:
        BlueprintWithChoices = create_model(
            "BlueprintWithArmorEquipment",
            equipment_choices=(tuple[tuple[object, ...], ...], ...),
            __base__=Blueprint,
        )
        state = BlueprintWithChoices(equipment_choices=((ArmorName.LEATHER,),))
        chooser = RandomEquipmentChooser()
        result = chooser.apply(state)
        assert ArmorName.LEATHER in result.armors


@pytest.mark.unit
class TestSpellAssignerEdgeCases:
    def test_no_available_spells_skips_level(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(spell_base, "_get_available_spells", lambda cls, lvl: [])
        state = Blueprint()
        state = LevelAssigner(level=1).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=1)})
        assigner = WizardRandomSpellAssigner()
        result = assigner.apply(state)
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
        state = LevelAssigner(level=1).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=1)})
        pre_spells = Spells(
            cantrips=(mock_cantrip,),
            first_level_spells=(mock_spell,),
        )
        state = state.model_copy(update={"spells": pre_spells})
        assigner = WizardRandomSpellAssigner()
        result = assigner.apply(state)
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
            chooser.apply(Blueprint())


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
        state = LevelAssigner(level=1).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=1)})
        assigner = WizardSubclassAssigner(subclass=WizardSubclass.ABJURATION)
        with pytest.raises(ValueError, match="below required level"):
            assigner.apply(state)


@pytest.mark.unit
class TestOptionalSubclassAssigner:
    def test_handles_can_not_assign_gracefully(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=1).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=1)})
        assigner = OptionalSubclassAssigner(
            assigner=RandomSubclassAssigner(class_=Class.WIZARD)
        )
        result = assigner.apply(state)
        assert result is not None

    def test_assigns_subclass_successfully_at_eligible_level(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=3).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=3)})
        assigner = OptionalSubclassAssigner(
            assigner=RandomSubclassAssigner(class_=Class.WIZARD)
        )
        result = assigner.apply(state)
        assert result is not None
        assert len(result.subclasses) > 0


@pytest.mark.unit
class TestBuildingBlockApplyException:
    def test_exception_propagates_on_apply(self) -> None:
        block = NullBlock()
        with patch.object(NullBlock, "apply", side_effect=ValueError("forced")):
            with pytest.raises(ValueError, match="forced"):
                block.apply(Blueprint())


@pytest.mark.unit
class TestWizardSpellAssignerLevel2:
    def test_wizard_level_2_assigns_spells(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=2).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=2)})
        assigner = WizardRandomSpellAssigner()
        result = assigner.apply(state)
        assert result is not None

    def test_wizard_random_spell_assigner_select_spells(self) -> None:
        state = Blueprint()
        state = LevelAssigner(level=2).apply(state)
        state = state.model_copy(update={"classes": ClassLevels(wizard=2)})
        assigner = WizardRandomSpellAssigner(seed=42)
        result = assigner.apply(state)
        assert result is not None
