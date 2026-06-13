from __future__ import annotations

from dnd_character_creator.character.blueprint.blueprint import Blueprint
from dnd_character_creator.character.builder import Builder


class TestBuilderInit:
    def test_init(self):
        character = Builder()._init_character()
        assert isinstance(character, Blueprint)
