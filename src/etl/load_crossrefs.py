from sqlalchemy import MetaData, insert, bindparam

from src.etl.mappings import CROSSREF_TO_HELLO_API_BOOK_ID_MAPPING

def load_verse_crossrefs(conn, crossrefs, verse_id_mapping_api_to_db):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    crossrefs_table = metadata_obj.tables['verse_references']

    insert_stmt = (
        insert(crossrefs_table)
        .values(
            from_id=bindparam('from_verse_id'),
            to_id=bindparam('to_verse_id'),
        )
        .returning(crossrefs_table.c.id)
    )

    crossrefs_with_db_verse_ids = [
        {
            **crossref,
            'from_verse_id': verse_id_mapping_api_to_db[(
                CROSSREF_TO_HELLO_API_BOOK_ID_MAPPING[crossref['from_book']],
                int(crossref['from_chapter']),
                int(crossref['from_verse'])
            )],
            'to_verse_id': verse_id_mapping_api_to_db[(
                CROSSREF_TO_HELLO_API_BOOK_ID_MAPPING[crossref['to_book']],
                int(crossref['to_chapter']),
                int(crossref['to_verse'])
            )],
        }
        for crossref in crossrefs
    ]
    
    conn.execute(insert_stmt, crossrefs_with_db_verse_ids)