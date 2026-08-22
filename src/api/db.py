import os
from src.db.utils import get_db_engine

env = os.getenv("PLEIADES_ENV", "sandbox")
engine = get_db_engine(env)