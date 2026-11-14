import os

from src.db.utils import get_db_engine

engine = get_db_engine(os.getenv("PLEIADES_ENV"))
