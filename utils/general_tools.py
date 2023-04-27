import json


def json_to_dict_parse(json_structure: str) -> dict:
    """
    Utility function responsible for parsing json to python dict. Function includes replacing critical characters.

    Parameters
    ----------
    json : str
        Json to parse.

    Returns
    -------
    dict
        Dictionary created based on json structure.

    """
    translation_tabele = [
        ("'", '"'),
        ("False", "false"),
        ("True", "true"),
        ("None", "null"),
    ]
    for pair in translation_tabele:
        json_structure = json_structure.replace(*pair)
    return json.loads(json_structure)
