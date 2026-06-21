from __future__ import annotations

import json

from dnd.character.race.race import Race
from dnd.config import Config
from scripts.wiki_scraper.MainRaceTemplate import (
    SubRaceTemplate,
)


def sub_race2stats(race: Race, sub_race: str, config: Config) -> SubRaceTemplate:
    return SubRaceTemplate(
        **json.loads(
            next(
                config.sub_races_root.joinpath(race.value).rglob(f"{sub_race}.json")  # type: ignore[attr-defined]
            ).read_text()
        )
    )
