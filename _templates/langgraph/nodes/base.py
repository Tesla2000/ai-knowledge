from abc import ABC

from config import Config
from state import State
class BaseNode(ABC):
    def __init__(self, config: Config):
        _ = config

    async def execute(self, state: "State") -> "State":
        pass