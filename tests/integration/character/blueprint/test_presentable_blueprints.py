import pytest

from dnd.character.blueprint.character_data import CharacterData
from dnd.character.blueprint.sentinels import FirstSubclassPostLevel
from dnd.character.blueprint.states.sorcerer.presentable import (
    PresentableSorcererBlueprint,
)
from dnd.character.blueprint.states.wizard.presentable import (
    PresentableWizardLevel20Blueprint,
)
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.spells.spell_slots import FirstLevel, ThirdLevel
from dnd.character.stats import Stats
from dnd.choices.abilities.metamagic import MetamagicOption

_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=18,
    wisdom=10,
    charisma=16,
)

_CHARACTER_DATA = CharacterData(
    name="Gandalf",
    age=80,
    backstory="A wandering wizard.",
)

_LEVEL_20 = FirstSubclassPostLevel.TWENTIETH

_SPELL_SLOTS_20 = FULL_CASTER_SPELL_SLOTS[19]
_SPELL_SLOTS_20_DUMP = _SPELL_SLOTS_20.model_dump()


@pytest.mark.integration
class TestPresentableSorcererBlueprint:
    def _make_bp(self, **extra: object) -> PresentableSorcererBlueprint:
        return PresentableSorcererBlueprint.model_validate(
            {
                "race": Race.HUMAN,
                "subrace": SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
                "stats": _STATS,
                "health_base": 100,
                "level": _LEVEL_20,
                "character_data": _CHARACTER_DATA,
                "spell_slots": _SPELL_SLOTS_20,
                "caster_level": 20,
                **extra,
            }
        )

    def test_spell_slots_in_api_response(self) -> None:
        dumped = self._make_bp().to_presentable_character().model_dump(mode="json")
        assert dumped["spell_slots"] == _SPELL_SLOTS_20_DUMP

    def test_caster_level_in_api_response(self) -> None:
        dumped = self._make_bp().to_presentable_character().model_dump(mode="json")
        assert dumped["caster_level"] == 20

    def test_metamagic_options_in_api_response(self) -> None:
        bp = self._make_bp(
            metamagic_options=(MetamagicOption.CAREFUL, MetamagicOption.TWINNED),
            n_metamagic_choices=0,
        )
        dumped = bp.to_presentable_character().model_dump(mode="json")
        assert dumped["metamagic_options"] == [
            MetamagicOption.CAREFUL,
            MetamagicOption.TWINNED,
        ]
        assert dumped["n_metamagic_choices"] == 0


@pytest.mark.integration
class TestPresentableWizardLevel20Blueprint:
    def _make_bp(self, **extra: object) -> PresentableWizardLevel20Blueprint:
        return PresentableWizardLevel20Blueprint.model_validate(
            {
                "race": Race.ELF,
                "subrace": SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK,
                "stats": _STATS,
                "health_base": 80,
                "level": _LEVEL_20,
                "character_data": _CHARACTER_DATA,
                "spell_slots": _SPELL_SLOTS_20,
                "caster_level": 20,
                "n_signature_spell_choices": 0,
                **extra,
            }
        )

    def test_spell_slots_in_api_response(self) -> None:
        dumped = self._make_bp().to_presentable_character().model_dump(mode="json")
        assert dumped["spell_slots"] == _SPELL_SLOTS_20_DUMP

    def test_caster_level_in_api_response(self) -> None:
        dumped = self._make_bp().to_presentable_character().model_dump(mode="json")
        assert dumped["caster_level"] == 20

    def test_signature_spells_in_api_response(self) -> None:
        sig_spells = (ThirdLevel.FIREBALL, FirstLevel.MAGIC_MISSILE)
        dumped = (
            self._make_bp(signature_spells=sig_spells)
            .to_presentable_character()
            .model_dump(mode="json")
        )
        assert dumped["signature_spells"] == [
            ThirdLevel.FIREBALL,
            FirstLevel.MAGIC_MISSILE,
        ]

    def test_prepared_and_mastery_spells_in_api_response(self) -> None:
        prepared = (FirstLevel.MAGIC_MISSILE, ThirdLevel.FIREBALL)
        mastery = (FirstLevel.MAGIC_MISSILE,)
        dumped = (
            self._make_bp(prepared_spells=prepared, spell_mastery_spells=mastery)
            .to_presentable_character()
            .model_dump(mode="json")
        )
        assert dumped["prepared_spells"] == [
            FirstLevel.MAGIC_MISSILE,
            ThirdLevel.FIREBALL,
        ]
        assert dumped["spell_mastery_spells"] == [FirstLevel.MAGIC_MISSILE]
