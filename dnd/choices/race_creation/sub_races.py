from __future__ import annotations

from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import cast
from typing import Protocol
from typing import runtime_checkable

from dnd.character.race.race import Race
from dnd.choices.race_creation.sub_race_sources import DNDResource


@runtime_checkable
class _SubRaceConfig(Protocol):
    sub_races_root: Path
    subclass_sources: list[DNDResource]


def get_sub_races(main_race: Race, config: _SubRaceConfig) -> type[Enum]:
    return cast(
        type[Enum],
        Enum(
            f"{main_race.value}SubRace",
            {
                (name := path.with_suffix("").name).upper().replace(" ", "_"): name
                for path in _get_sub_races(main_race, config)
            },
        ),
    )


def _get_sub_races(main_race: Race, config: _SubRaceConfig) -> Iterator[Path]:
    for path in config.sub_races_root.joinpath(main_race.value).iterdir():
        if str(path.name) in [str(s) for s in config.subclass_sources]:
            yield from path.iterdir()
