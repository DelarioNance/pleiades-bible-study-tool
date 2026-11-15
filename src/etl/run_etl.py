"""
Command-line entry point for the full Bible ETL pipeline.

The ETL functionality is implemented in src.etl.pipeline.

Run it as a module so imports within the src package resolve correctly:

    python -m src.etl.run_etl <environment>

Example:
    python -m src.etl.run_etl sandbox
"""

import asyncio
import sys
import time

from src.db.utils import get_db_engine
from src.etl.pipeline import pipeline


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python run_etl.py <environment>")
        print("Example: python run_etl.py sandbox")
        sys.exit(1) # convention: exit code 1 indicates an error

    env = sys.argv[1]

    print("=== Starting Bible ETL Pipeline ===")
    print(f"Running ETL against environment: {env}")
    print()

    engine = get_db_engine(env)
    load_test_data = env in ['sandbox', 'test']

    start = time.perf_counter()
    asyncio.run(pipeline(
        engine=engine,
        load_test_data=load_test_data,
    ))
    elapsed = time.perf_counter() - start

    print()
    print(f"ETL completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
