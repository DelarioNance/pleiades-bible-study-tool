# Pleiades Bible Study Tool

Pleiades is a scripture analysis app for the King James Version (KJV) Bible. Select a book, chapter, verse, and depth, and Pleiades traverses verse cross-references to show how that passage connects to others.

**Live app:** [https://pleiades-bible-study-tool.fastapicloud.dev/](https://pleiades-bible-study-tool.fastapicloud.dev/)

> **Note:** The first request after a period of inactivity may be slow during startup. Please allow a few seconds for the page to load.

## Table of Contents

- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Repository Layout](#repository-layout)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Configure the Environment](#configure-the-environment)
  - [Load the Data](#load-the-data)
  - [Run the App](#run-the-app)
- [Running the Tests](#running-the-tests)
- [CI/CD](#cicd)
- [Known Limitations](#known-limitations)

## Tech Stack

| Layer | Tools |
|-------|-------|
| Database | PostgreSQL, Supabase |
| ETL | Python, SQLAlchemy |
| API | Python, FastAPI |
| UI | HTML, CSS, JavaScript |
| ETL and API tests | Pytest |
| UI tests | Java, Playwright, Maven |
| CI/CD | GitHub Actions, FastAPI Cloud |

## Repository Layout

| Folder | Contents | Details |
|--------|----------|---------|
| `src/` | Application code: ETL, API, UI, and shared database utilities | [src/README.md](src/README.md) |
| `tests/` | Automated tests for each layer | [tests/README.md](tests/README.md) |
| `.github/workflows/` | CI, staging and production deployment, and staging test pipelines | [.github/workflows/README.md](.github/workflows/README.md) |

See the [tests README](tests/README.md) for what each suite covers.

## CI/CD

Pull requests run the full test suite against a temporary database. Merging to `main` deploys to staging and runs the UI tests against it. Production is deployed by a manual run. See the [workflows README](.github/workflows/README.md) for details.

## Known Limitations

Each layer's README lists its own planned improvements. Notable ones include:

- Verse passages are taken from the Free Use Bible API, and Pleiades relies on the correctness of this data
- Support for additional data sources beyond the current KJV source data
- The ETL runs as a single transaction, so staging and production may be blocked while a deployment is running

## Data Sources and Citations

"Bible Cross References" by [OpenBible.info](https://www.openbible.info/), sourced from https://www.openbible.info/labs/cross-references/, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); extracted, transformed, and loaded into a SQL database.

"Free Use Bible API" by [AO Lab](https://www.helloao.org/free-api.html), sourced from https://bible.helloao.org/docs/, licensed under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/); extracted, transformed, and loaded into a SQL database.