---
name: cli
description: cli, CLI app, pydantic-settings, BaseSettings, cli_cmd, CliApp, __main__.py, entry point, cli_kebab_case
---

# CLI Apps

- Use pydantic-settings BaseSettings exclusively.
- Entry point is cli_cmd (sync or async). No other methods on the settings class.
- cli_cmd has minimal code. All logic lives in dedicated pydantic services.
- Use cli_kebab_case=True.

```python
class Main(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        cli_parse_args=True,
        cli_kebab_case=True,
    )

    input_path: Path
    processor: ProcessorService = ProcessorService()

    def cli_cmd(self) -> None:
        result = self.processor.run(self.input_path)
        result.save(self.output_path)
```

The entry point is `__main__.py` in the package. It runs the settings class through `CliApp`, which parses the arguments and calls `cli_cmd`. Do not put an `if __name__` block in the settings module.

```python
# pkg/__main__.py
from pydantic_settings import CliApp

from pkg._main import Main

if __name__ == "__main__":
    CliApp.run(Main)
```

cli_cmd only: read fields, call service entry-point, return or print result.
No branching logic, no data transformation inside cli_cmd.
