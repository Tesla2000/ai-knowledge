import json
from itertools import islice
from pathlib import Path
from unittest.mock import patch

import pytest

from dnd.character._creature_base import _CreatureBase
from dnd.character.stats import Stats
from dnd.fight._attack import _Attack
from dnd.fight._attack_result import _AttackResult
from dnd.fight._creature import _Creature
from scripts.fight import (
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


@pytest.mark.integration
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


@pytest.mark.integration
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


@pytest.mark.integration
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
            patch("builtins.input", side_effect=["", "", "", ""]),
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
            **_CREATURE_DATA,
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
        written: list[str] = []
        with (
            patch("builtins.input", side_effect=["", ""]) as mock_input,
            patch("sys.stdout.write", side_effect=written.append),
            patch("dnd.fight.__main__.cycle", side_effect=lambda it: islice(it, 1)),
            patch.object(_Attack, _Attack.perform.__name__, return_value=mock_result),
        ):
            cli.cli_cmd()
        all_prompts = [call[0][0] for call in mock_input.call_args_list]
        assert any("wolf" in p and "moves now" in p for p in all_prompts)
        assert any("wolf [claw]" in line for line in written)

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
            patch("builtins.input", side_effect=["", "", "", "", "", ""]) as mock_input,
            patch("builtins.print"),
            patch("dnd.fight.__main__.cycle", side_effect=lambda it: islice(it, 3)),
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
