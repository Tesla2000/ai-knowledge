import pytest
import dnd.server.handler as handler_module


@pytest.mark.unit
class TestHandler:
    def test_handler_is_callable(self) -> None:
        assert callable(handler_module.handler)
