from __future__ import annotations

import json

from dnd.choices.background_creatrion.background import Background
from dnd.config import ResourcePaths
from scripts.wiki_scraper.BackgroundTemplate import BackgroundTemplate


def background2stats(
    background: Background, config: ResourcePaths
) -> BackgroundTemplate:
    return BackgroundTemplate(
        **json.loads(
            config.background_root.joinpath(background.value)
            .with_suffix(".json")
            .read_text()
        )
    )
