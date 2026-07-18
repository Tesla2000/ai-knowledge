import json
import sys
import termios
import tty
from collections.abc import Callable, Iterator
from functools import partial
from itertools import islice
from pathlib import Path

import pytest

import dnd.character.actions._melee_attack as melee_attack_module
import dnd.character.actions.combat.cast_fireball as cast_fireball_module
import dnd.fight._attack as attack_module
import dnd.fight._creature as creature_module
import dnd.fight._saving_throw as saving_throw_module
import dnd.fight._spell_attack as spell_attack_module
import scripts.fight as fight_module
from dnd.character.presentable_character import PresentableCharacter
from dnd.character.spells.max_spell_levels import SpellSlots
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic
from dnd.character._ability_name import AbilityName
from dnd.fight._action_group import _And, _Or
from dnd.fight._attack import _Attack
from dnd.fight._attack_result import _AttackResult
from dnd.fight._creature import _Creature
from dnd.character.actions._damage_type import DamageType
from dnd.fight._fight_resource import _FightResource, ResourceName
from dnd.fight._multi_attack import _MultiAttack
from dnd.fight._non_attack import _NonAttack
from dnd.fight._saving_throw import _SavingThrow
from dnd.fight._saving_throw_result import _SavingThrowResult
from dnd.fight._spell_attack import _SpellAttack
from dnd.character.actions.attack_bonus_modifier import RageAttackBonusModifier
from dnd.character.actions.damage_resistance_modifier import RageDamageResistanceModifier
from dnd.character.actions.combat import AttackWithAxe, CastFireball, UseRage
from dnd._combat_event import (
    CombatEventType,
    CreatureAttackedEvent,
    CreatureTargetedEvent,
    MeleeDamageEvent,
    RageEndsEvent,
    TurnStartEvent,
)
from dnd.character.actions.get_actions import get_actions
from dnd.fight.battlemap import Battlemap
from dnd.fight.fight_character import FightCharacter, SpellcasterFightCharacter
from scripts.fight import (
    _EncounterEntry,
    _FightCli,
    _PlayerEntry,
    _describe,
    _dmg,
    _fire,
    _load_character,
    _load_creature,
    _pick,
    _select,
    _stats,
)


class _Rec:
    """Records calls; replaces unittest.mock.patch."""

    def __init__(
        self, *values: object, fn: Callable[..., object] | None = None
    ) -> None:
        self._it: Iterator[object] | None = iter(values) if values else None
        self._fn: Callable[..., object] | None = fn
        self.call_args_list: list[tuple[tuple[object, ...], dict[str, object]]] = []
        self.call_count = 0

    def __call__(self, *args: object, **kwargs: object) -> object:
        self.call_args_list.append((args, kwargs))
        self.call_count += 1
        if self._fn is not None:
            return self._fn(*args, **kwargs)
        if self._it is not None:
            return next(self._it)
        return None

    def __get__(self, obj: object, objtype: object = None) -> object:
        if obj is None:
            return self
        return partial(self, obj)


_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=10,
    wisdom=10,
    charisma=10,
)

_BASE_DATA: dict[str, object] = {
    "name": "test",
    "stats": _STATS.model_dump(),
    "speed": 30,
    "dark_vision_range": 0,
    "initiative_bonus": 2,
    "saving_throw_proficiencies": [],
    "other_active_abilities": [],
}

_BASE_PC_DATA: dict[str, object] = {
    "race": "Human",
    "stats": _STATS.model_dump(),
    "health_base": 8,
    "character_data": {"name": "test"},
    "classes": {
        "wizard": 0,
        "sorcerer": 0,
        "fighter": 0,
        "barbarian": 1,
        "rogue": 0,
        "cleric": 0,
        "druid": 0,
        "paladin": 0,
        "ranger": 0,
        "monk": 0,
        "bard": 0,
        "warlock": 0,
        "artificer": 0,
    },
    "speed": 30,
    "dark_vision_range": 0,
    "saving_throw_proficiencies": [],
    "other_active_abilities": [],
}


def _pc_json(name: str) -> str:
    return json.dumps(
        PresentableCharacter.model_validate(
            {**_BASE_PC_DATA, "character_data": {"name": name}}
        ).model_dump(mode="json")
    )


_CREATURE_DATA: dict[str, object] = {
    **_BASE_DATA,
    "n_hit_dice": 1,
    "hit_die_size": 8,
    "attacks": [
        {
            "n_dice": 1,
            "dice_size": 6,
            "attack_bonus": 2,
            "damage_bonus": 0,
            "name": "punch",
        }
    ],
}


class _FloatBonusCreature(_Creature):
    initiative_bonus: float = 21.37


class _IntNameCreature(_Creature):
    name: int = 0


@pytest.mark.unit
class TestAttack:
    _attack = _Attack(
        n_dice=2, dice_size=6, attack_bonus=3, damage_bonus=1, name="sword"
    )

    def test_perform_normal_rolls(self, monkeypatch: pytest.MonkeyPatch) -> None:
        rec = _Rec(10, 15, 4, 3, 2, 1, 3, 2)
        monkeypatch.setattr(attack_module, "randint", rec)
        result = self._attack.perform()
        assert result.first_roll == 13
        assert result.second_roll == 18
        assert isinstance(result, _AttackResult)

    def test_perform_first_roll_critical(self, monkeypatch: pytest.MonkeyPatch) -> None:
        rec = _Rec(20, 10, 3, 4, 2, 1, 3, 2)
        monkeypatch.setattr(attack_module, "randint", rec)
        result = self._attack.perform()
        assert result.first_roll == "critical"
        assert result.second_roll == 13

    def test_perform_second_roll_critical(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        rec = _Rec(10, 20, 3, 4, 2, 1, 3, 2)
        monkeypatch.setattr(attack_module, "randint", rec)
        result = self._attack.perform()
        assert result.first_roll == 13
        assert result.second_roll == "critical"

    def test_perform_both_critical(self, monkeypatch: pytest.MonkeyPatch) -> None:
        rec = _Rec(20, 20, 3, 4, 2, 1, 3, 2)
        monkeypatch.setattr(attack_module, "randint", rec)
        result = self._attack.perform()
        assert result.first_roll == "critical"
        assert result.second_roll == "critical"


@pytest.mark.unit
class TestAttackResult:
    def test_str_no_crit(self) -> None:
        r = _AttackResult(first_roll=10, second_roll=8, damage=5, crit_damage=0)
        s = str(r)
        assert "first_roll=10" in s
        assert "second_roll=8" in s
        assert "damage=5" in s

    def test_str_first_crit(self) -> None:
        r = _AttackResult(first_roll="critical", second_roll=8, damage=5, crit_damage=9)
        assert "crit: 9" in str(r)

    def test_str_second_crit(self) -> None:
        r = _AttackResult(
            first_roll=10, second_roll="critical", damage=5, crit_damage=9
        )
        assert "crit with adv: 9" in str(r)

    def test_str_both_crit(self) -> None:
        r = _AttackResult(
            first_roll="critical", second_roll="critical", damage=5, crit_damage=9
        )
        assert "crit with disadvantage: 9" in str(r)


@pytest.mark.unit
class TestSavingThrow:
    def test_perform_half_on_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        st = _SavingThrow(
            n_dice=2,
            dice_size=6,
            damage_bonus=0,
            dc=15,
            name="fireball",
            saving_throw_type=Statistic.DEXTERITY,
            half_on_success=True,
        )
        rec = _Rec(4, 4)
        monkeypatch.setattr(saving_throw_module, "randint", rec)
        result = st.perform()
        assert isinstance(result, _SavingThrowResult)
        assert result.dc == 15
        assert result.saving_throw_type == Statistic.DEXTERITY
        assert result.damage_on_fail == 8
        assert result.damage_on_success == 4

    def test_perform_no_half_on_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        st = _SavingThrow(
            n_dice=1,
            dice_size=8,
            damage_bonus=2,
            dc=13,
            name="poison",
            saving_throw_type=Statistic.CONSTITUTION,
            half_on_success=False,
        )
        rec = _Rec(6)
        monkeypatch.setattr(saving_throw_module, "randint", rec)
        result = st.perform()
        assert result.damage_on_fail == 8
        assert result.damage_on_success == 0

    def test_saving_throw_result_str(self) -> None:
        result = _SavingThrowResult(
            dc=15,
            saving_throw_type=Statistic.DEXTERITY,
            damage_on_fail=10,
            damage_on_success=5,
        )
        assert str(result) == "DC 15 dexterity save | fail: 10 | success: 5"


@pytest.mark.unit
class TestMultiAttack:
    def test_perform_calls_each_attack(self, monkeypatch: pytest.MonkeyPatch) -> None:
        attack1 = _Attack(n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1)
        attack2 = _Attack(n_dice=1, dice_size=8, attack_bonus=3, damage_bonus=2)
        multi = _MultiAttack(attacks=(attack1, attack2))
        mock_result = _AttackResult(
            first_roll=10, second_roll=15, damage=5, crit_damage=8
        )
        mock_perform = _Rec(fn=lambda self: mock_result)
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, mock_perform)
        results = multi.perform()
        assert mock_perform.call_count == 2
        assert results == [mock_result, mock_result]


@pytest.mark.unit
class TestSpellAttack:
    _spell = _SpellAttack(
        base_n_dice=1,
        extra_dice_per_level=1,
        dice_size=6,
        attack_bonus=5,
        damage_bonus=0,
        min_level=1,
        max_level=3,
        name="magic missile",
    )

    def test_perform_returns_one_result_per_level(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(spell_attack_module, "randint", lambda *a: 10)
        results = self._spell.perform()
        assert len(results) == 3

    def test_perform_at_level_critical(self, monkeypatch: pytest.MonkeyPatch) -> None:
        rec = _Rec(20, 10, 3, 4, 2)
        monkeypatch.setattr(spell_attack_module, "randint", rec)
        result = self._spell._perform_at_level(1)
        assert result.first_roll == "critical"
        assert result.second_roll == 15

    def test_perform_at_level_second_critical(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        rec = _Rec(10, 20, 3, 4, 2, 1)
        monkeypatch.setattr(spell_attack_module, "randint", rec)
        result = self._spell._perform_at_level(1)
        assert result.first_roll == 15
        assert result.second_roll == "critical"

    def test_extra_dice_scale_with_level(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(spell_attack_module, "randint", lambda *a: 3)
        result_l1 = self._spell._perform_at_level(1)
        result_l2 = self._spell._perform_at_level(2)
        assert result_l2.damage > result_l1.damage


@pytest.mark.unit
class TestCreatureInit:
    def test_roll_initiative_with_bonus(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(creature_module, "randint", lambda *a: 10)
        creature = _Creature.model_validate({**_CREATURE_DATA, "initiative_bonus": 5})
        assert creature.initiative == 15

    def test_roll_initiative_invalid_bonus_type(self) -> None:
        with pytest.raises(ValueError, match="initiative_bonus must be int"):
            _FloatBonusCreature.model_validate(
                {**_CREATURE_DATA, "initiative_bonus": 21.37}
            )

    def test_default_type_uses_name(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(creature_module, "randint", lambda *a: 1)
        creature = _Creature.model_validate(_CREATURE_DATA)
        assert creature.type == "test"

    def test_default_type_invalid_name_type(self) -> None:
        with pytest.raises(ValueError, match="name must be str"):
            _IntNameCreature.model_validate({**_CREATURE_DATA, "name": 0})

    def test_explicit_initiative_bypasses_roll(self) -> None:
        creature = _Creature.model_validate({**_CREATURE_DATA, "initiative": 18})
        assert creature.initiative == 18

    def test_creature_requires_attacks(self) -> None:
        with pytest.raises(ValueError, match="creature must have at least one attack"):
            _Creature.model_validate({**_CREATURE_DATA, "attacks": [], "initiative": 1})

    def test_invalid_stats_type_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="stats must be Stats"):
            creature_module._default_hp({"stats": "not a Stats object"})


def _make_fc(**kwargs: object) -> FightCharacter:
    pc = PresentableCharacter.model_validate(_BASE_PC_DATA)
    return FightCharacter.from_presentable(pc, initiative=14).model_copy(update=kwargs)


def _make_fc_with_attack(**kwargs: object) -> FightCharacter:
    pc = PresentableCharacter.model_validate(
        {**_BASE_PC_DATA, "actions": [AbilityName.ATTACK_WITH_AXE]}
    )
    return FightCharacter.from_presentable(pc, initiative=14).model_copy(update=kwargs)


def _make_battlemap(*fighters: FightCharacter) -> Battlemap:
    return Battlemap(combatants=fighters)


def _make_adjacent_target() -> FightCharacter:
    pc = PresentableCharacter.model_validate(_BASE_PC_DATA)
    return FightCharacter.from_presentable(pc, initiative=5).model_copy(
        update={"position": (1, 0)}
    )


_RAGE_RESOURCE = _FightResource(name=ResourceName.RAGE, max_uses=3, remaining_uses=2)


@pytest.mark.unit
class TestFightCharacter:
    def test_from_presentable(self) -> None:
        pc = PresentableCharacter.model_validate(_BASE_PC_DATA)
        fc = FightCharacter.from_presentable(pc, initiative=14)
        assert fc.name == "test"
        assert fc.initiative == 14
        assert fc.current_health == fc.max_health
        assert fc.has_action is True
        assert fc.has_bonus_action is True
        assert fc.has_reaction is True
        assert fc.has_free_action is True

    def test_get_actions_skips_unknown_names(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.BLADESONG]}
            )
        )
        bm = _make_battlemap(fc)
        assert get_actions(fc, bm) == ()

    def test_get_actions_returns_rage_when_resource_available(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.RAGE]}
            ),
            resources=(_RAGE_RESOURCE,),
        )
        bm = _make_battlemap(fc)
        action_groups = get_actions(fc, bm)
        assert len(action_groups) == 1
        assert len(action_groups[0]) == 1
        assert isinstance(action_groups[0][0], UseRage)

    def test_get_actions_no_rage_when_already_raging(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.RAGE]}
            ),
            resources=(_RAGE_RESOURCE,),
            active_features=frozenset({AbilityName.RAGE}),
        )
        bm = _make_battlemap(fc)
        assert get_actions(fc, bm) == ()

    def test_get_actions_no_rage_when_no_resource(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.RAGE]}
            ),
        )
        bm = _make_battlemap(fc)
        assert get_actions(fc, bm) == ()

    def test_get_actions_no_rage_when_no_bonus_action(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.RAGE]}
            ),
            resources=(_RAGE_RESOURCE,),
            has_bonus_action=False,
        )
        bm = _make_battlemap(fc)
        assert get_actions(fc, bm) == ()

    def test_get_actions_returns_attack_when_has_action(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.ATTACK_WITH_AXE]}
            ),
        )
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        action_groups = get_actions(fc, bm)
        assert len(action_groups) == 1
        assert len(action_groups[0]) == 1
        assert isinstance(action_groups[0][0], AttackWithAxe)

    def test_get_actions_returns_two_attack_slots_for_two_melee_actions(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {
                    **_BASE_PC_DATA,
                    "actions": [
                        AbilityName.ATTACK_WITH_AXE,
                        AbilityName.ATTACK_WITH_AXE,
                    ],
                }
            ),
        )
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        action_groups = get_actions(fc, bm)
        assert len(action_groups) == 2
        assert all(isinstance(g[0], AttackWithAxe) for g in action_groups)

    def test_get_actions_no_attack_when_action_spent(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.ATTACK_WITH_AXE]}
            ),
            has_action=False,
            attacks_remaining=0,
        )
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        assert get_actions(fc, bm) == ()


@pytest.mark.unit
class TestUseRage:
    def test_perform_sets_resistance_and_bonus(self) -> None:
        fc = _make_fc(resources=(_RAGE_RESOURCE,))
        bm = _make_battlemap(fc)
        rages = UseRage.create(fc)
        assert len(rages) == 1
        new_bm = rages[0].perform(bm)
        new_fc = new_bm.combatants[0]
        assert isinstance(new_fc, FightCharacter)
        assert any(isinstance(m, RageDamageResistanceModifier) for m in new_fc.modifiers)
        assert any(isinstance(m, RageAttackBonusModifier) for m in new_fc.modifiers)
        assert AbilityName.RAGE in new_fc.active_features
        assert not new_fc.has_bonus_action

    def test_perform_consumes_rage_resource(self) -> None:
        fc = _make_fc(resources=(_RAGE_RESOURCE,))
        bm = _make_battlemap(fc)
        rages = UseRage.create(fc)
        assert len(rages) == 1
        new_bm = rages[0].perform(bm)
        new_fc = new_bm.combatants[0]
        assert isinstance(new_fc, FightCharacter)
        remaining = next(r for r in new_fc.resources if r.name == ResourceName.RAGE)
        assert remaining.remaining_uses == _RAGE_RESOURCE.remaining_uses - 1

    def test_perform_appends_rage_modifier_without_replacing_existing(self) -> None:
        existing = RageAttackBonusModifier(owner_id=_make_fc().id)
        fc = _make_fc(
            resources=(_RAGE_RESOURCE,),
            modifiers=(existing,),
        )
        bm = _make_battlemap(fc)
        rages = UseRage.create(fc)
        assert len(rages) == 1
        new_bm = rages[0].perform(bm)
        new_fc = new_bm.combatants[0]
        assert isinstance(new_fc, FightCharacter)
        # existing + RageAttackBonusModifier + RageDamageResistanceModifier
        assert len(new_fc.modifiers) == 3
        assert new_fc.modifiers[0] is existing


@pytest.mark.unit
class TestBattlemapEmit:
    def test_emit_turn_start_resets_actions(self) -> None:
        fc = _make_fc(
            has_action=False,
            has_bonus_action=False,
            has_reaction=False,
            has_free_action=False,
            attacks_remaining=0,
        )
        bm = _make_battlemap(fc)
        new_bm = bm.emit(TurnStartEvent(target_id=fc.id))
        new_fc = new_bm.combatants[0]
        assert isinstance(new_fc, FightCharacter)
        assert new_fc.has_action is True
        assert new_fc.has_bonus_action is True
        assert new_fc.has_reaction is True
        assert new_fc.has_free_action is True
        assert new_fc.attacks_remaining == new_fc.number_of_attacks

    def test_emit_turn_start_only_affects_target(self) -> None:
        fc1 = _make_fc(has_action=False)
        fc2 = _make_fc_with_attack(has_action=False)
        bm = _make_battlemap(fc1, fc2)
        new_bm = bm.emit(TurnStartEvent(target_id=fc1.id))
        assert isinstance(new_bm.combatants[0], FightCharacter)
        assert new_bm.combatants[0].has_action is True
        assert isinstance(new_bm.combatants[1], FightCharacter)
        assert new_bm.combatants[1].has_action is False

    def test_emit_rage_ends_removes_rage_state(self) -> None:
        fc_base = _make_fc(resources=(_RAGE_RESOURCE,))
        fc = fc_base.model_copy(
            update={
                "active_features": frozenset({AbilityName.RAGE}),
                "modifiers": (
                    RageAttackBonusModifier(owner_id=fc_base.id),
                    RageDamageResistanceModifier(owner_id=fc_base.id),
                ),
            }
        )
        bm = _make_battlemap(fc)
        new_bm = bm.emit(RageEndsEvent(target_id=fc.id))
        new_fc = new_bm.combatants[0]
        assert isinstance(new_fc, FightCharacter)
        assert AbilityName.RAGE not in new_fc.active_features
        assert not any(isinstance(m, RageAttackBonusModifier) for m in new_fc.modifiers)
        assert not any(isinstance(m, RageDamageResistanceModifier) for m in new_fc.modifiers)

    def test_emit_rage_ends_only_affects_target(self) -> None:
        fc1 = _make_fc(
            active_features=frozenset({AbilityName.RAGE}),
            damage_resistance=frozenset({DamageType.BLUDGEONING}),
        )
        fc2 = _make_fc_with_attack(
            active_features=frozenset({AbilityName.RAGE}),
            damage_resistance=frozenset({DamageType.BLUDGEONING}),
        )
        bm = _make_battlemap(fc1, fc2)
        new_bm = bm.emit(RageEndsEvent(target_id=fc1.id))
        assert isinstance(new_bm.combatants[0], FightCharacter)
        assert AbilityName.RAGE not in new_bm.combatants[0].active_features
        assert isinstance(new_bm.combatants[1], FightCharacter)
        assert AbilityName.RAGE in new_bm.combatants[1].active_features

    def test_emit_appends_event_to_log(self) -> None:
        fc = _make_fc()
        bm = _make_battlemap(fc)
        assert len(bm.event_log) == 0
        event = TurnStartEvent(target_id=fc.id)
        new_bm = bm.emit(event)
        assert new_bm.event_log == (event,)

    def test_emit_chained_events_all_appear_in_log(self) -> None:
        fc = _make_fc()
        bm = _make_battlemap(fc)
        e1 = TurnStartEvent(target_id=fc.id)
        e2 = RageEndsEvent(target_id=fc.id)
        new_bm = bm.emit(e1)
        new_bm = new_bm.emit(e2)
        assert new_bm.event_log == (e1, e2)

    def test_emit_rage_ends_removes_rage_bonus_modifier_only_for_owner(self) -> None:
        fc1 = _make_fc()
        fc2 = _make_fc_with_attack()
        modifier_for_fc1 = RageAttackBonusModifier(owner_id=fc1.id)
        modifier_for_fc2 = RageAttackBonusModifier(owner_id=fc2.id)
        fc1 = fc1.model_copy(update={"modifiers": (modifier_for_fc1,)})
        fc2 = fc2.model_copy(update={"modifiers": (modifier_for_fc2,)})
        bm = _make_battlemap(fc1, fc2)
        new_bm = bm.emit(RageEndsEvent(target_id=fc1.id))
        result_fc1 = new_bm.combatants[0]
        result_fc2 = new_bm.combatants[1]
        assert isinstance(result_fc1, FightCharacter)
        assert isinstance(result_fc2, FightCharacter)
        assert len(result_fc1.modifiers) == 0
        assert len(result_fc2.modifiers) == 1


@pytest.mark.unit
class TestAttackWithAxe:
    def test_create_returns_empty_when_no_action(self) -> None:
        fc = _make_fc_with_attack(has_action=False, attacks_remaining=0)
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        assert AttackWithAxe.create(fc, bm) == ()

    def test_create_returns_empty_when_no_attack_action(self) -> None:
        fc = _make_fc()
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        assert AttackWithAxe.create(fc, bm) == ()

    def test_create_returns_empty_when_no_attack_with_axe_ability(self) -> None:
        fc = _make_fc(
            character=PresentableCharacter.model_validate(
                {**_BASE_PC_DATA, "actions": [AbilityName.EXTRA_ATTACK]}
            ),
        )
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        assert AttackWithAxe.create(fc, bm) == ()

    def test_create_returns_empty_when_no_adjacent_target(self) -> None:
        fc = _make_fc_with_attack()
        far_target = _make_fc().model_copy(update={"position": (5, 5)})
        bm = _make_battlemap(fc, far_target)
        assert AttackWithAxe.create(fc, bm) == ()

    def test_create_returns_one_per_adjacent_target(self) -> None:
        fc = _make_fc_with_attack()
        t1 = _make_fc().model_copy(update={"position": (1, 0)})
        t2 = _make_fc().model_copy(update={"position": (0, 1)})
        bm = _make_battlemap(fc, t1, t2)
        attacks = AttackWithAxe.create(fc, bm)
        assert len(attacks) == 2
        positions = {a.target_position for a in attacks}
        assert positions == {(1, 0), (0, 1)}

    def test_perform_spends_action(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(melee_attack_module, "randint", lambda *a: 10)
        fc = _make_fc_with_attack()
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        attacks = AttackWithAxe.create(fc, bm)
        assert len(attacks) == 1
        new_bm = attacks[0].perform(bm)
        new_fc = new_bm.combatants[0]
        assert isinstance(new_fc, FightCharacter)
        assert not new_fc.has_action

    def test_perform_rolls_dice(self, monkeypatch: pytest.MonkeyPatch) -> None:
        rolls: list[int] = []

        def fake_randint(a: int, b: int) -> int:
            rolls.append(a)
            return 5

        monkeypatch.setattr(melee_attack_module, "randint", fake_randint)
        fc = _make_fc_with_attack()
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        attacks = AttackWithAxe.create(fc, bm)
        assert len(attacks) == 1
        attacks[0].perform(bm)
        assert len(rolls) > 0


@pytest.mark.unit
class TestAttackEventPhases:
    def test_hit_emits_all_three_events(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(melee_attack_module, "randint", lambda *a: 20)
        fc = _make_fc_with_attack()
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        attacks = AttackWithAxe.create(fc, bm)
        assert len(attacks) == 1
        new_bm = attacks[0].perform(bm)
        event_types = [e.type for e in new_bm.event_log]
        assert CombatEventType.CREATURE_TARGETED in event_types
        assert CombatEventType.CREATURE_ATTACKED in event_types
        assert CombatEventType.MELEE_DAMAGE in event_types

    def test_miss_omits_melee_damage_event(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(melee_attack_module, "randint", lambda *a: 1)
        fc = _make_fc_with_attack()
        target = _make_adjacent_target().model_copy(update={"base_ac": 30})
        bm = _make_battlemap(fc, target)
        attacks = AttackWithAxe.create(fc, bm)
        assert len(attacks) == 1
        new_bm = attacks[0].perform(bm)
        event_types = [e.type for e in new_bm.event_log]
        assert CombatEventType.CREATURE_TARGETED in event_types
        assert CombatEventType.CREATURE_ATTACKED in event_types
        assert CombatEventType.MELEE_DAMAGE not in event_types

    def test_events_carry_correct_attacker_and_defender_ids(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(melee_attack_module, "randint", lambda *a: 20)
        fc = _make_fc_with_attack()
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        attacks = AttackWithAxe.create(fc, bm)
        new_bm = attacks[0].perform(bm)
        targeted = next(
            e for e in new_bm.event_log if isinstance(e, CreatureTargetedEvent)
        )
        attacked = next(
            e for e in new_bm.event_log if isinstance(e, CreatureAttackedEvent)
        )
        damage = next(e for e in new_bm.event_log if isinstance(e, MeleeDamageEvent))
        assert targeted.attacker_id == fc.id
        assert targeted.defender_id == target.id
        assert attacked.attacker_id == fc.id
        assert attacked.defender_id == target.id
        assert damage.attacker_id == fc.id
        assert damage.defender_id == target.id

    def test_all_three_phases_share_same_attack_id(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(melee_attack_module, "randint", lambda *a: 20)
        fc = _make_fc_with_attack()
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        attacks = AttackWithAxe.create(fc, bm)
        new_bm = attacks[0].perform(bm)
        targeted = next(
            e for e in new_bm.event_log if isinstance(e, CreatureTargetedEvent)
        )
        attacked = next(
            e for e in new_bm.event_log if isinstance(e, CreatureAttackedEvent)
        )
        damage = next(e for e in new_bm.event_log if isinstance(e, MeleeDamageEvent))
        assert targeted.attack_id == attacked.attack_id == damage.attack_id


_SPELL_SLOTS_WITH_L3 = SpellSlots(
    level_1=4,
    level_2=3,
    level_3=2,
    level_4=0,
    level_5=0,
    level_6=0,
    level_7=0,
    level_8=0,
    level_9=0,
)
_SPELL_SLOTS_NO_L3 = SpellSlots(
    level_1=4,
    level_2=3,
    level_3=0,
    level_4=0,
    level_5=0,
    level_6=0,
    level_7=0,
    level_8=0,
    level_9=0,
)


def _make_sfc(**kwargs: object) -> SpellcasterFightCharacter:
    pc = PresentableCharacter.model_validate(
        {**_BASE_PC_DATA, "actions": [AbilityName.FIREBALL]}
    )
    return SpellcasterFightCharacter(
        character=pc,
        initiative=14,
        max_health=pc.health,
        current_health=pc.health,
        remaining_spell_slots=_SPELL_SLOTS_WITH_L3,
    ).model_copy(update=kwargs)


@pytest.mark.unit
class TestCastFireball:
    def test_create_returns_empty_for_non_spellcaster(self) -> None:
        fc = _make_fc_with_attack()
        target = _make_adjacent_target()
        bm = _make_battlemap(fc, target)
        assert CastFireball.create(fc, bm) == ()

    def test_create_returns_empty_when_no_action(self) -> None:
        sfc = _make_sfc(has_action=False)
        target = _make_adjacent_target()
        bm = _make_battlemap(sfc, target)
        assert CastFireball.create(sfc, bm) == ()

    def test_create_returns_empty_when_no_level3_slots(self) -> None:
        sfc = _make_sfc(remaining_spell_slots=_SPELL_SLOTS_NO_L3)
        target = _make_adjacent_target()
        bm = _make_battlemap(sfc, target)
        assert CastFireball.create(sfc, bm) == ()

    def test_create_returns_empty_when_no_fireball_ability(self) -> None:
        pc = PresentableCharacter.model_validate(
            {**_BASE_PC_DATA, "actions": [AbilityName.EXTRA_ATTACK]}
        )
        sfc = SpellcasterFightCharacter(
            character=pc,
            initiative=14,
            max_health=pc.health,
            current_health=pc.health,
            remaining_spell_slots=_SPELL_SLOTS_WITH_L3,
        )
        target = _make_adjacent_target()
        bm = _make_battlemap(sfc, target)
        assert CastFireball.create(sfc, bm) == ()

    def test_create_returns_one_per_enemy(self) -> None:
        sfc = _make_sfc()
        t1 = _make_fc().model_copy(update={"position": (1, 0)})
        t2 = _make_fc().model_copy(update={"position": (2, 0)})
        bm = _make_battlemap(sfc, t1, t2)
        fireballs = CastFireball.create(sfc, bm)
        assert len(fireballs) == 2
        centers = {f.center_position for f in fireballs}
        assert centers == {(1, 0), (2, 0)}

    def test_perform_spends_action_and_slot(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(cast_fireball_module, "randint", lambda *_: 3)
        sfc = _make_sfc()
        target = _make_fc().model_copy(update={"position": (6, 0)})
        bm = _make_battlemap(sfc, target)
        fireballs = CastFireball.create(sfc, bm)
        assert len(fireballs) == 1
        new_bm = fireballs[0].perform(bm)
        new_sfc = new_bm.combatants[0]
        assert isinstance(new_sfc, SpellcasterFightCharacter)
        assert not new_sfc.has_action
        assert new_sfc.remaining_spell_slots.level_3 == _SPELL_SLOTS_WITH_L3.level_3 - 1

    def test_perform_applies_full_damage_on_failed_save(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(cast_fireball_module, "randint", lambda *_: 1)
        sfc = _make_sfc()
        target = _make_fc().model_copy(
            update={"position": (6, 0), "max_health": 200, "current_health": 200}
        )
        bm = _make_battlemap(sfc, target)
        fireballs = CastFireball.create(sfc, bm)
        new_bm = fireballs[0].perform(bm)
        new_target = next(c for c in new_bm.combatants if c.position == target.position)
        expected_damage = 8 * 1
        assert new_target.current_health == target.current_health - expected_damage

    def test_perform_applies_half_damage_on_successful_save(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(cast_fireball_module, "randint", lambda *_: 20)
        sfc = _make_sfc()
        target = _make_fc().model_copy(
            update={"position": (6, 0), "max_health": 200, "current_health": 200}
        )
        bm = _make_battlemap(sfc, target)
        fireballs = CastFireball.create(sfc, bm)
        new_bm = fireballs[0].perform(bm)
        new_target = next(c for c in new_bm.combatants if c.position == target.position)
        expected_damage = (8 * 20) // 2
        assert new_target.current_health == target.current_health - expected_damage

    def test_perform_skips_combatants_outside_radius(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(cast_fireball_module, "randint", lambda *_: 1)
        sfc = _make_sfc()
        close = _make_fc().model_copy(update={"position": (1, 0)})
        far = _make_fc().model_copy(update={"position": (10, 10)})
        bm = _make_battlemap(sfc, close, far)
        fireballs = CastFireball.create(sfc, bm)
        close_fireball = next(f for f in fireballs if f.center_position == (1, 0))
        new_bm = close_fireball.perform(bm)
        new_far = next(c for c in new_bm.combatants if c.position == (10, 10))
        assert new_far.current_health == far.current_health


@pytest.mark.unit
class TestNonAttack:
    def test_perform_returns_description(self) -> None:
        na = _NonAttack(name="Stomp", description="massive crush")
        assert na.perform() == "massive crush"

    def test_default_name_empty(self) -> None:
        na = _NonAttack(description="roar")
        assert na.name == ""


@pytest.mark.unit
class TestActionGroups:
    _attack = _Attack(
        n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="claw"
    )
    _st = _SavingThrow(
        n_dice=1,
        dice_size=6,
        damage_bonus=0,
        dc=12,
        name="venom",
        saving_throw_type=Statistic.CONSTITUTION,
        half_on_success=False,
    )

    def test_or_perform(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        result = _Or(options=(self._attack,)).perform()
        assert result == mock_result

    def test_and_perform(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        results = _And(options=(self._attack, self._attack)).perform()
        assert len(results) == 2


@pytest.mark.unit
class TestFightHelpers:
    def test_dmg_no_bonus(self) -> None:
        assert _dmg(2, 6, 0) == "2d6"

    def test_dmg_positive_bonus(self) -> None:
        assert _dmg(1, 8, 3) == "1d8+3"

    def test_dmg_negative_bonus(self) -> None:
        assert _dmg(1, 8, -2) == "1d8-2"

    def test_stats_non_attack(self) -> None:
        na = _NonAttack(description="roar")
        assert _stats(na) == "roar"

    def test_stats_saving_throw(self) -> None:
        st = _SavingThrow(
            n_dice=2,
            dice_size=6,
            damage_bonus=0,
            dc=14,
            name="fireball",
            saving_throw_type=Statistic.DEXTERITY,
            half_on_success=True,
        )
        result = _stats(st)
        assert "DC 14" in result
        assert "half on save" in result

    def test_stats_saving_throw_no_half(self) -> None:
        st = _SavingThrow(
            n_dice=1,
            dice_size=6,
            damage_bonus=0,
            dc=12,
            name="poison",
            saving_throw_type=Statistic.CONSTITUTION,
            half_on_success=False,
        )
        result = _stats(st)
        assert "half on save" not in result

    def test_stats_attack(self) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=4, damage_bonus=2, name="sword"
        )
        result = _stats(attack)
        assert "+4 to hit" in result

    def test_stats_and(self) -> None:
        attack = _Attack(n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0)
        and_group = _And(options=(attack, attack))
        result = _stats(and_group)
        assert "2 attacks" in result

    def test_stats_or(self) -> None:
        attack = _Attack(n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0)
        or_group = _Or(options=(attack, attack))
        result = _stats(or_group)
        assert "2 options" in result

    def test_describe_non_attack(self) -> None:
        na = _NonAttack(name="Stomp", description="crush")
        assert _describe(na) == "Stomp"

    def test_describe_non_attack_no_name(self) -> None:
        na = _NonAttack(description="crush")
        assert _describe(na) == "(action)"

    def test_describe_attack(self) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=3, damage_bonus=1, name="sword"
        )
        result = _describe(attack)
        assert "sword" in result
        assert "+3 to hit" in result

    def test_describe_and_no_name(self) -> None:
        attack = _Attack(n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0)
        and_group = _And(options=(attack, attack))
        result = _describe(and_group)
        assert "Multiattack" in result

    def test_select_single_option(self) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="claw"
        )
        result = _select((attack,), "Choose")
        assert result is attack

    def test_select_multiple_options(self, monkeypatch: pytest.MonkeyPatch) -> None:
        attack1 = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="claw"
        )
        attack2 = _Attack(
            n_dice=1, dice_size=8, attack_bonus=3, damage_bonus=1, name="bite"
        )
        monkeypatch.setattr(fight_module, "_pick", lambda *a, **k: 1)
        result = _select((attack1, attack2), "Choose")
        assert result is attack2

    def test_fire_non_attack(self, monkeypatch: pytest.MonkeyPatch) -> None:
        na = _NonAttack(name="Roar", description="loud noise")
        written: list[str] = []
        monkeypatch.setattr(sys.stdout, "write", written.append)
        _fire("monster", na)
        assert any("Roar" in s and "loud noise" in s for s in written)

    def test_fire_and(self, monkeypatch: pytest.MonkeyPatch) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="claw"
        )
        and_group = _And(name="multiattack", options=(attack, attack))
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        written: list[str] = []
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        monkeypatch.setattr(sys.stdout, "write", written.append)
        _fire("wolf", and_group)
        assert len(written) == 2

    def test_fire_attack(self, monkeypatch: pytest.MonkeyPatch) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="bite"
        )
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        written: list[str] = []
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        monkeypatch.setattr(sys.stdout, "write", written.append)
        _fire("wolf", attack)
        assert any("wolf" in s and "bite" in s for s in written)

    def test_fire_or_single(self, monkeypatch: pytest.MonkeyPatch) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="scratch"
        )
        or_group = _Or(name="or_move", options=(attack,))
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        written: list[str] = []
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        monkeypatch.setattr(sys.stdout, "write", written.append)
        _fire("cat", or_group)
        assert any("scratch" in s for s in written)

    def test_fire_or_multiple(self, monkeypatch: pytest.MonkeyPatch) -> None:
        attack1 = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="claw"
        )
        attack2 = _Attack(
            n_dice=1, dice_size=8, attack_bonus=3, damage_bonus=1, name="bite"
        )
        or_group = _Or(name="multiopt", options=(attack1, attack2))
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        written: list[str] = []
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        monkeypatch.setattr(fight_module, "_pick", lambda *a, **k: 0)
        monkeypatch.setattr(sys.stdout, "write", written.append)
        _fire("monster", or_group)
        assert len(written) >= 1


@pytest.mark.unit
class TestPick:
    def test_pick_non_tty_empty_input_returns_zero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        monkeypatch.setattr("builtins.input", lambda *a, **k: "")
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_non_tty_valid_number(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        rec = _Rec("2")
        monkeypatch.setattr("builtins.input", rec)
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        result = _pick(["option1", "option2"], "Choose:")
        assert result == 1

    def test_pick_non_tty_invalid_then_valid(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
        rec = _Rec("99", "abc", "1")
        monkeypatch.setattr("builtins.input", rec)
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_tty_enter_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdin, "fileno", lambda: 0)
        monkeypatch.setattr(termios, "tcgetattr", lambda *a: [])
        monkeypatch.setattr(tty, "setraw", lambda *a: None)
        monkeypatch.setattr(termios, "tcsetattr", lambda *a: None)
        rec = _Rec("\r")
        monkeypatch.setattr(sys.stdin, "read", rec)
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        monkeypatch.setattr(sys.stdout, "flush", lambda: None)
        result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_tty_down_arrow_then_enter(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdin, "fileno", lambda: 0)
        monkeypatch.setattr(termios, "tcgetattr", lambda *a: [])
        monkeypatch.setattr(tty, "setraw", lambda *a: None)
        monkeypatch.setattr(termios, "tcsetattr", lambda *a: None)
        rec = _Rec("\x1b", "[B", "\r")
        monkeypatch.setattr(sys.stdin, "read", rec)
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        monkeypatch.setattr(sys.stdout, "flush", lambda: None)
        result = _pick(["option1", "option2"], "Choose:")
        assert result == 1

    def test_pick_tty_up_arrow_clamps_at_zero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdin, "fileno", lambda: 0)
        monkeypatch.setattr(termios, "tcgetattr", lambda *a: [])
        monkeypatch.setattr(tty, "setraw", lambda *a: None)
        monkeypatch.setattr(termios, "tcsetattr", lambda *a: None)
        rec = _Rec("\x1b", "[A", "\r")
        monkeypatch.setattr(sys.stdin, "read", rec)
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        monkeypatch.setattr(sys.stdout, "flush", lambda: None)
        result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_tty_ctrl_c_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdin, "fileno", lambda: 0)
        monkeypatch.setattr(termios, "tcgetattr", lambda *a: [])
        monkeypatch.setattr(tty, "setraw", lambda *a: None)
        monkeypatch.setattr(termios, "tcsetattr", lambda *a: None)
        rec = _Rec("\x03")
        monkeypatch.setattr(sys.stdin, "read", rec)
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        monkeypatch.setattr(sys.stdout, "flush", lambda: None)
        with pytest.raises(KeyboardInterrupt):
            _pick(["option1", "option2"], "Choose:")

    def test_pick_tty_unknown_escape_ignored(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        monkeypatch.setattr(sys.stdin, "fileno", lambda: 0)
        monkeypatch.setattr(termios, "tcgetattr", lambda *a: [])
        monkeypatch.setattr(tty, "setraw", lambda *a: None)
        monkeypatch.setattr(termios, "tcsetattr", lambda *a: None)
        rec = _Rec("\x1b", "[X", "\n")
        monkeypatch.setattr(sys.stdin, "read", rec)
        monkeypatch.setattr(sys.stdout, "write", lambda *a: None)
        monkeypatch.setattr(sys.stdout, "flush", lambda: None)
        result = _pick(["option1", "option2"], "Choose:")
        assert result == 0


@pytest.mark.unit
class TestLoadCreature:
    def test_returns_creature_unchanged(self) -> None:
        creature = _Creature.model_validate({**_CREATURE_DATA, "initiative": 10})
        assert _load_creature(creature) is creature

    def test_loads_from_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        (creatures_dir / "goblin.json").write_text(
            json.dumps({**_CREATURE_DATA, "name": "goblin", "initiative": 5})
        )
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        result = _load_creature("goblin")
        assert isinstance(result, _Creature)
        assert result.name == "goblin"

    def test_raises_on_missing_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        with pytest.raises(ValueError, match="Unknown creature type"):
            _load_creature("goblin")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="creature must be a str"):
            _load_creature(42)


@pytest.mark.unit
class TestLoadCharacter:
    def test_returns_presentable_character_unchanged(self) -> None:
        pc = PresentableCharacter.model_validate(_BASE_PC_DATA)
        assert _load_character(pc) is pc

    def test_loads_from_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        pc = PresentableCharacter.model_validate(_BASE_PC_DATA)
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        (characters_dir / "hero.json").write_text(
            json.dumps(pc.model_dump(mode="json"))
        )
        monkeypatch.setattr(fight_module, "_CHARACTER_DIR", characters_dir)
        result = _load_character("hero")
        assert isinstance(result, PresentableCharacter)
        assert result.character_data.name == "test"

    def test_raises_on_missing_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        monkeypatch.setattr(fight_module, "_CHARACTER_DIR", characters_dir)
        with pytest.raises(ValueError, match="Unknown character"):
            _load_character("hero")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="character must be a str"):
            _load_character(42)


@pytest.mark.unit
class TestRunFight:
    def test_player_turn_no_attack_output(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        (creatures_dir / "skeleton.json").write_text(
            json.dumps({**_CREATURE_DATA, "name": "skeleton", "initiative": 5})
        )
        (characters_dir / "hero.json").write_text(_pc_json("hero"))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        monkeypatch.setattr(fight_module, "_CHARACTER_DIR", characters_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate(
                    {"creature": "skeleton", "n_entities": 1}
                )
            ],
            players=[
                _PlayerEntry.model_validate({"character": "hero", "initiative": 20})
            ],
        )
        mock_input = _Rec("", "", "", "")
        monkeypatch.setattr("builtins.input", mock_input)
        mock_print = _Rec()
        monkeypatch.setattr("builtins.print", mock_print)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 2))
        cli.cli_cmd()
        printed_args = [str(call) for call in mock_print.call_args_list]
        assert not any("hero" in arg for arg in printed_args)

    def test_monster_turn_prints_attacks(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="claw"
        )
        creature_data = {
            **_CREATURE_DATA,
            "name": "wolf",
            "initiative": 5,
            "attacks": [attack.model_dump()],
        }
        (creatures_dir / "wolf.json").write_text(json.dumps(creature_data))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate({"creature": "wolf", "n_entities": 1})
            ],
            players=[],
        )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        written: list[str] = []
        mock_input = _Rec("", "")
        monkeypatch.setattr("builtins.input", mock_input)
        monkeypatch.setattr(sys.stdout, "write", written.append)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 1))
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        cli.cli_cmd()
        all_prompts = [call[0][0] for call in mock_input.call_args_list]
        assert any("wolf" in p and "moves now" in p for p in all_prompts)
        assert any("wolf [claw]" in line for line in written)

    def test_duplicate_attack_names_grouped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="claw"
        )
        creature_data = {
            **_CREATURE_DATA,
            "name": "wolf",
            "initiative": 5,
            "attacks": [attack.model_dump(), attack.model_dump()],
        }
        (creatures_dir / "wolf.json").write_text(json.dumps(creature_data))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate({"creature": "wolf", "n_entities": 1})
            ],
            players=[],
        )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        written: list[str] = []
        monkeypatch.setattr("builtins.input", _Rec("", ""))
        monkeypatch.setattr(sys.stdout, "write", written.append)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 1))
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        monkeypatch.setattr(fight_module, "_pick", lambda *a, **k: 0)
        cli.cli_cmd()
        assert any("wolf [claw]" in line for line in written)

    def test_offhand_attack_fires(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        main_attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="sword"
        )
        offhand_attack = _Attack(
            n_dice=1,
            dice_size=4,
            attack_bonus=2,
            damage_bonus=0,
            name="dagger (offhand)",
        )
        creature_data = {
            **_CREATURE_DATA,
            "name": "fighter",
            "initiative": 5,
            "attacks": [main_attack.model_dump(), offhand_attack.model_dump()],
        }
        (creatures_dir / "fighter.json").write_text(json.dumps(creature_data))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate({"creature": "fighter", "n_entities": 1})
            ],
            players=[],
        )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        written: list[str] = []
        monkeypatch.setattr("builtins.input", _Rec("", ""))
        monkeypatch.setattr(sys.stdout, "write", written.append)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 1))
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        cli.cli_cmd()
        assert any("dagger (offhand)" in line for line in written)

    def test_hp_tracking_after_player_deals_damage(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="sword"
        )
        creature_data = {
            **_CREATURE_DATA,
            "name": "goblin",
            "initiative": 1,
            "attacks": [attack.model_dump()],
        }
        (creatures_dir / "goblin.json").write_text(json.dumps(creature_data))
        (characters_dir / "hero.json").write_text(_pc_json("hero"))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        monkeypatch.setattr(fight_module, "_CHARACTER_DIR", characters_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate({"creature": "goblin", "n_entities": 1})
            ],
            players=[
                _PlayerEntry.model_validate({"character": "hero", "initiative": 20})
            ],
        )
        written: list[str] = []
        monkeypatch.setattr("builtins.input", _Rec("", "5", "", ""))
        monkeypatch.setattr(sys.stdout, "write", written.append)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 1))
        monkeypatch.setattr(fight_module, "_pick", _Rec(1, 0))
        cli.cli_cmd()
        assert any("→" in line for line in written)

    def test_hp_tracking_empty_damage_breaks_inner_loop(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="sword"
        )
        creature_data = {
            **_CREATURE_DATA,
            "name": "goblin",
            "initiative": 1,
            "attacks": [attack.model_dump()],
        }
        (creatures_dir / "goblin.json").write_text(json.dumps(creature_data))
        (characters_dir / "hero.json").write_text(_pc_json("hero"))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        monkeypatch.setattr(fight_module, "_CHARACTER_DIR", characters_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate({"creature": "goblin", "n_entities": 1})
            ],
            players=[
                _PlayerEntry.model_validate({"character": "hero", "initiative": 20})
            ],
        )
        written: list[str] = []
        monkeypatch.setattr("builtins.input", _Rec("", "", ""))
        monkeypatch.setattr(sys.stdout, "write", written.append)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 1))
        monkeypatch.setattr(fight_module, "_pick", _Rec(1, 0))
        cli.cli_cmd()
        assert written is not None

    def test_hp_tracking_invalid_damage_then_valid(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="sword"
        )
        creature_data = {
            **_CREATURE_DATA,
            "name": "goblin",
            "initiative": 1,
            "attacks": [attack.model_dump()],
        }
        (creatures_dir / "goblin.json").write_text(json.dumps(creature_data))
        (characters_dir / "hero.json").write_text(_pc_json("hero"))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        monkeypatch.setattr(fight_module, "_CHARACTER_DIR", characters_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate({"creature": "goblin", "n_entities": 1})
            ],
            players=[
                _PlayerEntry.model_validate({"character": "hero", "initiative": 20})
            ],
        )
        written: list[str] = []
        monkeypatch.setattr("builtins.input", _Rec("", "bad", "3", "", ""))
        monkeypatch.setattr(sys.stdout, "write", written.append)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 1))
        monkeypatch.setattr(fight_module, "_pick", _Rec(1, 0))
        cli.cli_cmd()
        assert any("valid number" in line for line in written)

    def test_multi_entity_index_in_prefix(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="claw"
        )
        creature_data = {
            **_CREATURE_DATA,
            "name": "wolf",
            "initiative": 5,
            "attacks": [attack.model_dump()],
        }
        (creatures_dir / "wolf.json").write_text(json.dumps(creature_data))
        monkeypatch.setattr(fight_module, "_CREATURE_DIR", creatures_dir)
        cli = _FightCli.model_construct(
            encounter=[
                _EncounterEntry.model_validate({"creature": "wolf", "n_entities": 3})
            ],
            players=[],
        )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        mock_input = _Rec("", "", "", "", "", "")
        monkeypatch.setattr("builtins.input", mock_input)
        monkeypatch.setattr("builtins.print", lambda *a, **k: None)
        monkeypatch.setattr(fight_module, "cycle", lambda it: islice(it, 3))
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        cli.cli_cmd()
        move_prompts = [
            call[0][0]
            for call in mock_input.call_args_list
            if "moves now" in call[0][0]
        ]
        assert len(move_prompts) == 3
        assert "wolf 1" in move_prompts[0]
        assert "wolf 2" in move_prompts[1]
        assert "wolf 3" in move_prompts[2]
