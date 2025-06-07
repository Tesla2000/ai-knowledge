from __future__ import annotations

from enum import StrEnum
from typing import List
from typing import Optional
from typing import Union

from langchain.schema import AIMessage
from pydantic import BaseModel


class FormattingType(StrEnum):
    OPTIONS = "options"
    MEDIA = "media"
    URL = "url"


class MediaObject(BaseModel):
    mediaUri: str
    mimeType: str
    mediaName: str


class Suggestion(BaseModel):
    label: str
    url: Optional[str]
    media: MediaObject


class OptionsFormatting(BaseModel):
    type: FormattingType
    options: List[str]
    body: str


class MediaFormatting(BaseModel):
    type: FormattingType
    media: List[MediaObject]


class SuggestionsFormatting(BaseModel):
    type: FormattingType
    suggestions: List[Suggestion]


class AIMessageWithFormatting(AIMessage):
    details: dict = {
        "formatting": Union[
            OptionsFormatting, MediaFormatting, SuggestionsFormatting
        ]
    }
