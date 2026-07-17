import json
import sys
from collections.abc import Callable, Iterator
from functools import partial
from itertools import islice
from pathlib import Path

import pytest

import scripts.fight as fight_script
from dnd.character.presentable_character import PresentableCharacter
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


@pytest.mark.integration
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
        monkeypatch.setattr(fight_script, "_CREATURE_DIR", creatures_dir)
        result = _load_creature("goblin")
        assert isinstance(result, _Creature)
        assert result.name == "goblin"

    def test_raises_on_missing_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        creatures_dir = tmp_path / "creatures"
        creatures_dir.mkdir()
        monkeypatch.setattr(fight_script, "_CREATURE_DIR", creatures_dir)
        with pytest.raises(ValueError, match="Unknown creature type"):
            _load_creature("goblin")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="creature must be a str"):
            _load_creature(42)


@pytest.mark.integration
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
        monkeypatch.setattr(fight_script, "_CHARACTER_DIR", characters_dir)
        result = _load_character("hero")
        assert isinstance(result, PresentableCharacter)
        assert result.character_data.name == "test"

    def test_raises_on_missing_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        characters_dir = tmp_path / "characters"
        characters_dir.mkdir()
        monkeypatch.setattr(fight_script, "_CHARACTER_DIR", characters_dir)
        with pytest.raises(ValueError, match="Unknown character"):
            _load_character("hero")

    def test_raises_on_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="character must be a str"):
            _load_character(42)


@pytest.mark.integration
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
        monkeypatch.setattr(fight_script, "_CREATURE_DIR", creatures_dir)
        monkeypatch.setattr(fight_script, "_CHARACTER_DIR", characters_dir)
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
        monkeypatch.setattr("builtins.input", _Rec("", "", "", ""))
        mock_print = _Rec()
        monkeypatch.setattr("builtins.print", mock_print)
        monkeypatch.setattr(fight_script, "cycle", lambda it: islice(it, 2))
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
        monkeypatch.setattr(fight_script, "_CREATURE_DIR", creatures_dir)
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
        monkeypatch.setattr(fight_script, "cycle", lambda it: islice(it, 1))
        monkeypatch.setattr(_Attack, _Attack.perform.__name__, lambda self: mock_result)
        cli.cli_cmd()
        all_prompts = [call[0][0] for call in mock_input.call_args_list]
        assert any("wolf" in p and "moves now" in p for p in all_prompts)
        assert any("wolf [claw]" in line for line in written)

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
        monkeypatch.setattr(fight_script, "_CREATURE_DIR", creatures_dir)
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
        monkeypatch.setattr(fight_script, "cycle", lambda it: islice(it, 3))
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
