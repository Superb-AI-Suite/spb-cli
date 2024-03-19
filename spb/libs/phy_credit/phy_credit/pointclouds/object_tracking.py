from typing import Optional

from ..common.object_interface import ObjectInterfaceDef


class ObjectTrackingDef(ObjectInterfaceDef):
    def __init__(
        self,
        object_groups: list = [],
        object_classes: list = [],
        annotation_types: list = [],
    ):
        super().__init__(
            keypoints=None,
            object_groups=object_groups,
            object_classes=object_classes,
            annotation_types=annotation_types,
        )

    @classmethod
    def get_default(cls):
        return cls(
            object_groups=[],
            object_classes=[],
            annotation_types=[],
        )

    @classmethod
    def from_dict(cls, object_detection_dict: dict):
        return cls(
            object_groups=object_detection_dict["object_groups"],
            object_classes=object_detection_dict["object_classes"],
            annotation_types=object_detection_dict["annotation_types"],
        )

    def add_cuboid(
        self,
        name: str,
        id: Optional[str] = None,
        color: Optional[str] = None,
        properties: list = [],
    ):
        self.add_object_class(name, "cuboid", color, properties, id)

    def add_box(self): raise NotImplementedError

    def add_rbox(self): raise NotImplementedError

    def add_polyline(self): raise NotImplementedError

    def add_polygon(self): raise NotImplementedError

    def add_2dcuboid(self): raise NotImplementedError

    def add_keypoint(self): raise NotImplementedError

    def to_dict(self):
        return {
            "object_groups": self.object_groups,
            "object_classes": self.object_classes,
            "annotation_types": self.annotation_types,
        }
