"""
CLI utility for initializing Bible content tables in a selected database environment.

This script provides a controlled entry point for recreating the Bible content
tables used by the Pleiades application. It supports multiple database targets
(e.g., 'prod' and 'test') and loads the appropriate connection URL from the
project's .env file. The ingestion logic itself is implemented in a referenced
module, which performs async API calls and database writes.

Example usage against the test database with logging enabled:
    python init_db.py --env test --log
        --env : Required. Chooses which database URL to load (prod or test).
        --log : Optional. Enables verbose logging during ingestion.

This tool is intentionally environment‑aware to prevent accidental writes to the
wrong database. It should be used whenever you need to refresh the
Bible content tables for development or testing.
"""

# ------------------------------------------------------------
# Standard library
# ------------------------------------------------------------
import argparse

# ------------------------------------------------------------
# Third‑party packages
# ------------------------------------------------------------
from sqlalchemy import create_engine
import asyncio # essentially an async version of requests

# ------------------------------------------------------------
# Local modules
# ------------------------------------------------------------
from ingest_bible import initialize_bible_content
from util import get_db_engine


def parse_args():
    parser = argparse.ArgumentParser(description="Recreates Bible content tables in a user-specified database")
    parser.add_argument(
        "--env",
        required=True, 
        help="Database environment to run code against (e.g., prod, test)"
    ) # no action, so value is required
    parser.add_argument(
        "--log", 
        action="store_true", 
        help="Flag to print execution events during run of script"
    ) # store_true treats the arg as a boolean flag
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    env_alias = args.env
    include_logs = args.log

    engine = get_db_engine(env_alias)

    asyncio.run(initialize_bible_content(engine, log_mode=include_logs)) # asyncio is needed to run async functions from a main function