import pytest
from dnd.character.blueprint.building_blocks.language_choice_resolver import (
    AILanguageChoiceResolver,
)
from langchain_openai import ChatOpenAI


@pytest.mark.e2e
class TestAIAsBaseModel:
    def test_ai_as_base_model(self) -> None:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key="test-key-not-real",  # pragma: allowlist secret
        )
        AILanguageChoiceResolver(llm=llm)
        AILanguageChoiceResolver(llm=llm.model_dump())
