from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dnd.BackgroundTemplate import BackgroundTemplate
from dnd.choices.background_creatrion.background import (
    Background,
)
from langchain_openai import ChatOpenAI

url = "https://dnd5e.wikidot.com/background:{}"


def scraper_wiki_background(background: Background, output_dir: Path, llm):
    feat_path = output_dir.joinpath(f"{background.value}.json")
    if feat_path.exists():
        return
    response = requests.get(url.format(background.value.lower()))
    if response.status_code != 200:
        print(f"Wrong status code {url.format(background.value.lower())}")
        return

    content = response.content.decode()
    soup = BeautifulSoup(content, "html.parser")
    toc_element = soup.find(id="toc0")

    previous_p = toc_element.find_previous("p")
    page_struct = str(previous_p)
    feat_result = llm.invoke(
        "Extract data about background from page content. "
        "Map extracted information to provided options:\n\n" + page_struct
    )
    feat_path.write_text(feat_result.model_dump_json(indent=2))


if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
        BackgroundTemplate
    )
    for background in Background:
        scraper_wiki_background(
            background,
            Path("../../scraped_data/background"),
            llm=llm,
        )
