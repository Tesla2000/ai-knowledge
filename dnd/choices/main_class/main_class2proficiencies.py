from __future__ import annotations

import json

from dnd.choices.class_creation.character_class import (
    Class,
)
from dnd.config import Config
from scripts.wiki_scraper.MainClassTemplate import (
    MainClassTemplate,
)


def main_class2proficiencies(
    main_class: Class, config: Config
) -> MainClassTemplate:
    return MainClassTemplate(
        **json.loads(
            config.main_class_root.joinpath(main_class.value)
            .with_suffix(".json")
            .read_text()
        )
    )
