from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from dnd.character.race.race import Race

if TYPE_CHECKING:
    from dnd.config import Config


def get_sub_races(main_race: Race, config: Config) -> type[Enum]:
    return Enum(  # type: ignore[return-value]
        f"{main_race.value}SubRace",
        {
            (name := path.with_suffix("").name).upper().replace(" ", "_"): name
            for path in _get_sub_races(main_race, config)
        },
    )


def _get_sub_races(main_race: Race, config: Config) -> object:
    for path in filter(  # type: ignore[var-annotated]
        lambda path: path.name in config.subclass_sources,  # type: ignore[arg-type]
        config.sub_races_root.joinpath(main_race.value).iterdir(),  # type: ignore[attr-defined]
    ):
        yield from path.iterdir()
