---
name: cli
description: CLI app pattern using pydantic-settings BaseSettings with cli_cmd entry point
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

if __name__ == "__main__":
    Main().cli_cmd()
```

cli_cmd only: read fields, call service entry-point, return or print result.
No branching logic, no data transformation inside cli_cmd.
