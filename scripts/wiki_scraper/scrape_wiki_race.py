from __future__ import annotations

import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from bs4 import Tag
from dnd.choices.main_race import MainRace
from langchain_openai import ChatOpenAI
from scripts.wiki_scraper.MainRaceTemplate import (
    MainRaceTemplate,
)

url = "https://dnd5e.wikidot.com/lineage:{}"


def scraper_wiki_race(race: MainRace, output_dir: Path, llm):
    race_path = output_dir.joinpath(race.value)
    if race_path.exists():
        return
    response = requests.get(url.format(race.value.lower()))
    if response.status_code != 200:
        raise ValueError("Wrong status code")
    race_path.mkdir()

    content = response.content.decode()
    soup = BeautifulSoup(content, "html.parser")

    page_struct = soup.find("div", id="page-content")
    for section in _split_by_h1(page_struct):
        section_title = re.sub(r"\W", "", section["title"])
        directory = race_path.joinpath(section_title)
        if directory.exists():
            continue
        directory.mkdir(parents=True)
        result = llm.invoke(
            f"Extract data about the sub-races of {race.value} from page "
            f"content:\n\n" + "\n".join(section["content"])
        )
        for sub_race in result.sub_races:
            directory.joinpath(f"{sub_race.name}.json").write_text(
                sub_race.model_dump_json(indent=2)
            )


def _split_by_h1(page_struct: Tag) -> list[dict[str, str | list[str]]]:
    sections = page_struct.find_all("h1")
    split_content = []
    if not sections:
        return [{"title": "PlayersHandbook", "content": [str(page_struct)]}]
    for h1 in sections:
        # Create a dictionary to hold the current h1 and its following content
        section = {"title": h1.get_text(), "content": []}

        # Get the next siblings until the next h1 or the end of the content
        for sibling in h1.find_all_next():
            if sibling.name == "h1":
                break
            section["content"].append(str(sibling))

        split_content.append(section)
    return split_content


if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
        MainRaceTemplate
    )
    for race in MainRace:
        scraper_wiki_race(
            race,
            Path("../../scraped_data/sub_races"),
            llm=llm,
        )
