from uuid import uuid4

from ..common.label_creator import LabelCreator
from ..common.utils import dim, set_properties
from .video_label import Box, Cuboid2D, Keypoint, Polygon, Polyline, RotatedBox


class BoxCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_box_coord(self):
        return {
            "x": 0.0,
            "y": 0.0,
            "width": 0.0,
            "height": 0.0,
        }

    def create(
        self,
        class_name: str,
        nums: list,
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert class_name in self.object_classes_map.keys()
        assert list(coord.keys()) == [
            "x",
            "y",
            "width",
            "height",
        ]
        return Box(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=[
                {
                    "num": num,
                    "annotation": {
                        "coord": coord,
                        "meta": meta if meta else self._get_meta(class_name),
                    },
                    "properties": set_properties(
                        self.object_classes_map[class_name]["properties"],
                        properties,
                    ),
                }
                for num in nums
            ],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, box):
        class_name = box["class_name"]
        assert class_name in self.object_classes_map.keys()
        assert list(box["frame"][0]["annotation"]["coord"]) == [
            "x",
            "y",
            "width",
            "height",
        ]
        return Box(
            id=box["id"] if "id" in box else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=box["frame"],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=box["properties"] if "properties" in box else [],
            tracking_id=box["tracking_id"] if "tracking_id" in box else 0,
        )


class RotatedBoxCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_rotated_box_coord(self):
        return {
            "cx": 0.0,
            "cy": 0.0,
            "width": 0.0,
            "height": 0.0,
            "angle": 0.0,
        }

    def create(
        self,
        class_name: str,
        nums: list,
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert class_name in self.object_classes_map.keys()
        assert list(coord.keys()) == [
            "cx",
            "cy",
            "width",
            "height",
            "angle",
        ]
        return RotatedBox(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=[
                {
                    "num": num,
                    "annotation": {
                        "coord": coord,
                        "meta": meta if meta else self._get_meta(class_name),
                    },
                    "properties": set_properties(
                        self.object_classes_map[class_name]["properties"],
                        properties,
                    ),
                }
                for num in nums
            ],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, rbox):
        class_name = rbox["class_name"]
        assert class_name in self.object_classes_map.keys()
        assert list(rbox["frame"][0]["annotation"]["coord"]) == [
            "cx",
            "cy",
            "width",
            "height",
            "angle",
        ]
        return RotatedBox(
            id=rbox["id"] if "id" in rbox else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=rbox["frame"],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=rbox["properties"] if "properties" in rbox else [],
            tracking_id=rbox["tracking_id"] if "tracking_id" in rbox else 0,
        )


class PolylineCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_polyline_coord(self, multiple=True):
        if multiple:
            points = [[{"x": 0, "y": 0}]]
        else:
            points = [{"x": 0, "y": 0}]

        return {"points": points}

    def create(
        self,
        class_name: str,
        nums: list,
        coord: dict,
        multiple: bool = True,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert class_name in self.object_classes_map.keys()
        assert list(coord.keys()) == ["points"]

        if dim(coord["points"]) == 1:
            multiple = False

        return Polyline(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=[
                {
                    "num": num,
                    "annotation": {
                        "multiple": multiple,
                        "coord": coord,
                        "meta": meta if meta else self._get_meta(class_name),
                    },
                    "properties": set_properties(
                        self.object_classes_map[class_name]["properties"],
                        properties,
                    ),
                }
                for num in nums
            ],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, polyline):
        class_name = polyline["class_name"]
        assert class_name in self.object_classes_map.keys()
        assert list(polyline["frame"][0]["annotation"]["coord"]) == ["points"]
        return Polyline(
            id=polyline["id"] if "id" in polyline else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=polyline["frame"],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=polyline["properties"]
            if "properties" in polyline
            else [],
            tracking_id=polyline["tracking_id"]
            if "tracking_id" in polyline
            else 0,
        )


class PolygonCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_polyline_coord(self, multiple=True):
        if multiple:
            points = [[[{"x": 0, "y": 0}]]]
        else:
            points = [{"x": 0, "y": 0}]
        return {"points": points}

    def create(
        self,
        class_name: str,
        nums: list,
        coord: dict,
        multiple: bool = True,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert class_name in self.object_classes_map.keys()
        assert list(coord.keys()) == ["points"]

        if dim(coord["points"]) == 1:
            multiple = False

        return Polygon(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=[
                {
                    "num": num,
                    "annotation": {
                        "multiple": multiple,
                        "coord": coord,
                        "meta": meta if meta else self._get_meta(class_name),
                    },
                    "properties": set_properties(
                        self.object_classes_map[class_name]["properties"],
                        properties,
                    ),
                }
                for num in nums
            ],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, polygon):
        class_name = polygon["class_name"]
        assert class_name in self.object_classes_map.keys()
        assert list(polygon["frame"][0]["annotation"]["coord"]) == ["points"]
        return Polygon(
            id=polygon["id"] if "id" in polygon else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=polygon["frame"],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=polygon["properties"]
            if "properties" in polygon
            else [],
            tracking_id=polygon["tracking_id"]
            if "tracking_id" in polygon
            else 0,
        )


class KeypointCreator(LabelCreator):
    def __init__(self, object_classes_map, keypoint_map):
        super().__init__(object_classes_map)
        self.keypoint_map = keypoint_map

    def get_default_keypoint_coord(self, keypoint_interface_id):
        return {
            "points": [
                {
                    "name": point["name"],
                    "x": 0.0,
                    "y": 0.0,
                    "state": {
                        "visible": True,
                        "valid": True,
                    },
                }
                for point in self.keypoint_map[keypoint_interface_id]["points"]
            ]
        }

    def get_default_keypoint_legacy_coord(self, keypoint_interface_id):
        return {
            "graph": {
                "nodes": [
                    {
                        "x": 0.0,
                        "y": 0.0,
                    }
                    for _ in self.keypoint_map[keypoint_interface_id]["points"]
                ],
                "states": [
                    {"state": {"visible": True}}
                    for _ in self.keypoint_map[keypoint_interface_id]["points"]
                ],
            }
        }

    def create(
        self,
        class_name: str,
        nums: list,
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert class_name in self.object_classes_map.keys()
        assert list(coord.keys()) == ["points"]
        return Keypoint(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=[
                {
                    "num": num,
                    "annotation": {
                        "coord": coord,
                        "meta": meta if meta else self._get_meta(class_name),
                    },
                    "properties": set_properties(
                        self.object_classes_map[class_name]["properties"],
                        properties,
                    ),
                }
                for num in nums
            ],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, keypoint):
        class_name = keypoint["class_name"]
        assert class_name in self.object_classes_map.keys()
        assert list(keypoint["frame"][0]["annotation"]["coord"]) == ["points"]
        return Keypoint(
            id=keypoint["id"] if "id" in keypoint else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=keypoint["frame"],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=keypoint["properties"]
            if "properties" in keypoint
            else [],
            tracking_id=keypoint["tracking_id"]
            if "tracking_id" in keypoint
            else 0,
        )


class Cuboid2DCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_cuboid2d_coord(self):
        return {
            "near": {
                "x": 0.0,
                "y": 0.0,
                "width": 0.0,
                "height": 0.0,
            },
            "far": {
                "x": 0.0,
                "y": 0.0,
                "width": 0.0,
                "height": 0.0,
            },
        }

    def create(
        self,
        class_name: str,
        nums: list,
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert class_name in self.object_classes_map.keys()
        assert list(coord.keys()) == ["near", "far"]
        return Cuboid2D(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=[
                {
                    "num": num,
                    "annotation": {
                        "coord": coord,
                        "meta": meta if meta else self._get_meta(class_name),
                    },
                    "properties": set_properties(
                        self.object_classes_map[class_name]["properties"],
                        properties,
                    ),
                }
                for num in nums
            ],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, cuboid2d):
        class_name = cuboid2d["class_name"]
        assert class_name in self.object_classes_map.keys()
        assert list(cuboid2d["frame"][0]["annotation"]["coord"]) == [
            "near",
            "far",
        ]
        return Cuboid2D(
            id=cuboid2d["id"] if "id" in cuboid2d else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[class_name]["id"],
            frames=cuboid2d["frame"],
            properties_def=self.object_classes_map[class_name]["properties"],
            properties=cuboid2d["properties"]
            if "properties" in cuboid2d
            else [],
            tracking_id=cuboid2d["tracking_id"]
            if "tracking_id" in cuboid2d
            else 0,
        )
