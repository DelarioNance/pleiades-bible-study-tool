# Source Code

Overview of the Pleiades application code. Each layer has its own README with details.

| Layer | Purpose | Details |
|-------|---------|---------|
| etl | Builds the production, staging, and sandbox databases from KJV book, chapter, verse, and cross-reference data | [etl/README.md](etl/README.md) |
| api | Serves the UI and exposes endpoints for books, chapters, verses, and cross-reference traversal | [api/README.md](api/README.md) |
| ui | Single Page Application that lets users select a book, chapter, and verse, and view 1st- and 2nd-degree scripture connections | [ui/README.md](ui/README.md) |
| db | Shared database utilities, such as building connection URLs from environment variables | [db/README.md](db/README.md) |

## How the Layers Fit Together

1. **ETL** loads data into Postgres. It runs before the app is deployed or used.
2. **API** reads from that database and serves the data as JSON, along with the single HTML page.
3. **UI** runs in the browser talks only to the API.

The ETL and API both rely on the shared database utilities to connect to the right database.

## Running

Run commands from the project root.

| Task | Command |
|------|---------|
| Initialize a database | `python -m src.etl.run_etl sandbox` (or `staging`, `prod`) |
| Run the app locally | `fastapi dev src/api/main.py` |

The UI has no separate run command because the API serves it.

## Related

- Tests for each layer live in the top-level tests folder.
- Automated testing and deployment are described in the GitHub workflows [README](../.github/workflows/README.md).