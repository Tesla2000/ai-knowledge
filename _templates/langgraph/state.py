from __future__ import annotations

from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from pydantic import BaseModel
from pydantic import Field

from context import Context
from nodes import NODE_NAME
from user_profile import Profile


class State(BaseModel):
    """The graph input state."""

    messages: Annotated[list[AnyMessage], add_messages]
    phase: NODE_NAME = "init"
    profile: Profile = Profile()
    context: Context = Field(default_factory=Context)
