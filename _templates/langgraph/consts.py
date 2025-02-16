from __future__ import annotations

import os

SLACK_NOTIFICATION_URL = (
    "",
    "",
)[os.getenv("ENV") == "production"]
