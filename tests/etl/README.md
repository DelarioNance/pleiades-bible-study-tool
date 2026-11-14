# ETL Test Suite

## Purpose
Automated tests for the Pleiades ETL layer. They check that each stage of the pipeline behaves correctly in isolation, that the database tables are created and dropped as expected, and that the data loaded into the database is complete.

## Running the Tests

Run from the project root:

```bash
source venv/bin/activate
pytest tests/etl
```

## Organization

The tests are divided into three levels, moving from the smallest piece of the pipeline to the whole thing.

### Unit Tests
Test individual pieces of the pipeline in isolation, using mock data instead of a real database or real data sources. They are grouped by pipeline stage:

- **Extract:** Reading data from the source files and sources. Mock classes stand in for the asynchronous functionality, which allows the async verse retrieval to be validated without making real requests.
- **Tranform / Derive:** Converting and shaping the extracted data into the structure the database expects.
- **Load:** Inserting the prepared data into the database.

### Integration Tests
Test the ETL's interaction with the database. These cover creating the tables and dropping them, confirming that the schema setup and teardown work.

### End-to-End (E2E) Tests
Run against a database populated by the full ETL and check the real loaded data. They are grouped by the kind of check:

- **Canon tests:** Confirm the books, chapters, and verses loaded match the expected canonical structure of the KJV.
- **Integrity tests:** Confirm the loaded data is internally consistent, including for books, chapters, verses, and verse cross-references.
- **Seed data test:** Confirms the database is seeded with the expected data after the ETL runs.

A shared fixture runs the ETL process and makes its results available to multiple test runs. This avoids re-running the full pipeline for every test, which keeps the E2E tests faster and ensures every test checks the same loaded data.

## Notable Areas for Improvement

### Real-Data Validation in E2E Tests

- **Current Approach:** The E2E tests check structure, counts, and integrity, while validation of specific book, chapter, and verse values relies mostly on unit tests that use mock data.
- **Planned Enhancement:** Add checks of actual book, chapter, and verse values to the E2E tests, so the real data loaded at the ETL level is validated directly instead of only through mock data in the unit tests.