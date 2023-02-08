from typing import Any, Dict, List
from ..common.utils import (add_class_id, count_properties,
                            expand_options, remove_free_response)

JsonDict = Dict[str, Any]


def flatten_img_obj_properties(objects: List[JsonDict]) -> List[JsonDict]:
    return [
        add_class_id(property, obj)
        for obj in objects
        for property in obj["properties"]
    ]


def preprocess_image_obj_properties(objects):
    return expand_options(remove_free_response(flatten_img_obj_properties(objects)))


def calculate_imageV2_properties_count(objects):
    properties = preprocess_image_obj_properties(objects)
    return count_properties(properties)
