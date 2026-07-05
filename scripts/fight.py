import sys
import json
import termios
import tty
from itertools import cycle
from pathlib import Path
from typing import Annotated, ClassVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, PositiveInt
from pydantic_settings import BaseSettings, CliApp, SettingsConfigDict

from dnd.character._creature_base import _CreatureBase
from dnd.fight._action_group import _Action, _And, _Or
from dnd.fight._attack import _Attack
from dnd.fight._creature import _Creature, _PlayerFightCreature
from dnd.fight._non_attack import _NonAttack
from dnd.fight._saving_throw import _SavingThrow

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
        raise ValueError(f"character must be a str name, got {type(value).__name__}")
    path = _CHARACTER_DIR / f"{value}.json"
    if not path.exists():
        raise ValueError(
            f"Unknown character '{value}'. Available: {[p.stem for p in _CHARACTER_DIR.glob('*.json')]}"
        )
    return _CreatureBase.model_validate(json.loads(path.read_text()))


def _dmg(n_dice: int, dice_size: int, damage_bonus: int) -> str:
    base = f"{n_dice}d{dice_size}"
    if damage_bonus > 0:
        return f"{base}+{damage_bonus}"
    if damage_bonus < 0:
        return f"{base}{damage_bonus}"
    return base


def _stats(action: _Action | _NonAttack | _Or | _And) -> str:
    if isinstance(action, _NonAttack):
        return action.description
    if isinstance(action, _SavingThrow):
        half = ", half on save" if action.half_on_success else ""
        return (
            f"DC {action.dc} {action.saving_throw_type.value}"
            f"{half} | {_dmg(action.n_dice, action.dice_size, action.damage_bonus)}"
        )
    if isinstance(action, _Attack):
        return (
            f"+{action.attack_bonus} to hit"
            f" | {_dmg(action.n_dice, action.dice_size, action.damage_bonus)}"
        )
    if isinstance(action, _And):
        return f"{len(action.options)} attacks"
    return f"{len(action.options)} options"


def _describe(action: _Action | _NonAttack | _Or | _And) -> str:
    if isinstance(action, _NonAttack):
        return action.name or "(action)"
    name = action.name or ("Multiattack" if isinstance(action, _And) else "One of")
    return f"{name} | {_stats(action)}"


def _pick(items: list[str], label: str) -> int:
    """Arrow-key selection menu; returns 0-based index."""
    n = len(items)
    idx = 0

    def _draw(current: int) -> None:
        for i, item in enumerate(items):
            if i == current:
                sys.stdout.write(f"\r\033[7m  {item}\033[0m\033[K\n")
            else:
                sys.stdout.write(f"\r  {item}\033[K\n")
        sys.stdout.flush()

    if not sys.stdin.isatty():
        for i, item in enumerate(items, 1):
            sys.stdout.write(f"  {i}. {item}\n")
        while True:
            raw = input(f"{label} (1-{n}): ").strip()
            if not raw:
                return 0
            if raw.isdigit() and 1 <= int(raw) <= n:
                return int(raw) - 1
            sys.stdout.write(f"  Enter a number between 1 and {n}.\n")

    sys.stdout.write(f"{label}:\n")
    _draw(idx)

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == "\x03":
                raise KeyboardInterrupt
            if ch == "\x1b":
                nxt = sys.stdin.read(2)
                if nxt == "[A":
                    idx = max(0, idx - 1)
                elif nxt == "[B":
                    idx = min(n - 1, idx + 1)
            elif ch in ("\r", "\n"):
                break
            sys.stdout.write(f"\x1b[{n}F")
            _draw(idx)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    return idx


def _select(
    options: tuple[_Action | _NonAttack | _Or | _And, ...],
    label: str,
) -> _Action | _NonAttack | _Or | _And:
    if len(options) == 1:
        return options[0]
    return options[_pick([_describe(opt) for opt in options], label)]


def _fire(prefix: str, action: _Action | _NonAttack | _Or | _And) -> None:
    if isinstance(action, _NonAttack):
        sys.stdout.write(f"{prefix} [{action.name}]: {action.perform()}\n")
    elif isinstance(action, _And):
        for sub, result in zip(action.options, action.perform()):
            sys.stdout.write(f"{prefix} [{sub.name}]: {result}\n")
    elif isinstance(action, _Or):
        or_options = action.options
        if len(or_options) == 1:
            sub_action = or_options[0]
        else:
            sub_action = or_options[
                _pick(
                    [_describe(opt) for opt in or_options],
                    action.name or prefix,
                )
            ]
        sys.stdout.write(f"{prefix} [{sub_action.name}]: {sub_action.perform()}\n")
    else:
        sys.stdout.write(f"{prefix} [{action.name}]: {action.perform()}\n")


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
        turn_order: list[tuple[int | None, _Creature | _PlayerFightCreature]] = sorted(
            all_combatants, key=lambda ic: -ic[1].initiative
        )
        monster_prefixes: list[str] = [
            f"{c.name} {i}" if i is not None else c.name
            for i, c in turn_order
            if isinstance(c, _Creature)
        ]
        player_prefixes: list[str] = [
            c.name for i, c in turn_order if not isinstance(c, _Creature)
        ]
        hp: dict[str, int] = {}
        max_hp: dict[str, int] = {}
        for idx, c in turn_order:
            if isinstance(c, _Creature):
                pfx = f"{c.name} {idx}" if idx is not None else c.name
                hp[pfx] = c.hp
                max_hp[pfx] = c.hp
        if hp:
            sys.stdout.write("--- Enemies ---\n")
            for pfx, h in hp.items():
                sys.stdout.write(f"  {pfx}: {h} HP\n")
        player_damage: dict[str, int] = {pfx: 0 for pfx in player_prefixes}
        for index, creature in cycle(turn_order):
            prefix = f"{creature.name} {index}" if index is not None else creature.name
            if isinstance(creature, _Creature):
                status = f"{hp[prefix]}/{max_hp[prefix]}"
            else:
                status = f"dealt: {player_damage[prefix]}"
            input(f"\n{prefix} ({status}) moves now...")
            if isinstance(creature, _Creature):
                offhand: list[_Action | _NonAttack | _Or | _And] = []
                main: list[_Action | _NonAttack | _Or | _And] = []
                for a in creature.attacks:
                    (offhand if "(offhand)" in a.name else main).append(a)
                groups: dict[str, list[_Action | _NonAttack | _Or | _And]] = {}
                menu: list[_Action | _NonAttack | _Or | _And] = []
                for a in main:
                    key = a.name if a.name else str(id(a))
                    if key in groups:
                        groups[key].append(a)
                    else:
                        groups[key] = [a]
                        menu.append(a)
                chosen = _select(tuple(menu), f"Choose action for {prefix}")
                chosen_key = chosen.name if chosen.name else str(id(chosen))
                for a in groups[chosen_key]:
                    _fire(prefix, a)
                for a in offhand:
                    _fire(prefix, a)
            if monster_prefixes:
                while True:
                    hit_options = ["-- done --"] + [
                        f"{p}  {hp[p]}/{max_hp[p]}" for p in monster_prefixes
                    ]
                    target_idx = _pick(hit_options, "Who was hit?")
                    if target_idx == 0:
                        break
                    target = monster_prefixes[target_idx - 1]
                    while True:
                        dmg_raw = input(f"  Damage to {target}: ").strip()
                        if not dmg_raw:
                            break
                        try:
                            dmg = int(dmg_raw)
                            prev = hp[target]
                            hp[target] -= dmg
                            sys.stdout.write(
                                f"  {target}: {prev}/{max_hp[target]}"
                                f" → {hp[target]}/{max_hp[target]}\n"
                            )
                            if prefix in player_damage:
                                player_damage[prefix] += dmg
                                sys.stdout.write(
                                    f"  {prefix} total dealt: {player_damage[prefix]}\n"
                                )
                            break
                        except ValueError:
                            sys.stdout.write("  Enter a valid number.\n")


if __name__ == "__main__":  # pragma: no cover
    CliApp.run(_FightCli)
