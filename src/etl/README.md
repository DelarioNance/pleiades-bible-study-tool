# Extract-Transform-Load (ETL) Layer

## Purpose
Initialize the production, staging, and sandbox Pleiades databases with a normalized schema of KJV book, chapter, verse, and verse cross-reference data.

## Entry Point

Run any of the following pairs of commands from the project root to initialize the respective database:

```bash
source venv/bin/activate
python -m src.etl.run_etl sandbox

source venv/bin/activate
python -m src.etl.run_etl staging

source venv/bin/activate
python -m src.etl.run_etl prod
```

## Notable Areas for Improvment

### Backup of Migrated Data

- **Current Approach:** Re-running the ETL drops the existing tables and rebuilds them, so previously migrated data is not preserved if the source schema changes.
- **Planned Enhancement:** Back up the existing data before a schema change so it can be restored or carried into the new schema if something goes wrong.

### Data Source Flexibility

- **Current Approach:** The ETL is written around the current KJV and cross-reference data sources.
- **Planned Enhancement:** Handle future data and API sources dynamically, so adding a new source or translation does not require much reworking of the extract and transform steps.

### DDL Management

- **Current Approach:** Table names in the `CREATE TABLE` and `DROP TABLE IF EXISTS` statements are defined separately.
- **Planned Enhancement:** Define the tables once as SQLAlchemy models and derive both creation and teardown from that metadata, keeping the two in sync automatically.