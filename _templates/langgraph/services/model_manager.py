from __future__ import annotations

import logging
import operator
from functools import reduce

from langchain.schema import AIMessage
from langchain.schema import BaseMessage
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from consts import MAX_CONV_LENGTH
from utils.filter_tool_message import filter_tool_messages

logger = logging.getLogger(__name__)


class ModelManager:
    def __init__(self, model_name: str, extractor_model_name: str):
        self.model = ChatOpenAI(model_name=model_name, temperature=0)
        self.extractor_model = ChatOpenAI(model_name=extractor_model_name, temperature=0)

    def invoke_model_with_structured_output(
        self,
        prompt: str,
        messages: list[BaseMessage],
        possible_outputs: type,
    ) -> AIMessage:
        class StructuredResponse(BaseModel):
            content: possible_outputs

        structured_model = self.extractor_model.with_structured_output(
            StructuredResponse
        )
        response = structured_model.invoke(
            [SystemMessage(content=prompt)] + filter_tool_messages(messages),
            stream=False,
        )

        return response

    async def generate_response(
        self,
        prompt: str,
        messages: list[BaseMessage],
        max_conv_length: int = MAX_CONV_LENGTH,
    ) -> AIMessage:
        response = []
        async for elem in self.model.astream(
            [SystemMessage(content=prompt)]
            + filter_tool_messages(messages)[-max_conv_length:]
        ):
            response.append(elem)
        response = reduce(operator.add, response)
        return AIMessage(
            content=response.content,
            additional_kwargs=response.additional_kwargs,
            response_metadata=response.response_metadata,
            id=response.id,
        )
