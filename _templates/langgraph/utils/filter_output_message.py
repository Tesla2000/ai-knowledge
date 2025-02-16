from __future__ import annotations

from collections.abc import Iterable

from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage


def filter_output_messages(
    messages: Iterable[BaseMessage],
) -> list[BaseMessage]:
    return list(
        message
        for message in messages
        if not isinstance(message, ToolMessage) and message.content
    )
