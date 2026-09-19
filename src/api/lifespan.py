# https://fastapi.tiangolo.com/advanced/events/#use-case

import os

from fastapi.concurrency import asynccontextmanager

from src.db.utils import get_db_engine
from src.etl.pipeline import pipeline

# async is used because FastAPI requires it
@asynccontextmanager
async def lifespan(app):
    env = os.getenv("PLEIADES_ENV", "sandbox").lower() # may want to tightly couple with similar code in get_current_engine
    if env == "staging":
        engine = get_db_engine(env)
        await pipeline(
            bible_api_url="https://bible.helloao.org/api/eng_kjv", 
            engine=engine
        ) # will want to extract this to a utility for maintainability/simplicity

    # No need to force an ETL run for sandbox.

    # Could be worth forcing an ETL run testing (i.e., CI),
    # but I don't think so right now since the CI tests
    # for the ETL already run the ETL pipeline. 

    yield

    # No shutdown tasks needed for now.