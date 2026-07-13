from dnd.character.blueprint.states.state import Blueprint


class TestBuilderInit:
    def test_init(self):
        blueprint = Blueprint()
        assert isinstance(blueprint, Blueprint)
