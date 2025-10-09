def parse_object_id(obj: dict | list[dict]):
    if type(obj) is list:
        return [{**x, '_id': str(x['_id'])} for x in obj]
    else:
        return {**obj, '_id': str(obj['_id'])}
