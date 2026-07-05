# Validation & Linting

Pre-commit and tests are both code quality gates. The same principle applies to both:
run once, save output, read the file -- never re-run with different flags just to see
additional lines.

## pre-commit

```bash
pre-commit run --all-files 2>&1 | tee pre-commit-output.txt
```

Read `pre-commit-output.txt` to analyse failures.

## pytest

```bash
pytest --tb=short 2>&1 | tee test-output.txt
```

Read `test-output.txt` to analyse failures and coverage gaps.

## Related

- [testing.md](../python/testing.md) -- pytest rules and coverage
- [git.md](git.md) -- git discipline and dependency management
