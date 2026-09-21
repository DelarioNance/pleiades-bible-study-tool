# https://fastapi.tiangolo.com/advanced/events/#use-case

import os

from fastapi.concurrency import asynccontextmanager
from sqlalchemy import text

from src.db.utils import get_db_engine
from src.etl.pipeline import pipeline


ETL_LOCK_ID = 987654  

# async is used because FastAPI requires it
@asynccontextmanager
async def lifespan(app):
    env = os.getenv("PLEIADES_ENV", "sandbox").lower() # may want to tightly couple with similar code in get_current_engine
    if env == "staging":
        engine = get_db_engine(env)

        # We don't want every worker to run ETL on startup. Technically,
        # two workers could both run ETL if one worker's attempt to 
        # run ETL is delayed for the length of time it takes the other
        # worker to finish. However, this should be unlikely and is not
        # the end of the world if it happens. 
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT pg_try_advisory_lock({ETL_LOCK_ID});"))
            got_lock = result.scalar()

        if not got_lock:
            print("ETL already running or completed; skipping.")
            return
        
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