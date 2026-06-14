import json
from itertools import cycle
from pathlib import Path
from typing import Annotated, ClassVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, PositiveInt
from pydantic_settings import BaseSettings, CliApp, SettingsConfigDict

from dnd.character._creature_base import _CreatureBase
from dnd.fight._creature import _Creature, _PlayerFightCreature

_DATA_DIR = Path(__file__).parent / "data"
_CREATURE_DIR = _DATA_DIR / "creatures"
_CHARACTER_DIR = _DATA_DIR / "characters"


def _load_creature(value: object) -> _Creature:
    if isinstance(value, _Creature):
        return value
    if not isinstance(value, str):
        raise ValueError(f"creature must be a str creature type, got {type(value)}")
    path = _CREATURE_DIR / f"{value}.json"
    if not path.exists():
        raise ValueError(
            f"Unknown creature type '{value}'. Available: {[p.stem for p in _CREATURE_DIR.glob('*.json')]}"
        )
    return _Creature.model_validate(json.loads(path.read_text()))


def _load_character(value: object) -> _CreatureBase:
    if isinstance(value, _CreatureBase):
        return value
    if not isinstance(value, str):
        raise ValueError(f"character must be a str name, got {type(value)}")
    path = _CHARACTER_DIR / f"{value}.json"
    if not path.exists():
        raise ValueError(
            f"Unknown character '{value}'. Available: {[p.stem for p in _CHARACTER_DIR.glob('*.json')]}"
        )
    return _CreatureBase.model_validate(json.loads(path.read_text()))


class _EncounterEntry(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    creature: Annotated[_Creature, BeforeValidator(_load_creature)]
    n_entities: PositiveInt


class _PlayerEntry(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    character: Annotated[_CreatureBase, BeforeValidator(_load_character)]
    initiative: int


class _FightCli(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        cli_parse_args=True,
        cli_kebab_case=True,
    )

    encounter: list[_EncounterEntry]
    players: list[_PlayerEntry]

    def cli_cmd(self) -> None:
        monsters: tuple[tuple[int | None, _Creature], ...] = tuple(
            (i + 1 if entry.n_entities > 1 else None, entry.creature)
            for entry in self.encounter
            for i in range(entry.n_entities)
        )
        player_combatants: tuple[tuple[None, _PlayerFightCreature], ...] = tuple(
            (
                None,
                _PlayerFightCreature(
                    initiative=p.initiative, **p.character.model_dump()
                ),
            )
            for p in self.players
        )
        all_combatants: tuple[
            tuple[int | None, _Creature | _PlayerFightCreature], ...
        ] = monsters + player_combatants
        for index, creature in cycle(
            sorted(all_combatants, key=lambda ic: -ic[1].initiative)
        ):
            prefix = f"{creature.name} {index}" if index is not None else creature.name
            input(f"{prefix} moves now...")
            if isinstance(creature, _Creature):
                for attack in creature.attacks:
                    print(f"{prefix} attacked with {attack.name}", attack.perform())


if __name__ == "__main__":  # pragma: no cover
    CliApp.run(_FightCli)
