from __future__ import annotations

from src.config import Config
from src.config import create_config_with_args
from src.config import parse_arguments


def main():
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    print(config)


if __name__ == "__main__":
    exit(main())
