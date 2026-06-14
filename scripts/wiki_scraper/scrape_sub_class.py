from __future__ import annotations

from enum import Enum
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dnd.choices.class_creation.character_class import (
    Class,
)
from dnd.choices.class_creation.character_class import (
    SUBCLASSES,
)
from langchain_openai import ChatOpenAI
from scripts.wiki_scraper.ability_template import (
    AbilitiesTemplate,
)

url = "https://dnd5e.wikidot.com/{}:{}"


def scraper_wiki_subclass_class(
    main_class: Class, sub_class: Enum, output_dir: Path, llm
):
    main_class_path = output_dir.joinpath(main_class.value)
    if not main_class_path.exists():
        main_class_path.mkdir()
    sub_class_path = main_class_path.joinpath(sub_class.value)
    if sub_class_path.exists():
        return
    request_url = url.format(
        main_class.value.lower(),
        sub_class.value.lower()
        .replace("path of the ", "")
        .replace("path of ", "")
        .replace("college of ", "")
        .replace(" domain", "")
        .replace("circle of the ", "")
        .replace("circle of ", "")
        .replace("way of the ", "")
        .replace("oath of the ", "")
        .replace("oath of ", "")
        .replace(" conclave", "")
        .replace("school of ", "")
        .replace("way of ", "")
        .replace(" ", "-"),
    )
    response = requests.get(request_url)
    if response.status_code != 200:
        raise ValueError(f"Wrong status code {request_url}")
    sub_class_path.mkdir()
    content = response.content.decode()
    soup = BeautifulSoup(content, "html.parser")

    page_struct = str(soup.find("div", id="page-content"))
    abilities_result = llm.invoke(
        "Extract data about abilities of a sub_class from page content:\n\n"
        + page_struct
    )
    for ability in abilities_result.abilities:
        ability_path = sub_class_path.joinpath(f"{ability.name}.json")
        if ability_path.exists():
            continue
        ability_path.write_text(ability.model_dump_json(indent=2))


if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(AbilitiesTemplate)
    for main_class in Class:
        for sub_class in SUBCLASSES[main_class]:
            scraper_wiki_subclass_class(
                main_class,
                sub_class,
                Path("../../scraped_data/sub_class_abilities"),
                llm=llm,
            )
