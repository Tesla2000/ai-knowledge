from __future__ import annotations

from src.{project_name}.config import parse_arguments, Config, \
    create_config_with_args


def main():
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    print(config)


if __name__ == "__main__":
    exit(main())
