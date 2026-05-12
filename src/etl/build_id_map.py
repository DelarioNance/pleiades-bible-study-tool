def build_id_map(items, db_ids, key):
    return {
        item[key]: db_id
        for item, db_id in zip(items, db_ids)
    }
