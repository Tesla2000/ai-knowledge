from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from dnd.character.armor.names import ArmorName
from dnd.character.race.race import Race
from pydantic import Field
from pydantic import PositiveInt
from pydantic_settings import BaseSettings

from .choices.alignment import Alignment
from .choices.background_creatrion.background import Background
from .choices.class_creation.character_class import WizardSubclass
from .choices.equipment_creation.weapons import WeaponName
from .choices.invocations.eldritch_invocation import WarlockPact
from .choices.race_creation.sub_race_sources import DNDResource
from .choices.sex import Sex
from .choices.stats_creation.statistic import Statistic


class ResourcePaths(BaseSettings):
    characters_output_dir: Path = (
        Path("dnd_character_creator") / "characters_output"
    )
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


class Config(BaseSettings):
    backstory_prompt: str = "About 10 sentence long"
    appearance_prompt: str = "The character's general appearance"
    height_prompt: str = "Height in centimeters"
    weight_prompt: str = "Weight in kilograms"
    sex: Optional[Sex] = None
    backstory: Optional[str] = ""
    age: Optional[PositiveInt] = None
    first_most_important_stat: Optional[Statistic] = None
    second_most_important_stat: Optional[Statistic] = None
    third_most_important_stat: Optional[Statistic] = None
    forth_most_important_stat: Optional[Statistic] = None
    fifth_most_important_stat: Optional[Statistic] = None
    sixth_most_important_stat: Optional[Statistic] = None
    main_race: Optional[Race] = Race.HUMAN
    name: Optional[str] = None
    background: Optional[Background] = None
    alignment: Optional[Alignment] = None
    height: Optional[PositiveInt] = None
    weight: Optional[PositiveInt] = None
    eye_color: Optional[str] = None
    skin_color: Optional[str] = None
    hairstyle: Optional[str] = None
    appearance: Optional[str] = None
    subclass_sources: list[DNDResource] = Field(
        default_factory=lambda: list(DNDResource)
    )
    character_llm: str = "gpt-4o"
    character_llm_temp: float = 0.7
    details_llm: str = "gpt-4o-mini"
    details_llm_temp: float = 0
    sub_race: Optional[str] = "Variant Human"
    sub_class: Optional[str] = WizardSubclass.WAR_MAGIC
    character_traits: Optional[str] = None
    ideals: Optional[str] = None
    bonds: Optional[str] = None
    weaknesses: Optional[str] = None
    amount_of_gold_for_equipment: Optional[int] = sys.maxsize
    warlock_pact: Optional[WarlockPact] = None
    armor: Optional[ArmorName] = None
    uses_shield: Optional[bool] = None
    weapons: Optional[list[WeaponName]] = None
    other_equipment: Optional[list[str]] = None


resource_paths = ResourcePaths()
config = Config()
