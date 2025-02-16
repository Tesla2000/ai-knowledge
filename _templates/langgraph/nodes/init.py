from langchain.schema import AIMessage
from state import State
from .base import BaseNode

class Init(BaseNode):
    async def execute(self, state: "State") -> "State":
        return State(
            messages=[AIMessage("Hello world")],
            phase=state.phase,
        )
