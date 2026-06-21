from __future__ import annotations

import os
import shutil

from dnd.character_wrapper import CharacterWrapper  # type: ignore[import-not-found]
from dnd.config import Config
from dnd.pdf_creator.remove_blank_page import (
    remove_blank_page,
)
from dnd.pdf_creator.run_lunatex import run_lualatex
from dnd.pdf_creator.update_prototype import (  # type: ignore[import-not-found]
    update_prototype,
)


def create_pdf(
    character_wrapper: CharacterWrapper,
    config: Config,
) -> None:
    character_full = character_wrapper.character
    tex_prototype = config.tex_prototype  # type: ignore[attr-defined]
    pdf_creator = config.pdf_creator  # type: ignore[attr-defined]
    characters_output_dir = config.characters_output_dir  # type: ignore[attr-defined]
    prototype = update_prototype(
        character_wrapper, character_full, tex_prototype.read_text()
    )
    character_path = pdf_creator.joinpath(f"{character_full.name}.tex")
    character_path.write_text(prototype)
    try:
        run_lualatex(character_path.name, pdf_creator)
    except Exception as e:
        raise e
    else:
        pdf_path = character_path.with_suffix(".pdf")
        shutil.move(pdf_path, characters_output_dir / pdf_path.name)
        shutil.move(character_path, characters_output_dir / character_path.name)
        remove_blank_page(characters_output_dir / pdf_path.name)
    finally:
        os.remove(character_path.with_suffix(".aux"))
        os.remove(character_path.with_suffix(".log"))
