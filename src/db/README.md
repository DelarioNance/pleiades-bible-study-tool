# Database (DB) Layer

## Purpose
Centralizes connection handling for the Pleiades databases. It creates a SQLAlchemy engine for each environment (sandbox, staging, prod) and reads connection secrets from environment variables, so no credentials live in the code.

## Key Functions

```python
# Engine for a specific environment
get_db_engine("sandbox")
get_db_engine("staging")
get_db_engine("prod")

# Engine for the environment set in the PLEIADES_ENV environment variable
get_current_engine()
```