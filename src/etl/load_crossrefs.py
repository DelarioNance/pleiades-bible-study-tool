from sqlalchemy import MetaData, insert, bindparam

from src.etl.mappings import CROSSREF_TO_HELLO_API_BOOK_ID_MAPPING
from src.etl.data_test_seed import TEST_VERSE_REFERENCES


def load_verse_crossrefs_non_test(conn, crossrefs, verse_id_mapping_api_to_db):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    crossrefs_table = metadata_obj.tables['verse_references']

    insert_stmt = (
        insert(crossrefs_table)
        .values(
            from_id=bindparam('from_verse_id'),
            to_id=bindparam('to_verse_id'),
            num_votes=bindparam('num_votes'),
            is_test=False
        )
        .returning(crossrefs_table.c.id)
    )

    crossrefs_with_db_verse_ids = [
        {
            **crossref,
            'from_verse_id': verse_id_mapping_api_to_db[(
                CROSSREF_TO_HELLO_API_BOOK_ID_MAPPING[crossref['from_book_name']],
                int(crossref['from_chapter_num']),
                int(crossref['from_verse_num'])
            )],
            'to_verse_id': verse_id_mapping_api_to_db[(
                CROSSREF_TO_HELLO_API_BOOK_ID_MAPPING[crossref['to_book_name']],
                int(crossref['to_chapter_num']),
                int(crossref['to_verse_num'])
            )],
            'num_votes': int(crossref['num_votes']),
        }
        for crossref in crossrefs 
        if crossref['from_book_name'] + '.' + crossref['from_chapter_num'] + '.' + crossref['from_verse_num'] != '3John.1.15' # the verse cross-reference data has a reference to a non-existent verse (3 John 1:15), so we need to filter it out
    ]
    
    conn.execute(insert_stmt, crossrefs_with_db_verse_ids)


def load_verse_crossrefs_test(conn, test_verse_id_mapping):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=conn)
    crossrefs_table = metadata_obj.tables['verse_references']

    insert_stmt = (
        insert(crossrefs_table)
        .values(
            from_id=bindparam('from_verse_id'),
            to_id=bindparam('to_verse_id'),
            num_votes=bindparam('num_votes'),
            is_test=True
        )
        .returning(crossrefs_table.c.id)
    )

    test_crossrefs_with_db_verse_ids = [
        {
            **crossref,
            'from_verse_id': test_verse_id_mapping[(
                crossref['from_book_name'],
                int(crossref['from_chapter_number']),
                int(crossref['from_verse_number'])
            )],
            'to_verse_id': test_verse_id_mapping[(
                crossref['to_book_name'],
                int(crossref['to_chapter_number']),
                int(crossref['to_verse_number'])
            )],
        }
        for crossref in TEST_VERSE_REFERENCES
    ]

    conn.execute(insert_stmt, test_crossrefs_with_db_verse_ids)