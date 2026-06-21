from __future__ import annotations

import json

from dnd.choices.background_creatrion.background import (
    Background,
)
from dnd.config import Config
from scripts.wiki_scraper import (
    BackgroundTemplate,
)


def background2stats(background: Background, config: Config) -> BackgroundTemplate:  # type: ignore[valid-type]
    return BackgroundTemplate(  # type: ignore[operator,no-any-return]
        **json.loads(
            config.background_root.joinpath(background.value)  # type: ignore[attr-defined]
            .with_suffix(".json")
            .read_text()
        )
    )
