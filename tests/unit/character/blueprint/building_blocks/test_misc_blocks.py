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
from dnd.character.blueprint.building_blocks.level_up.health_increase import (
    D6HealthIncreaseAverage,
    D8HealthIncreaseAverage,
    D10HealthIncreaseAverage,
    D12HealthIncreaseAverage,
    D6HealthIncreaseRandom,
    D6HealthIncreaseRandomMinTwo,
    D6HealthIncreaseRandomRerollOnes,
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
from dnd.character.spells.spell_slots import WizardCantrip as Cantrip
from dnd.character.spells.spell_slots import WizardFirstLevel as FirstLevel
from dnd.character.spells.spells import Spells
from dnd.character.blueprint.building_blocks.magical_item_chooser.random import (
    RandomMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.building_blocks.stats_builder.standard_array import (
    StandardArray,
)
from dnd.character.blueprint.building_blocks.stats_priority import StatsPriority
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard.base import WizardBlueprint
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.stats import Stats
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
class TestHealthIncreaseRandomMinTwo:
    def test_random_min_two_on_subsequent_level(self) -> None:
        block = D6HealthIncreaseRandomMinTwo()
        state = Blueprint()
        state = block.apply(state)
        state = block.apply(state)
        assert state.health_base >= 2


@pytest.mark.unit
class TestSorcererSpellAssigner:
    def test_first_level_assigns_spells(self) -> None:
        assigner = SorcererRandomSpellAssigner()
        state = SorcererBlueprint(
            classes=ClassLevels(sorcerer=1), spell_slots=FULL_CASTER_SPELL_SLOTS[0]
        )
        result = assigner.apply(state)
        assert result is not None

    def test_second_level_assigns_spells(self) -> None:
        assigner = SorcererRandomSpellAssigner()
        state = SorcererBlueprint(
            classes=ClassLevels(sorcerer=2), spell_slots=FULL_CASTER_SPELL_SLOTS[1]
        )
        result = assigner.apply(state)
        assert result is not None


@pytest.mark.unit
@pytest.mark.parametrize(
    "block, expected_die",
    [
        (D12HealthIncreaseAverage(), 12),
        (D10HealthIncreaseAverage(), 10),
        (D8HealthIncreaseAverage(), 8),
        (D6HealthIncreaseAverage(), 6),
    ],
)
def test_class_hit_die_branches(
    block: D6HealthIncreaseAverage, expected_die: int
) -> None:
    state = Blueprint()
    result = block.apply(state)
    assert result.health_base == expected_die


@pytest.mark.unit
class TestHealthIncreaseRandom:
    def test_random_roll_on_subsequent_levels(self) -> None:
        block = D6HealthIncreaseRandom()
        state = Blueprint()
        state = block.apply(state)
        state = block.apply(state)
        assert state.health_base > 0

    def test_reroll_ones(self, monkeypatch: pytest.MonkeyPatch) -> None:
        block = D6HealthIncreaseRandomRerollOnes()
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
        monkeypatch.setattr(spell_base, "_get_available_spells", lambda query: [])
        state = WizardBlueprint(
            classes=ClassLevels(wizard=1),
            caster=CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[0]),
        )
        assigner = WizardRandomSpellAssigner()
        result = assigner.apply(state)
        assert result is not None

    def test_all_spells_known_skips_level(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_cantrip = Cantrip.ACID_SPLASH
        mock_spell = FirstLevel.ABSORB_ELEMENTS

        def fake_available(query):
            if query[1] == 0:
                return [mock_cantrip]
            return [mock_spell]

        monkeypatch.setattr(spell_base, "_get_available_spells", fake_available)
        pre_spells = Spells(
            cantrips=(mock_cantrip,),
            first_level_spells=(mock_spell,),
        )
        state = WizardBlueprint(
            classes=ClassLevels(wizard=1),
            caster=CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[0]),
            spells=pre_spells,
        )
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
class TestBuildingBlockApplyException:
    def test_exception_propagates_on_apply(self) -> None:
        block = NullBlock()
        with patch.object(NullBlock, "apply", side_effect=ValueError("forced")):
            with pytest.raises(ValueError, match="forced"):
                block.apply(Blueprint())


@pytest.mark.unit
class TestWizardSpellAssignerLevel2:
    def test_wizard_level_2_assigns_spells(self) -> None:
        state = WizardBlueprint(
            classes=ClassLevels(wizard=2),
            caster=CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[1]),
        )
        assigner = WizardRandomSpellAssigner()
        result = assigner.apply(state)
        assert result is not None

    def test_wizard_random_spell_assigner_select_spells(self) -> None:
        state = WizardBlueprint(
            classes=ClassLevels(wizard=2),
            caster=CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[1]),
        )
        assigner = WizardRandomSpellAssigner(seed=42)
        result = assigner.apply(state)
        assert result is not None
