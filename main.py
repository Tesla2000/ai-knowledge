from __future__ import annotations

import json
from operator import attrgetter
from typing import Type

from dnd.character_base import (
    get_base_character_template,
)
from dnd.character_details_filler import (
    CharacterDetailsFiller,
)
from dnd.config import Config
from dnd.config import create_config_with_args
from dnd.config import parse_arguments
from dnd.pdf_creator.create_pdf import create_pdf
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import create_model


class Main:
    def __init__(self):
        args = parse_arguments(Config)
        self.config = create_config_with_args(Config, args)
        self.character_llm = ChatOpenAI(
            model=self.config.character_llm,
            temperature=self.config.character_llm_temp,
        )
        self.details_llm = ChatOpenAI(
            model=self.config.details_llm,
            temperature=self.config.details_llm_temp,
        )

    def __call__(self):
        self._get_character_bases()
        self._fill_character_details()
        self._generate_pdfs()

    def _get_character_bases(self):
        character_base_template, self.base_pre_defined_fields = (
            get_base_character_template(self.config)
        )
        if self.config.n_instances == 1:
            self._generate_character(character_base_template)
        else:
            self._generate_characters(character_base_template)

    def _generate_character(self, character_base_template: Type[BaseModel]):
        description_base = (
            "Create a D&D e5 " + self.config.base_description.strip()
        )
        description_base = self._modify_base(description_base)
        base_template = self.character_llm.with_structured_output(
            character_base_template
        )
        self.character_base_templates = [
            base_template.invoke(description_base)
        ]

    def _generate_characters(self, character_base_template: Type[BaseModel]):
        description_base = (
            "Create a D&D e5 characters according to description "
            + self.config.base_description.strip()
        )
        description_base = self._modify_base(description_base)
        fields = tuple(
            f"npc_{index + 1}" for index in range(self.config.n_instances)
        )
        characters_base_template = create_model(
            "GroupOfNPCs",
            **{field: (character_base_template, ...) for field in fields},
        )
        base_template = self.character_llm.with_structured_output(
            characters_base_template
        )
        self.character_base_templates = attrgetter(*fields)(
            base_template.invoke(description_base)
        )

    def _modify_base(self, description_base: str) -> str:
        if self.base_pre_defined_fields:
            description_base += (
                f"\nThe following details about the character are "
                f"given:\n{json.dumps(self.base_pre_defined_fields, indent=2)}"
            )
        description_base += (
            "\nBe careful picking size of character some races "
            "are smaller than others."
        )
        return description_base

    def _fill_character_details(self):
        self.character_wrappers = (
            CharacterDetailsFiller(
                character_base_template,
                self.base_pre_defined_fields,
                self.config,
                self.details_llm,
            ).fill_details()
            for character_base_template in self.character_base_templates
        )

    def _generate_pdfs(self):
        tuple(
            create_pdf(character_wrapper, self.config)
            for character_wrapper in self.character_wrappers
        )


if __name__ == "__main__":
    exit(Main()())
