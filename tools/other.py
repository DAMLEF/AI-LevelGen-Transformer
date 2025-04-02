def dict_add(d: dict, nd: dict):
    result = {}

    for k, v in nd.items():
        result[k] = v

    for k, v in d.items():
        result[k] = v

    return result
