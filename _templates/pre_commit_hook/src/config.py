from __future__ import annotations

import toml
from config_parser import ConfigBase
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(ConfigBase):
    pass
