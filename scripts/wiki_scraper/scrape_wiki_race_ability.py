from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dnd.character.race.race import Race
from langchain_openai import ChatOpenAI
from scripts.wiki_scraper.ability_template import (
    AbilitiesTemplate,
)

url = "https://dnd5e.wikidot.com/lineage:{}"


def scraper_wiki_race(race: Race, output_dir: Path, llm):
    race_path = output_dir.joinpath(race.value)
    if race_path.exists():
        return
    response = requests.get(url.format(race.value.lower()))
    if response.status_code != 200:
        raise ValueError("Wrong status code")
    race_path.mkdir()

    content = response.content.decode()
    soup = BeautifulSoup(content, "html.parser")

    page_struct = str(soup.find("div", id="page-content"))
    abilities = llm.invoke(
        "Extract data about abilities from page content:\n\n" + page_struct
    )
    for ability in abilities.abilities:
        json_path = race_path.joinpath(f"{ability.name}.json")
        if json_path.exists():
            continue
        json_path.write_text(ability.model_dump_json(indent=2))


if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(AbilitiesTemplate)
    for race in Race:
        scraper_wiki_race(
            race,
            Path("../../scraped_data/abilities"),
            llm=llm,
        )
