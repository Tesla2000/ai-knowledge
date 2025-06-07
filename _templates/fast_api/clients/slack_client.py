from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from typing import TYPE_CHECKING

import requests


if TYPE_CHECKING:
    pass


class SlackClient:
    def __init__(self, slack_url: str):
        self.slack_url = slack_url

    def send_data(self, data: dict) -> requests.Response:
        return requests.post(self.slack_url, json=data)

    def send_bullet_list_with_headers(self, header: str, bullet_list: Mapping):
        builder = _SlackBlockBuilder()
        builder.add_text(header)
        builder.add_nested_list(bullet_list)
        self.send_data({"blocks": builder.blocks})


class _SlackBlockBuilder:
    def __init__(self):
        self.blocks = []
        self.current_block = None

    def start_rich_text(self):
        self.current_block = {"type": "rich_text", "elements": []}
        self.blocks.append(self.current_block)
        return self

    def add_text(
        self, text, bold=False, italic=False, strike=False, code=False
    ):
        if not self.current_block:
            self.start_rich_text()

        element = {"type": "text", "text": text}
        element["style"] = {
            "bold": bold,
            "italic": italic,
            "strike": strike,
            "code": code,
        }

        self.current_block["elements"].append(
            {"type": "rich_text_section", "elements": [element]}
        )
        return self

    # Usage example
    @staticmethod
    def format_item(key: str, value: Any) -> str:
        return f"{key.replace('_', ' ').capitalize()}: {value}"

    def add_nested_list(self, items, style="bullet", indent=0, border=None):
        if not self.current_block:
            self.start_rich_text()

        items = [self.format_item(k, v) for k, v in items.items()]

        nested_list = {
            "type": "rich_text_list",
            "style": style,
            "indent": indent,
            "elements": [],
        }
        if border is not None:
            nested_list["border"] = border

        for item in items:
            nested_list["elements"].append(
                {
                    "type": "rich_text_section",
                    "elements": [{"type": "text", "text": str(item)}],
                }
            )

        self.current_block["elements"].append(nested_list)
        return self
