import random
from uuid import uuid4

from ..common.object_interface import ObjectInterfaceDef


class ObjectDetectionDef(ObjectInterfaceDef):
    def __init__(
        self,
        keypoints: list = [],
        object_groups: list = [],
        object_classes: list = [],
        annotation_types: list = [],
    ):
        super().__init__(
            keypoints=keypoints,
            object_groups=object_groups,
            object_classes=object_classes,
            annotation_types=annotation_types,
        )
