"""
Command‑line entry point for running the full Bible ETL pipeline.

The ETL pipeline itself (extraction, transformation, and loading of books,
chapters, verses, and cross‑references) is implemented in src.etl.pipeline.
This script is the correct and intended way to execute the pipeline:

    python -m src.etl.run_etl <environment>

Example:
    python -m src.etl.run_etl sandbox

The -m and module path style of invocation (python -m src.etl.run_etl) 
lets the script be executed as a module within the src package, 
which is important for resolving imports correctly.
"""

import sys
import time
import asyncio

from src.utils.db import get_db_engine
from src.etl.pipeline import main


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_etl.py <environment>")
        print("Example: python run_etl.py sandbox")
        sys.exit(1)

    env = sys.argv[1]

    print("=== Starting Bible ETL Pipeline ===")
    print(f"Running ETL against environment: {env}")
    print()

    engine = get_db_engine(env)

    start = time.perf_counter()
    asyncio.run(main(
        bible_api_url="https://bible.helloao.org/api/eng_kjv", 
        engine=engine
    ))
    elapsed = time.perf_counter() - start

    print()
    print(f"ETL completed in {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
