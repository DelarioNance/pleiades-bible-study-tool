# Tests

Overview of the Pleiades automated test suites.

| Suite | Type | Run with | Details |
|-------|------|----------|---------|
| etl   | unit, integration, e2e | `pytest tests/etl` | [etl/README.md](etl/README.md) |
| api   | contract, integration, client/server error | `pytest tests/api` | [api/README.md](api/README.md) |
| db    | unit | `pytest tests/db` | [db/README.md](db/README.md) |
| ui    | browser (Playwright) | `cd tests/ui && mvn clean package` | [ui/README.md](ui/README.md) |

## Notable Prerequisite(s)
- The app running locally for UI tests

## Run order in CI
ETL, then API, then UI.

(DB is ommitted due to low priority)