# CLI Apps

## Rules

- CLI apps use `pydantic-settings` `BaseSettings` exclusively.
- Entry point is `cli_cmd` (sync or async). No other methods allowed on the settings class.
- `cli_cmd` contains minimal code. All logic lives in dedicated pydantic services called from it.
- Use `cli_kebab_case=True` for argument names.

## Template

```python
from typing import ClassVar
from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

class Main(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        cli_parse_args=True,
        cli_kebab_case=True,
    )

    input_path: Path
    output_path: Path
    processor: ProcessorService = ProcessorService()

    def cli_cmd(self) -> None:
        result = self.processor.run(self.input_path)
        result.save(self.output_path)


if __name__ == "__main__":
    Main().cli_cmd()
```

## What goes in cli_cmd

Only: read fields, call service entry-point method, return or print result.
No branching logic, no data transformation, no error handling beyond what propagates naturally.

## Related

- [services.md](services.md) -- pydantic service pattern
- [pydantic.md](../python/pydantic.md) -- BaseModel rules
