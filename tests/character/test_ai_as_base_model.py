from dnd_character_creator.character.blueprint.building_blocks.language_choice_resolver import (
    AILanguageChoiceResolver,
)
from langchain_openai import ChatOpenAI


class TestAIAsBaseModel:
    def test_ai_as_base_model(self):
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key="test-key-not-real",
        )
        AILanguageChoiceResolver(llm=llm)
        AILanguageChoiceResolver(llm=llm.model_dump())
