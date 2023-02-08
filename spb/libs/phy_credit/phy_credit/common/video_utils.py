from collections import Counter
from typing import Any, Dict, List

from ..common.utils import (add_class_id, count_properties,
                            expand_options, remove_free_response)

JsonDict = Dict[str, Any]


def get_video_frame_properties(object: JsonDict) -> List[JsonDict]:
    result = []
    for frame in object.get("frames", []):
        properties_in_frame = [
            add_class_id(property, object) for property in frame.get("properties", [])
        ]
        result.extend(properties_in_frame)
    return result


def get_video_label_properties(object: JsonDict) -> List[JsonDict]:
    return [add_class_id(property, object) for property in object.get("properties", [])]


def flatten_video_obj_properties(objects: List[JsonDict]) -> List[JsonDict]:
    result = []
    for object in objects:
        result.extend(get_video_frame_properties(object))
        result.extend(get_video_label_properties(object))
    return result


def preprocess_video_obj_properties(objects: List[JsonDict]) -> List[JsonDict]:
    return expand_options(remove_free_response(flatten_video_obj_properties(objects)))


def calculate_video_properties_count(objects):
    properties = preprocess_video_obj_properties(objects)
    return count_properties(properties)


def calculate_annotated_frame_count(objects: List[JsonDict]) -> int:
    # include frames which have annotated objects (exclude categories)
    annotations = [
        annotation for obj in objects for annotation in obj["frames"]]
    frame_number_to_anno_count = Counter(anno["num"] for anno in annotations)
    return len(frame_number_to_anno_count)
