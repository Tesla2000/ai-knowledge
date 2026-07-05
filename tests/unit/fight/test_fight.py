import json
import sys
from itertools import islice
from pathlib import Path
from unittest.mock import patch

import pytest

import dnd.fight._attack as attack_module
import dnd.fight._creature as creature_module
import dnd.fight._saving_throw as saving_throw_module
import dnd.fight._spell_attack as spell_attack_module
from dnd.character._creature_base import _CreatureBase
from dnd.character.stats import Stats
from dnd.choices.stats_creation.statistic import Statistic
from dnd.fight._action_group import _And, _Or
from dnd.fight._attack import _Attack
from dnd.fight._attack_result import _AttackResult
from dnd.fight._creature import _Creature, _PlayerFightCreature
from dnd.fight._multi_attack import _MultiAttack
from dnd.fight._non_attack import _NonAttack
from dnd.fight._saving_throw import _SavingThrow
from dnd.fight._saving_throw_result import _SavingThrowResult
from dnd.fight._spell_attack import _SpellAttack
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

    def test_perform_normal_rolls(self) -> None:
        with patch.object(
            attack_module, "randint", side_effect=[10, 15, 4, 3, 2, 1, 3, 2]
        ):
            result = self._attack.perform()
        assert result.first_roll == 13
        assert result.second_roll == 18
        assert isinstance(result, _AttackResult)

    def test_perform_first_roll_critical(self) -> None:
        with patch.object(
            attack_module, "randint", side_effect=[20, 10, 3, 4, 2, 1, 3, 2]
        ):
            result = self._attack.perform()
        assert result.first_roll == "critical"
        assert result.second_roll == 13

    def test_perform_second_roll_critical(self) -> None:
        with patch.object(
            attack_module, "randint", side_effect=[10, 20, 3, 4, 2, 1, 3, 2]
        ):
            result = self._attack.perform()
        assert result.first_roll == 13
        assert result.second_roll == "critical"

    def test_perform_both_critical(self) -> None:
        with patch.object(
            attack_module, "randint", side_effect=[20, 20, 3, 4, 2, 1, 3, 2]
        ):
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
    def test_perform_half_on_success(self) -> None:
        st = _SavingThrow(
            n_dice=2,
            dice_size=6,
            damage_bonus=0,
            dc=15,
            name="fireball",
            saving_throw_type=Statistic.DEXTERITY,
            half_on_success=True,
        )
        with patch.object(saving_throw_module, "randint", side_effect=[4, 4]):
            result = st.perform()
        assert isinstance(result, _SavingThrowResult)
        assert result.dc == 15
        assert result.saving_throw_type == Statistic.DEXTERITY
        assert result.damage_on_fail == 8
        assert result.damage_on_success == 4

    def test_perform_no_half_on_success(self) -> None:
        st = _SavingThrow(
            n_dice=1,
            dice_size=8,
            damage_bonus=2,
            dc=13,
            name="poison",
            saving_throw_type=Statistic.CONSTITUTION,
            half_on_success=False,
        )
        with patch.object(saving_throw_module, "randint", side_effect=[6]):
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
    def test_perform_calls_each_attack(self) -> None:
        attack1 = _Attack(n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1)
        attack2 = _Attack(n_dice=1, dice_size=8, attack_bonus=3, damage_bonus=2)
        multi = _MultiAttack(attacks=(attack1, attack2))
        mock_result = _AttackResult(
            first_roll=10, second_roll=15, damage=5, crit_damage=8
        )
        with patch.object(
            _Attack, _Attack.perform.__name__, return_value=mock_result
        ) as mock_perform:
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

    def test_perform_returns_one_result_per_level(self) -> None:
        with patch.object(spell_attack_module, "randint", return_value=10):
            results = self._spell.perform()
        assert len(results) == 3

    def test_perform_at_level_critical(self) -> None:
        with patch.object(
            spell_attack_module, "randint", side_effect=[20, 10, 3, 4, 2]
        ):
            result = self._spell._perform_at_level(1)
        assert result.first_roll == "critical"
        assert result.second_roll == 15

    def test_perform_at_level_second_critical(self) -> None:
        with patch.object(
            spell_attack_module, "randint", side_effect=[10, 20, 3, 4, 2, 1]
        ):
            result = self._spell._perform_at_level(1)
        assert result.first_roll == 15
        assert result.second_roll == "critical"

    def test_extra_dice_scale_with_level(self) -> None:
        with patch.object(spell_attack_module, "randint", return_value=3):
            result_l1 = self._spell._perform_at_level(1)
            result_l2 = self._spell._perform_at_level(2)
        assert result_l2.damage > result_l1.damage


@pytest.mark.unit
class TestCreatureInit:
    def test_roll_initiative_with_bonus(self) -> None:
        with patch.object(creature_module, "randint", return_value=10):
            creature = _Creature.model_validate(
                {**_CREATURE_DATA, "initiative_bonus": 5}
            )
        assert creature.initiative == 15

    def test_roll_initiative_invalid_bonus_type(self) -> None:
        with pytest.raises(ValueError, match="initiative_bonus must be int"):
            _FloatBonusCreature.model_validate(
                {**_CREATURE_DATA, "initiative_bonus": 21.37}
            )

    def test_default_type_uses_name(self) -> None:
        with patch.object(creature_module, "randint", return_value=1):
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


@pytest.mark.unit
class TestPlayerFightCreature:
    def test_construction(self) -> None:
        player = _PlayerFightCreature(
            name="test",
            stats=_STATS,
            speed=30,
            dark_vision_range=0,
            initiative_bonus=2,
            saving_throw_proficiencies=(),
            other_active_abilities=(),
            initiative=14,
        )
        assert player.name == "test"
        assert player.initiative == 14


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

    def test_or_perform(self) -> None:
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        with patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result):
            result = _Or(options=(self._attack,)).perform()
        assert result == mock_result

    def test_and_perform(self) -> None:
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        with patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result):
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

    def test_select_multiple_options(self) -> None:
        attack1 = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="claw"
        )
        attack2 = _Attack(
            n_dice=1, dice_size=8, attack_bonus=3, damage_bonus=1, name="bite"
        )
        with patch("scripts.fight._pick", return_value=1):
            result = _select((attack1, attack2), "Choose")
        assert result is attack2

    def test_fire_non_attack(self) -> None:
        na = _NonAttack(name="Roar", description="loud noise")
        written: list[str] = []
        with patch("sys.stdout.write", side_effect=written.append):
            _fire("monster", na)
        assert any("Roar" in s and "loud noise" in s for s in written)

    def test_fire_and(self) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="claw"
        )
        and_group = _And(name="multiattack", options=(attack, attack))
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        written: list[str] = []
        with (
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
            patch("sys.stdout.write", side_effect=written.append),
        ):
            _fire("wolf", and_group)
        assert len(written) == 2

    def test_fire_attack(self) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="bite"
        )
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        written: list[str] = []
        with (
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
            patch("sys.stdout.write", side_effect=written.append),
        ):
            _fire("wolf", attack)
        assert any("wolf" in s and "bite" in s for s in written)

    def test_fire_or_single(self) -> None:
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=0, name="scratch"
        )
        or_group = _Or(name="or_move", options=(attack,))
        mock_result = _AttackResult(
            first_roll=10, second_roll=8, damage=4, crit_damage=0
        )
        written: list[str] = []
        with (
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
            patch("sys.stdout.write", side_effect=written.append),
        ):
            _fire("cat", or_group)
        assert any("scratch" in s for s in written)

    def test_fire_or_multiple(self) -> None:
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
        with (
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
            patch("scripts.fight._pick", return_value=0),
            patch("sys.stdout.write", side_effect=written.append),
        ):
            _fire("monster", or_group)
        assert len(written) >= 1


@pytest.mark.unit
class TestPick:
    def test_pick_non_tty_empty_input_returns_zero(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=False),
            patch("builtins.input", return_value=""),
            patch("sys.stdout.write"),
        ):
            result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_non_tty_valid_number(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=False),
            patch("builtins.input", side_effect=["2"]),
            patch("sys.stdout.write"),
        ):
            result = _pick(["option1", "option2"], "Choose:")
        assert result == 1

    def test_pick_non_tty_invalid_then_valid(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=False),
            patch("builtins.input", side_effect=["99", "abc", "1"]),
            patch("sys.stdout.write"),
        ):
            result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_tty_enter_key(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=True),
            patch.object(sys.stdin, "fileno", return_value=0),
            patch("termios.tcgetattr", return_value=[]),
            patch("tty.setraw"),
            patch("termios.tcsetattr"),
            patch.object(sys.stdin, "read", side_effect=["\r"]),
            patch("sys.stdout.write"),
            patch("sys.stdout.flush"),
        ):
            result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_tty_down_arrow_then_enter(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=True),
            patch.object(sys.stdin, "fileno", return_value=0),
            patch("termios.tcgetattr", return_value=[]),
            patch("tty.setraw"),
            patch("termios.tcsetattr"),
            patch.object(sys.stdin, "read", side_effect=["\x1b", "[B", "\r"]),
            patch("sys.stdout.write"),
            patch("sys.stdout.flush"),
        ):
            result = _pick(["option1", "option2"], "Choose:")
        assert result == 1

    def test_pick_tty_up_arrow_clamps_at_zero(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=True),
            patch.object(sys.stdin, "fileno", return_value=0),
            patch("termios.tcgetattr", return_value=[]),
            patch("tty.setraw"),
            patch("termios.tcsetattr"),
            patch.object(sys.stdin, "read", side_effect=["\x1b", "[A", "\r"]),
            patch("sys.stdout.write"),
            patch("sys.stdout.flush"),
        ):
            result = _pick(["option1", "option2"], "Choose:")
        assert result == 0

    def test_pick_tty_ctrl_c_raises(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=True),
            patch.object(sys.stdin, "fileno", return_value=0),
            patch("termios.tcgetattr", return_value=[]),
            patch("tty.setraw"),
            patch("termios.tcsetattr"),
            patch.object(sys.stdin, "read", side_effect=["\x03"]),
            patch("sys.stdout.write"),
            patch("sys.stdout.flush"),
        ):
            with pytest.raises(KeyboardInterrupt):
                _pick(["option1", "option2"], "Choose:")

    def test_pick_tty_unknown_escape_ignored(self) -> None:
        with (
            patch.object(sys.stdin, "isatty", return_value=True),
            patch.object(sys.stdin, "fileno", return_value=0),
            patch("termios.tcgetattr", return_value=[]),
            patch("tty.setraw"),
            patch("termios.tcsetattr"),
            patch.object(sys.stdin, "read", side_effect=["\x1b", "[X", "\n"]),
            patch("sys.stdout.write"),
            patch("sys.stdout.flush"),
        ):
            result = _pick(["option1", "option2"], "Choose:")
        assert result == 0


@pytest.mark.unit
class TestLoadCreature:
    def test_returns_creature_unchanged(self) -> None:
        creature = _Creature.model_validate({**_CREATURE_DATA, "initiative": 10})
        assert _load_creature(creature) is creature

    def test_loads_from_file(self, tmp_path: Path) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        (creatures_dir / "goblin.json").write_text(
            json.dumps({**_CREATURE_DATA, "name": "goblin", "initiative": 5})
        )
        with patch("scripts.fight._CREATURE_DIR", creatures_dir):
            result = _load_creature("goblin")
        assert isinstance(result, _Creature)
        assert result.name == "goblin"

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        with patch("scripts.fight._CREATURE_DIR", creatures_dir):
            with pytest.raises(ValueError, match="Unknown creature type"):
                _load_creature("goblin")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="creature must be a str"):
            _load_creature(42)


@pytest.mark.unit
class TestLoadCharacter:
    def test_returns_creature_base_unchanged(self) -> None:
        base = _CreatureBase.model_validate(_BASE_DATA)
        assert _load_character(base) is base

    def test_loads_from_file(self, tmp_path: Path) -> None:
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        (characters_dir / "hero.json").write_text(json.dumps(_BASE_DATA))
        with patch("scripts.fight._CHARACTER_DIR", characters_dir):
            result = _load_character("hero")
        assert isinstance(result, _CreatureBase)
        assert result.name == "test"

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        with patch("scripts.fight._CHARACTER_DIR", characters_dir):
            with pytest.raises(ValueError, match="Unknown character"):
                _load_character("hero")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="character must be a str"):
            _load_character(42)


@pytest.mark.unit
class TestRunFight:
    def test_player_turn_no_attack_output(self, tmp_path: Path) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        (creatures_dir / "skeleton.json").write_text(
            json.dumps({**_CREATURE_DATA, "name": "skeleton", "initiative": 5})
        )
        (characters_dir / "hero.json").write_text(
            json.dumps({**_BASE_DATA, "name": "hero"})
        )
        with (
            patch("scripts.fight._CREATURE_DIR", creatures_dir),
            patch("scripts.fight._CHARACTER_DIR", characters_dir),
        ):
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
        with (
            patch("builtins.input", side_effect=["", "", "", ""]),
            patch("builtins.print") as mock_print,
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 2)),
        ):
            cli.cli_cmd()
        printed_args = [str(call) for call in mock_print.call_args_list]
        assert not any("hero" in arg for arg in printed_args)

    def test_monster_turn_prints_attacks(self, tmp_path: Path) -> None:
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
        with patch("scripts.fight._CREATURE_DIR", creatures_dir):
            cli = _FightCli.model_construct(
                encounter=[
                    _EncounterEntry.model_validate(
                        {"creature": "wolf", "n_entities": 1}
                    )
                ],
                players=[],
            )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        written: list[str] = []
        with (
            patch("builtins.input", side_effect=["", ""]) as mock_input,
            patch("sys.stdout.write", side_effect=written.append),
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 1)),
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
        ):
            cli.cli_cmd()
        all_prompts = [call[0][0] for call in mock_input.call_args_list]
        assert any("wolf" in p and "moves now" in p for p in all_prompts)
        assert any("wolf [claw]" in line for line in written)

    def test_duplicate_attack_names_grouped(self, tmp_path: Path) -> None:
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
        with patch("scripts.fight._CREATURE_DIR", creatures_dir):
            cli = _FightCli.model_construct(
                encounter=[
                    _EncounterEntry.model_validate(
                        {"creature": "wolf", "n_entities": 1}
                    )
                ],
                players=[],
            )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        written: list[str] = []
        with (
            patch("builtins.input", side_effect=["", ""]),
            patch("sys.stdout.write", side_effect=written.append),
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 1)),
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
            patch("scripts.fight._pick", return_value=0),
        ):
            cli.cli_cmd()
        assert any("wolf [claw]" in line for line in written)

    def test_offhand_attack_fires(self, tmp_path: Path) -> None:
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
        with patch("scripts.fight._CREATURE_DIR", creatures_dir):
            cli = _FightCli.model_construct(
                encounter=[
                    _EncounterEntry.model_validate(
                        {"creature": "fighter", "n_entities": 1}
                    )
                ],
                players=[],
            )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        written: list[str] = []
        with (
            patch("builtins.input", side_effect=["", ""]),
            patch("sys.stdout.write", side_effect=written.append),
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 1)),
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
        ):
            cli.cli_cmd()
        assert any("dagger (offhand)" in line for line in written)

    def test_hp_tracking_after_player_deals_damage(self, tmp_path: Path) -> None:
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
        (characters_dir / "hero.json").write_text(
            json.dumps({**_BASE_DATA, "name": "hero"})
        )
        with (
            patch("scripts.fight._CREATURE_DIR", creatures_dir),
            patch("scripts.fight._CHARACTER_DIR", characters_dir),
        ):
            cli = _FightCli.model_construct(
                encounter=[
                    _EncounterEntry.model_validate(
                        {"creature": "goblin", "n_entities": 1}
                    )
                ],
                players=[
                    _PlayerEntry.model_validate({"character": "hero", "initiative": 20})
                ],
            )
        written: list[str] = []
        with (
            patch("builtins.input", side_effect=["", "5", "", ""]),
            patch("sys.stdout.write", side_effect=written.append),
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 1)),
            patch("scripts.fight._pick", side_effect=[1, 0]),
        ):
            cli.cli_cmd()
        assert any("→" in line for line in written)

    def test_hp_tracking_empty_damage_breaks_inner_loop(self, tmp_path: Path) -> None:
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
        (characters_dir / "hero.json").write_text(
            json.dumps({**_BASE_DATA, "name": "hero"})
        )
        with (
            patch("scripts.fight._CREATURE_DIR", creatures_dir),
            patch("scripts.fight._CHARACTER_DIR", characters_dir),
        ):
            cli = _FightCli.model_construct(
                encounter=[
                    _EncounterEntry.model_validate(
                        {"creature": "goblin", "n_entities": 1}
                    )
                ],
                players=[
                    _PlayerEntry.model_validate({"character": "hero", "initiative": 20})
                ],
            )
        written: list[str] = []
        with (
            patch("builtins.input", side_effect=["", "", ""]),
            patch("sys.stdout.write", side_effect=written.append),
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 1)),
            patch("scripts.fight._pick", side_effect=[1, 0]),
        ):
            cli.cli_cmd()
        assert written is not None

    def test_hp_tracking_invalid_damage_then_valid(self, tmp_path: Path) -> None:
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
        (characters_dir / "hero.json").write_text(
            json.dumps({**_BASE_DATA, "name": "hero"})
        )
        with (
            patch("scripts.fight._CREATURE_DIR", creatures_dir),
            patch("scripts.fight._CHARACTER_DIR", characters_dir),
        ):
            cli = _FightCli.model_construct(
                encounter=[
                    _EncounterEntry.model_validate(
                        {"creature": "goblin", "n_entities": 1}
                    )
                ],
                players=[
                    _PlayerEntry.model_validate({"character": "hero", "initiative": 20})
                ],
            )
        written: list[str] = []
        with (
            patch("builtins.input", side_effect=["", "bad", "3", "", ""]),
            patch("sys.stdout.write", side_effect=written.append),
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 1)),
            patch("scripts.fight._pick", side_effect=[1, 0]),
        ):
            cli.cli_cmd()
        assert any("valid number" in line for line in written)

    def test_multi_entity_index_in_prefix(self, tmp_path: Path) -> None:
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
        with patch("scripts.fight._CREATURE_DIR", creatures_dir):
            cli = _FightCli.model_construct(
                encounter=[
                    _EncounterEntry.model_validate(
                        {"creature": "wolf", "n_entities": 3}
                    )
                ],
                players=[],
            )
        mock_result = _AttackResult(
            first_roll=12, second_roll=8, damage=5, crit_damage=9
        )
        with (
            patch("builtins.input", side_effect=["", "", "", "", "", ""]) as mock_input,
            patch("builtins.print"),
            patch("scripts.fight.cycle", side_effect=lambda it: islice(it, 3)),
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
        ):
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
