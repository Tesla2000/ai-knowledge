from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dnd.character.feature.feats import FeatName
from dnd.character.feature.feature import Feature
from langchain_openai import ChatOpenAI

url = "https://dnd5e.wikidot.com/feat:{}"


def scraper_wiki_feats(feat: FeatName, output_dir: Path, llm):
    feat_path = output_dir.joinpath(f"{feat.value}.json")
    if feat_path.exists():
        return
    response = requests.get(url.format(feat.value.lower()))
    if response.status_code != 200:
        raise ValueError("Wrong status code")

    content = response.content.decode()
    soup = BeautifulSoup(content, "html.parser")

    page_struct = str(soup.find("div", id="page-content"))
    feat_result = llm.invoke(
        "Extract data about feat from page content:\n\n" + page_struct
    )
    feat_path.write_text(feat_result.model_dump_json(indent=2))


if __name__ == "__main__":
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(Feature)
    for feat in FeatName:
        scraper_wiki_feats(
            feat,
            Path("../../scraped_data/feats"),
            llm=llm,
        )
