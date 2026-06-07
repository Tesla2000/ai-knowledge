from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dnd.choices.class_creation.character_class import (
    Class,
)
from langchain_openai import ChatOpenAI
from scripts.wiki_scraper.MainClassTemplate import (
    MainClassTemplate,
)

url = "https://dnd5e.wikidot.com/{}"


def scraper_wiki_class(main_class: Class, output_dir: Path, llm):
    main_class_path = output_dir.joinpath(f"{main_class.value}.json")
    if main_class_path.exists():
        return
    response = requests.get(url.format(main_class.value.lower()))
    if response.status_code != 200:
        raise ValueError("Wrong status code")
    content = response.content.decode()
    soup = BeautifulSoup(content, "html.parser")
    toc_element = soup.find(id="toc2")
    next_p = toc_element.find_next("p")
    page_struct = str(next_p)
    main_class_result = llm.invoke(
        "Extract data about abilities of a class from page content:\n\n"
        + page_struct
    )
    main_class_path.write_text(main_class_result.model_dump_json(indent=2))


if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
        MainClassTemplate
    )
    for main_class in Class:
        scraper_wiki_class(
            main_class, Path("../../scraped_data/main_class"), llm=llm
        )
