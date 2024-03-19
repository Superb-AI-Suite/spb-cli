from abc import ABC
from enum import Enum
from typing import Union


class ClassType(Enum):
    BOX = "box"
    RBOX = "rbox"
    POLYLINE = "polyline"
    POLYGON = "polygon"
    KEYPOINT = "keypoint"
    CUBOID2D = "cuboid2d"
    CUBOID = "cuboid"

    @staticmethod
    def is_valid_class_type(class_type: Union[str, 'ClassType']):
        if isinstance(class_type, ClassType):
            return True
        elif isinstance(class_type, str):
            return class_type in [member.value for member in ClassType]
        else:
            return False


class Label(ABC):
    def __init__(self, attributes):
        self.id = attributes["id"]
        self.class_name = attributes["class_name"]
        self.class_id = attributes["class_id"]
        self.properties_def = attributes["properties_def"]
        self.properties = attributes["properties"]
        self.tracking_id = attributes["tracking_id"]
        self.annotation_type = None

    def to_dict(self):
        pass
