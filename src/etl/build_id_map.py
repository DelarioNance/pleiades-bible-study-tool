def build_id_map(from_items, to_ids, key):
    """
    Build a mapping from an input item's key to an 
    id value at the same index in a user-specified list.
    """
    return {
        item[key]: db_id
        for item, db_id in zip(from_items, to_ids)
    }
