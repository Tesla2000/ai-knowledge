from __future__ import annotations

from enum import Enum
from typing import Type
from typing import TYPE_CHECKING

from dnd.character.race.race import Race

if TYPE_CHECKING:
    from dnd.config import Config


def get_sub_races(main_race: Race, config: "Config") -> Type[Enum]:
    return Enum(
        f"{main_race.value}SubRace",
        dict(
            (
                (name := path.with_suffix("").name).upper().replace(" ", "_"),
                name,
            )
            for path in _get_sub_races(main_race, config)
        ),
    )


def _get_sub_races(main_race: Race, config: "Config"):
    for path in filter(
        lambda path: path.name in config.subclass_sources,
        config.sub_races_root.joinpath(main_race.value).iterdir(),
    ):
        yield from path.iterdir()
