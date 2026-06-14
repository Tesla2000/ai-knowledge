import json
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
from dnd.fight._attack import _Attack
from dnd.fight._attack_result import _AttackResult
from dnd.fight._creature import _Creature, _PlayerFightCreature
from dnd.fight._multi_attack import _MultiAttack
from dnd.fight._saving_throw import _SavingThrow
from dnd.fight._saving_throw_result import _SavingThrowResult
from dnd.fight._spell_attack import _SpellAttack
from dnd.fight.__main__ import (
    _EncounterEntry,
    _FightCli,
    _PlayerEntry,
    _load_character,
    _load_creature,
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


class TestAttack:
    # n_dice=2: 2 rolls + 2 damage dice + 4 crit dice = 8 randint calls
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
        # roll1=20(crit), roll2=10, 2 damage dice, 4 crit dice
        with patch.object(
            attack_module, "randint", side_effect=[20, 10, 3, 4, 2, 1, 3, 2]
        ):
            result = self._attack.perform()
        assert result.first_roll == "critical"
        assert result.second_roll == 13

    def test_perform_second_roll_critical(self) -> None:
        # roll1=10, roll2=20(crit), 2 damage dice, 4 crit dice
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


class _FloatBonusCreature(_Creature):
    initiative_bonus: float = 21.37  # type: ignore[assignment]


class _IntNameCreature(_Creature):
    name: int = 0  # type: ignore[assignment]


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
            _Creature.model_validate({**_BASE_DATA, "attacks": [], "initiative": 1})


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
        with patch("dnd.fight.__main__._CREATURE_DIR", creatures_dir):
            result = _load_creature("goblin")
        assert isinstance(result, _Creature)
        assert result.name == "goblin"

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        with patch("dnd.fight.__main__._CREATURE_DIR", creatures_dir):
            with pytest.raises(ValueError, match="Unknown creature type"):
                _load_creature("goblin")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="creature must be a str"):
            _load_creature(42)


class TestLoadCharacter:
    def test_returns_creature_base_unchanged(self) -> None:
        base = _CreatureBase.model_validate(_BASE_DATA)
        assert _load_character(base) is base

    def test_loads_from_file(self, tmp_path: Path) -> None:
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        (characters_dir / "hero.json").write_text(json.dumps(_BASE_DATA))
        with patch("dnd.fight.__main__._CHARACTER_DIR", characters_dir):
            result = _load_character("hero")
        assert isinstance(result, _CreatureBase)
        assert result.name == "test"

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        with patch("dnd.fight.__main__._CHARACTER_DIR", characters_dir):
            with pytest.raises(ValueError, match="Unknown character"):
                _load_character("hero")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="character must be a str"):
            _load_character(42)


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
            patch("dnd.fight.__main__._CREATURE_DIR", creatures_dir),
            patch("dnd.fight.__main__._CHARACTER_DIR", characters_dir),
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
            patch("builtins.input"),
            patch("builtins.print") as mock_print,
            patch("dnd.fight.__main__.cycle", side_effect=lambda it: islice(it, 2)),
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
            **_BASE_DATA,
            "name": "wolf",
            "initiative": 5,
            "attacks": [attack.model_dump()],
        }
        (creatures_dir / "wolf.json").write_text(json.dumps(creature_data))
        with patch("dnd.fight.__main__._CREATURE_DIR", creatures_dir):
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
        with (
            patch("builtins.input") as mock_input,
            patch("builtins.print") as mock_print,
            patch("dnd.fight.__main__.cycle", side_effect=lambda it: islice(it, 1)),
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
        ):
            cli.cli_cmd()
        assert mock_input.call_args[0][0] == "wolf moves now..."
        first_call_args = mock_print.call_args_list[0][0]
        assert first_call_args[0] == "wolf attacked with claw"

    def test_multi_entity_index_in_prefix(self, tmp_path: Path) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        attack = _Attack(
            n_dice=1, dice_size=6, attack_bonus=2, damage_bonus=1, name="claw"
        )
        creature_data = {
            **_BASE_DATA,
            "name": "wolf",
            "initiative": 5,
            "attacks": [attack.model_dump()],
        }
        (creatures_dir / "wolf.json").write_text(json.dumps(creature_data))
        with patch("dnd.fight.__main__._CREATURE_DIR", creatures_dir):
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
            patch("builtins.input") as mock_input,
            patch("builtins.print"),
            patch("dnd.fight.__main__.cycle", side_effect=lambda it: islice(it, 3)),
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
        ):
            cli.cli_cmd()
        prompts = [call[0][0] for call in mock_input.call_args_list]
        assert prompts == [
            "wolf 1 moves now...",
            "wolf 2 moves now...",
            "wolf 3 moves now...",
        ]
