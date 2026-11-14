# Extract-Transform-Load (ETL) Pipeline

## Purpose
Initialize the production, staging, and sandbox Pleiades databases with a normalized schema of KJV book, chapter, verse, and verse cross-reference data.

## Entry Point

Run any of the following commands from the project root to initialize the respective database:

```bash
python -m src.etl.run_etl sandbox
python -m src.etl.run_etl staging
python -m src.etl.run_etl prod
```

## Possible Enhancements

### DDL Management

- **Current Approach:** Table names in the `CREATE TABLE` and `DROP TABLE IF EXISTS` statements are defined separately.
- **Planned Enhancement:** Define the tables once as SQLAlchemy models and derive both creation and teardown from that metadata, keeping the two in sync automatically.