from __future__ import annotations

import sys

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dnd.choices.class_creation.character_class import (
    Class,
)
from dnd.choices.spell_slots.spell_slots import (
    all_spells,
)
from dnd.choices.spell_slots.spell_slots import Spell

url = "https://dnd5e.wikidot.com/spell:{}"


def scraper_wiki_spell(spell: Spell, output_dir: Path):
    spell_name = spell.value.replace("/", "-").replace(":", "")
    spell_path = output_dir.joinpath(spell_name)
    if spell_path.exists():
        return
    formatted_url = url.format(
        spell_name.replace(" ", "-")
        .lower()
        .replace("-(ua)", "")
        .replace("-(hb)", "")
        .replace("'", "-")
        .replace(":", "")
    )
    response = requests.get(formatted_url)
    if response.status_code != 200:
        sys.stderr.write(f"Wrong status code {formatted_url}\n")
        return

    content = response.content.decode()
    soup = BeautifulSoup(content, "html.parser")
    page_content_div = soup.find("div", id="page-content")
    p_elements = page_content_div.find_all("p")
    last_p_element = p_elements[-1]
    a_elements = last_p_element.find_all("a")
    a_texts = [a.get_text() for a in a_elements if "(" not in a.get_text()]
    tuple(map(Class, a_texts))
    spell_path.write_text(",".join(a_texts))


if __name__ == "__main__":
    for spell_list in all_spells[4:]:
        for spell in spell_list:
            out_path = Path(f"scraped_data/spells/{spell_list.__name__.lower()}")
            out_path.mkdir(exist_ok=True, parents=True)
            scraper_wiki_spell(spell, out_path)
