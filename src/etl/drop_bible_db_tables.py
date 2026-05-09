from sqlalchemy import MetaData, Table


def drop_bible_db_tables(session, table_names_ordered): # should be ordered in drop order
    engine = session.get_bind() # the engine used to build the session
    
    metadata = MetaData()

    for table_name in table_names_ordered: # order matters here due to foreign key constraints
        table_reflection = Table(table_name, metadata, autoload_with=engine) # reflection is a way to reference the DB table in Python
        table_reflection.drop(bind=engine, checkfirst=True) # effects are immediate unless inside a transaction (session), in which case they are pending until commit
