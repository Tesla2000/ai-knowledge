# Knowledge Base Index

| File | Summary |
|------|---------|
| [CLI Apps](topics/architecture/cli.md) | - CLI apps use `pydantic-settings` `BaseSettings` exclusively. |
| [Service Creation Pattern](topics/architecture/services.md) | - Services are exclusively pydantic `BaseModel` subclasses, frozen. |
| [Exception Handling](topics/python/exception_handling.md) | The exception is a normal, anticipated outcome (file not found, no releases, regex no match). |
| [Imports](topics/python/imports.md) | - Never use local (inline) imports unless explicitly allowed by the supervisor. |
| [Pydantic](topics/python/pydantic.md) | - All pydantic models must be frozen (`ConfigDict(frozen=True)`). |
| [Style](topics/python/style.md) | - Never use bare functions. Only methods are allowed. |
| [Testing](topics/python/testing.md) | - Use pytest exclusively. |
| [Typing](topics/python/typing.md) | - Always type hint both arguments and return type. |
| [Git & Dependency Workflow](topics/workflow/git.md) | - Never commit unless explicitly asked. |
