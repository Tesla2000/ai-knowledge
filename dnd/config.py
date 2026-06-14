from __future__ import annotations

import sys
from pathlib import Path

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


class Config(BaseSettings):
    backstory_prompt: str = "About 10 sentence long"
    appearance_prompt: str = "The character's general appearance"
    height_prompt: str = "Height in centimeters"
    weight_prompt: str = "Weight in kilograms"
    sex: Sex | None = None
    backstory: str | None = ""
    age: PositiveInt | None = None
    first_most_important_stat: Statistic | None = None
    second_most_important_stat: Statistic | None = None
    third_most_important_stat: Statistic | None = None
    forth_most_important_stat: Statistic | None = None
    fifth_most_important_stat: Statistic | None = None
    sixth_most_important_stat: Statistic | None = None
    main_race: Race | None = Race.HUMAN
    name: str | None = None
    background: Background | None = None
    alignment: Alignment | None = None
    height: PositiveInt | None = None
    weight: PositiveInt | None = None
    eye_color: str | None = None
    skin_color: str | None = None
    hairstyle: str | None = None
    appearance: str | None = None
    subclass_sources: list[DNDResource] = Field(
        default_factory=lambda: list(DNDResource)
    )
    character_llm: str = "gpt-4o"
    character_llm_temp: float = 0.7
    details_llm: str = "gpt-4o-mini"
    details_llm_temp: float = 0
    sub_race: str | None = "Variant Human"
    sub_class: str | None = WizardSubclass.WAR_MAGIC
    character_traits: str | None = None
    ideals: str | None = None
    bonds: str | None = None
    weaknesses: str | None = None
    amount_of_gold_for_equipment: int | None = sys.maxsize
    warlock_pact: WarlockPact | None = None
    armor: ArmorName | None = None
    uses_shield: bool | None = None
    weapons: list[WeaponName] | None = None
    other_equipment: list[str] | None = None


resource_paths = ResourcePaths()
config = Config()
