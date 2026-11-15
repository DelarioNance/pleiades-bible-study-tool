def build_id_map(from_items, to_ids, key):
    """
    Map each item's key to the ID at the same position in `to_ids`.

    Args:
        from_items: Dicts to build keys from, in the same order as `to_ids`.
        to_ids: IDs to pair with the items, one per item.
        key: Field(s) in each item that identify it.
            - str: the map key is that field's value.
            - list/tuple of str: the map key is a tuple of those fields' values.

    IMPORTANT:
    The order of `from_items` MUST match the order of `to_ids`.
    SQLAlchemy RETURNING preserves insert order, so this function
    relies on positional alignment.
    """
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

def _normalize_key(item, key_fields):
    if len(key_fields) == 1:
        return item[key_fields[0]]
    else:
        return tuple(item[field] for field in key_fields)