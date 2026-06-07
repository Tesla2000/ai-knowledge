import pytest
from dnd.character.checkpoint import MemoryStorage
from dnd.server.app import create_app
from starlette.testclient import TestClient as StarletteTestClient


class TestClient:

    @pytest.fixture
    def storage(self):
        return MemoryStorage()

    @pytest.fixture
    def client(self, storage):
        app = create_app(storage)
        return StarletteTestClient(app)
