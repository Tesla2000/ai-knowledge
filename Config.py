from pathlib import Path


class Config:
    root = Path(__file__).parent

for variable in dir(Config):
    value = getattr(Config, variable)
    if isinstance(value, Path) and value.is_dir():
        value.mkdir(parents=True, exist_ok=True)
