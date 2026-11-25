# Automated Tests

Overview of the Pleiades automated test suites.

| Suite | Type | Run with | Details |
|-------|------|----------|---------|
| etl   | unit, integration, e2e | `pytest tests/etl` | [etl/README.md](etl/README.md) |
| api   | contract, integration, client/server error | `pytest tests/api` | [api/README.md](api/README.md) |
| ui    | browser (Playwright) | `cd tests/ui && mvn clean package` | [ui/README.md](ui/README.md) |

## Notable Prerequisite(s)
- The app running locally for UI tests

## Run order in CI
ETL, then API, then UI.

## Test Reports

Allure reports are automatically generated and published for Continuous Integration and Staging Test workflow runs.

Report URLs follow these patterns:

- Continuous Integration:
  https://delarionance.github.io/pleiades-bible-study-tool/test-reports/continuous-integration/run-{GITHUB_ACTIONS_WORKFLOW_RUN_NUMBER}

- Staging Tests:
  https://delarionance.github.io/pleiades-bible-study-tool/test-reports/staging-tests/run-{GITHUB_ACTIONS_WORKFLOW_RUN_NUMBER}

Replace `{GITHUB_ACTIONS_WORKFLOW_RUN_NUMBER}` with the workflow run number from the GitHub Actions run you want to see results for.