from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


class ResourcePaths(BaseSettings):
    characters_output_dir: Path = Path("dnd_character_creator") / "characters_output"
    pdf_creator: Path = Path("dnd_character_creator") / "pdf_creator"
    tex_prototype: Path = pdf_creator / "prototype.tex"
    scraped_path: Path = Path("scraped_data")
    main_class_root: Path = scraped_path / "main_class"
    background_root: Path = scraped_path / "background"
    sub_races_root: Path = scraped_path / "sub_races"
    spells_root: Path = scraped_path / "spells"
    feats_root: Path = scraped_path / "feats"
    race_abilities_root: Path = scraped_path / "abilities"
    main_class_abilities_root: Path = scraped_path / "main_class_abilities"
    sub_class_abilities_root: Path = scraped_path / "sub_class_abilities"


resource_paths = ResourcePaths()
