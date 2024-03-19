from typing import Optional
from uuid import uuid4

from ..common.label_creator import LabelCreator
from ..common.utils import set_properties, unique_string_builder, is_sublist
from .label import Cuboid
from ..common.label import ClassType


class CuboidCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_cuboid_coord(self):
        return {
            "position": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "rotation_quaternion": {
                "x": 0,
                "y": 0,
                "z": 0,
                "w": 0
            },
            "size": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        }

    def create(
        self,
        class_name: str,
        frames: list,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: Optional[int] = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.CUBOID,
        ) in self.object_classes_map.keys()
        coord = frames[0]["annotation"]["coord"]
        assert is_sublist(
            ["position", "rotation_quaternion", "size"],
            coord.keys(),
        )
        return Cuboid(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[
                unique_string_builder(
                    class_name,
                    ClassType.CUBOID,
                )
            ]["id"],
            frames=frames,
            meta=meta if meta else self._get_meta(
                class_name, ClassType.CUBOID),
            properties_def=self.object_classes_map[
                unique_string_builder(
                    class_name,
                    ClassType.CUBOID,
                )
            ]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )
