from typing import Any, Dict, List

JsonDict = Dict[str, Any]


def add_class_id(property: JsonDict, object: JsonDict):
    return {**property, "class_id": object["class_id"]}


def count_properties(properties):
    result = {}

    for property in properties:
        unique_option_id = property["property_option_id"]
        if unique_option_id not in result:
            result[unique_option_id] = {**property, "count": 1}
        else:
            result[unique_option_id]["count"] += 1

    return list(result.values())


def _unique_option_id(property_id: str, option_id: str) -> str:
    return f"{property_id}#{option_id}"


def _format_radio_option(property) -> JsonDict:
    return {
        "class_id": property["class_id"],
        "property_id": property["property_id"],
        "property_name": property["property_name"],
        "option_id": property["option_id"],
        "option_name": property["option_name"],
        "property_option_id": _unique_option_id(
            property["property_id"], property["option_id"]
        ),
    }


def _flatten_and_format_checkbox_options(property: JsonDict) -> List[JsonDict]:
    option_ids = property["option_ids"]
    option_names = property["option_names"]

    return [
        {
            "class_id": property["class_id"],
            "property_id": property["property_id"],
            "property_name": property["property_name"],
            "option_id": option_id,
            "option_name": option_names[idx],
            "property_option_id": _unique_option_id(
                property["property_id"], option_id
            ),
        }
        for (idx, option_id) in enumerate(option_ids)
    ]


def expand_options(properties: List[JsonDict]) -> List[JsonDict]:
    result = []

    def check_valid_radio_option(property):
        return property.get("option_id") is not None

    def check_valid_checkbox(property):
        # check fields not null and has len > 0
        return property["option_ids"] and property["option_names"]

    def list_options(property):
        if property.get("type") == "radio" and check_valid_radio_option(
            property
        ):
            return [_format_radio_option(property)]
        if property.get("type") == "checkbox" and check_valid_checkbox(
            property
        ):
            return _flatten_and_format_checkbox_options(property)
        return []

    return [o for property in properties for o in list_options(property)]


def remove_free_response(properties: List[JsonDict]) -> List[JsonDict]:
    return [
        property
        for property in properties
        if property.get("type") in ["radio", "checkbox"]
    ]


def get_opt_map(options: list) -> dict:
    res = {}
    for opt in options:
        if "children" in opt:
            res.update(get_opt_map(opt["children"]))
        else:
            res[opt["name"]] = opt
    return res


def set_properties(properties_def, properties):
    prop_def_map = {prop_def["name"]: prop_def for prop_def in properties_def}
    converted_properties = []
    for prop in properties:
        prop_def = prop_def_map[prop["name"]]
        if prop_def["type"] in ["radio", "dropdown", "checkbox"]:
            opt_map = get_opt_map(prop_def["options"])
            if prop_def["type"] == "checkbox":
                converted_properties.append(
                    {
                        "type": prop_def["type"],
                        "property_id": prop_def["id"],
                        "property_name": prop_def["name"],
                        "option_ids": [
                            opt_map[val]["id"] for val in prop["value"]
                        ],
                        "option_names": [
                            opt_map[val]["name"] for val in prop["value"]
                        ],
                    }
                )
            else:
                converted_properties.append(
                    {
                        "type": prop_def["type"],
                        "property_id": prop_def["id"],
                        "property_name": prop_def["name"],
                        "option_id": opt_map[prop["value"]]["id"],
                        "option_name": opt_map[prop["value"]]["name"],
                    }
                )
        elif prop_def["type"] == "free response":
            converted_properties.append(
                {
                    "type": prop_def["type"],
                    "property_id": prop_def["id"],
                    "property_name": prop_def["name"],
                    "value": prop["value"],
                }
            )
    return converted_properties


def get_properties(properties_def, properties):
    prop_def_map = {prop_def["name"]: prop_def for prop_def in properties_def}
    converted_properties = []
    for prop in properties:
        prop_def = prop_def_map[prop["property_name"]]
        if prop_def["type"] in ["radio", "dropdown"]:
            converted_properties.append(
                {
                    "name": prop["property_name"],
                    "value": prop["option_name"],
                }
            )
        elif prop_def["type"] == "checkbox":
            converted_properties.append(
                {
                    "name": prop["property_name"],
                    "value": prop["option_names"],
                }
            )
        elif prop_def["type"] == "free response":
            converted_properties.append(
                {
                    "name": prop["property_name"],
                    "value": prop["value"],
                }
            )
    return converted_properties


def dim(arr):
    if not type(arr) == list:
        return []
    return [len(arr)] + dim(arr[0])
