from __future__ import annotations

from typing import List, Union

from langchain.schema import AIMessage

from models.formatting import FormattingType, OptionsFormatting, \
    MediaFormatting, SuggestionsFormatting
from models.formatting import MediaObject
from models.formatting import Suggestion



class _AIMessageWithFormatting(AIMessage):
    details: dict = {
        "formatting": Union[
            OptionsFormatting, MediaFormatting, SuggestionsFormatting
        ]
    }

class FormattingManager:
    @staticmethod
    def format_options_response(
        response: AIMessage, options: list[str]
    ) -> _AIMessageWithFormatting:
        return _AIMessageWithFormatting(
            **{
                **response.model_dump(),
                "details": {
                    "formatting": {
                        "type": FormattingType.OPTIONS,
                        "options": options,
                        "body": response.content,
                    }
                },
            }
        )

    @staticmethod
    def format_media_response(
        response: AIMessage, media_list: List[MediaObject]
    ) -> _AIMessageWithFormatting:
        return _AIMessageWithFormatting(
            **{
                **response.model_dump(),
                "details": {
                    "formatting": {
                        "type": FormattingType.MEDIA,
                        "media": media_list,
                        "body": response.content,
                    }
                },
            }
        )

    @staticmethod
    def format_suggestions_response(
        response: AIMessage, suggestions: List[Suggestion]
    ) -> _AIMessageWithFormatting:
        return _AIMessageWithFormatting(
            **{
                **response.model_dump(),
                "details": {
                    "formatting": {
                        "type": FormattingType.URL,
                        "suggestions": suggestions,
                        "body": response.content,
                    }
                },
            }
        )
