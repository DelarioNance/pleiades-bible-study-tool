# Database Utility Test Suite

## Purpose
Automated tests for the Pleiades database utilities. They check that the database connection URL is built correctly from environment variables for each supported database alias, and that unsupported aliases are rejected.

## Running the Tests

Run from the project root:

```bash
source venv/bin/activate
pytest tests/db
```

### Environment Isolation
The tests use pytest's `monkeypatch` to set environment variables temporarily. Anything a test sets is automatically removed when the test finishes, so no state leaks between tests and the real environment is never modified.