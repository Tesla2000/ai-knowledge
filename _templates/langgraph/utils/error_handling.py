from __future__ import annotations

import inspect
import traceback
from functools import wraps
from typing import Any
from typing import Callable
from typing import TYPE_CHECKING

from clients.slack_client import SlackClient
from consts import SLACK_NOTIFICATION_URL

if TYPE_CHECKING:
    from state import State


def send_error_notification(function: Callable[["State", ...], Any]):
    @wraps(function)
    async def wrapper(state: "State", *args, **kwargs):
        try:
            return await function(state, *args, **kwargs)
        except:  # noqa: E722
            if any("unittest" in frame.filename for frame in inspect.stack()):
                raise
            SlackClient(SLACK_NOTIFICATION_URL).send_bullet_list_with_headers(
                "Error detected",
                {
                    **state.model_dump(exclude_defaults=True),
                    "traceback": traceback.format_exc(),
                },
            )
            raise

    return wrapper
