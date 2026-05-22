def build_id_map(from_items, to_ids, key):
    """
    Build a mapping from one or more fields in each input item
    to the corresponding ID at the same index in `to_ids`.

    If `key` is a string:
        key = "book_id"
        → mapping key is item["book_id"]

    If `key` is a list/tuple of strings:
        key = ["book_id", "chapter_number"]
        → mapping key is (item["book_id"], item["chapter_number"])

    IMPORTANT:
    The order of `from_items` MUST match the order of `to_ids`.
    SQLAlchemy RETURNING preserves insert order, so this function
    relies on positional alignment.
    """
    # Normalize key into a tuple of keys
    if isinstance(key, str):
        key_fields = (key,)
        single_value_key = True
    else:
        key_fields = tuple(key)
        single_value_key = False
    
    mapping = {}
    for item, to_id in zip(from_items, to_ids):
        if single_value_key:
            map_key = item[key_fields[0]]
        else:
            map_key = tuple(item[field] for field in key_fields)

        mapping[map_key] = to_id

    return mapping
