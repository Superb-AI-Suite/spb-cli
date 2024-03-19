from uuid import uuid4

from ..common.label_creator import LabelCreator
from ..common.label import ClassType
from ..common.utils import dim, unique_string_builder, is_sublist
from .image_label import Box, Cuboid2D, Keypoint, Polygon, Polyline, RotatedBox


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
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.BOX,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["x", "y", "width", "height"],
            coord.keys(),
        )

        return Box(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.BOX,
            )]["id"],
            coord=coord,
            meta=meta if meta else self._get_meta(class_name, ClassType.BOX),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.BOX,
            )]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, box):
        class_name = box["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.BOX,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["x", "y", "width", "height"],
            box["annotation"]["coord"].keys(),
        )

        properties = box["properties"] if "properties" in box else []
        return Box(
            id=box["id"] if "id" in box else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.BOX,
            )]["id"],
            coord=box["annotation"]["coord"],
            meta=box["annotation"]["meta"] if "meta" in box["annotation"] else self._get_meta(
                class_name,
                ClassType.BOX,
            ),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.BOX,
            )]["properties"],
            properties=properties,
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
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.RBOX,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["cx", "cy", "width", "height", "angle"],
            coord.keys(),
        )

        return RotatedBox(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.RBOX,
            )]["id"],
            coord=coord,
            meta=meta if meta else self._get_meta(class_name, ClassType.RBOX),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.RBOX,
            )]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, rbox):
        class_name = rbox["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.RBOX,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["cx", "cy", "width", "height", "angle"],
            rbox["annotation"]["coord"].keys()
        )

        properties = rbox["properties"] if "properties" in rbox else []
        return RotatedBox(
            id=rbox["id"] if "id" in rbox else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.RBOX,
            )]["id"],
            coord=rbox["annotation"]["coord"],
            meta=rbox["annotation"]["meta"]
            if "meta" in rbox["annotation"]
            else self._get_meta(class_name, ClassType.RBOX),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.RBOX,
            )]["properties"],
            properties=properties,
            tracking_id=rbox["tracking_id"] if "tracking_id" in rbox else 0,
        )


class PolylineCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_polyline_coord(self):
        return {"points": [[{"x": 0, "y": 0}]]}

    def create(
        self,
        class_name: str,
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.POLYLINE,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["points"],
            coord.keys(),
        )
        assert len(dim(coord["points"])) == 2
        assert dim(coord["points"])[-1] >= 1

        return Polyline(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYLINE,
            )]["id"],
            coord=coord,
            multiple=True,
            meta=meta if meta else self._get_meta(
                class_name, ClassType.POLYLINE),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYLINE,
            )]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, polyline):
        class_name = polyline["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.POLYLINE,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["points"],
            polyline["annotation"]["coord"].keys(),
        )
        assert len(dim(polyline["annotation"]["coord"]["points"])) == 2
        assert dim(polyline["annotation"]["coord"]["points"])[-1] >= 1
        properties = polyline["properties"] if "properties" in polyline else []

        return Polyline(
            id=polyline["id"] if "id" in polyline else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYLINE
            )]["id"],
            coord=polyline["annotation"]["coord"],
            multiple=True,
            meta=polyline["annotation"]["meta"]
            if "meta" in polyline["annotation"]
            else self._get_meta(class_name, ClassType.POLYLINE),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYLINE
            )]["properties"],
            properties=properties,
            tracking_id=polyline["tracking_id"]
            if "tracking_id" in polyline
            else 0,
        )


class PolygonCreator(LabelCreator):
    def __init__(self, object_classes_map):
        super().__init__(object_classes_map)

    def get_default_polyline_coord(self):
        return {"points": [[[{"x": 0, "y": 0}]]]}

    def create(
        self,
        class_name: str,
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.POLYGON,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["points"],
            coord.keys(),
        )
        assert len(dim(coord["points"])) == 3
        assert dim(coord["points"])[-1] >= 3

        return Polygon(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYGON,
            )]["id"],
            coord=coord,
            multiple=True,
            meta=meta if meta else self._get_meta(
                class_name, ClassType.POLYGON),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYGON,
            )]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, polygon):
        class_name = polygon["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.POLYGON,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["points"],
            polygon["annotation"]["coord"].keys(),
        )
        assert len(dim(polygon["annotation"]["coord"]["points"])) == 3
        assert dim(polygon["annotation"]["coord"]["points"])[-1] >= 3

        properties = polygon["properties"] if "properties" in polygon else []

        return Polygon(
            id=polygon["id"] if "id" in polygon else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYGON,
            )]["id"],
            coord=polygon["annotation"]["coord"],
            multiple=True,
            meta=polygon["annotation"].get("meta", None)
            if "meta" in polygon["annotation"]
            else self._get_meta(class_name, ClassType.POLYGON),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYGON,
            )]["properties"],
            properties=properties,
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
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.KEYPOINT,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["points"],
            coord.keys(),
        )
        assert is_sublist(
            ["x", "y"],
            coord["points"][0].keys(),
        )

        return Keypoint(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.KEYPOINT,
            )]["id"],
            coord=coord,
            meta=meta if meta else self._get_meta(
                class_name, ClassType.KEYPOINT),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.KEYPOINT,
            )]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, keypoint):
        class_name = keypoint["class_name"]
        coord = keypoint["annotation"]["coord"]

        assert unique_string_builder(
            class_name,
            ClassType.KEYPOINT,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["points"],
            coord.keys(),
        )
        assert is_sublist(
            ["x", "y"],
            coord["points"][0].keys(),
        )

        return Keypoint(
            id=keypoint["id"] if "id" in keypoint else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.KEYPOINT,
            )]["id"],
            coord=coord,
            meta=keypoint["annotation"]["meta"]
            if "meta" in keypoint["annotation"]
            else self._get_meta(class_name, ClassType.KEYPOINT),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.KEYPOINT,
            )]["properties"],
            properties=keypoint["properties"] if "properties" in keypoint else [
            ],
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
        coord: dict,
        meta: dict = {},
        properties: list = [],
        id: str = str(uuid4()),
        tracking_id: int = None,
    ):
        assert unique_string_builder(
            class_name,
            ClassType.CUBOID2D,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["near", "far"],
            coord.keys(),
        )

        return Cuboid2D(
            id=id,
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.CUBOID2D,
            )]["id"],
            coord=coord,
            meta=meta if meta else self._get_meta(
                class_name,
                ClassType.CUBOID2D
            ),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.CUBOID2D,
            )]["properties"],
            properties=properties,
            tracking_id=tracking_id,
        )

    def from_dict(self, cuboid2d):
        class_name = cuboid2d["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.CUBOID2D,
        ) in self.object_classes_map.keys()
        assert is_sublist(
            ["near", "far"],
            cuboid2d["annotation"]["coord"].keys()
        )

        properties = cuboid2d["properties"] if "properties" in cuboid2d else []
        a = Cuboid2D(
            id=cuboid2d["id"] if "id" in cuboid2d else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.CUBOID2D,
            )]["id"],
            coord=cuboid2d["annotation"]["coord"],
            meta=cuboid2d["annotation"]["meta"]
            if "meta" in cuboid2d["annotation"]
            else self._get_meta(class_name, ClassType.CUBOID2D),
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.CUBOID2D,
            )]["properties"],
            properties=properties,
            tracking_id=cuboid2d["tracking_id"]
            if "tracking_id" in cuboid2d
            else 0,
        )
        return a


class AutoLabelCreator(LabelCreator):
    def __init__(self, object_classes_map, keypoint_map):
        super().__init__(object_classes_map)
        self.keypoint_map = keypoint_map

    def create(self):
        raise NotImplementedError

    def from_dict(self, label):
        creators = [
            BoxCreator(self.object_classes_map),
            RotatedBoxCreator(self.object_classes_map),
            PolylineCreator(self.object_classes_map),
            PolygonCreator(self.object_classes_map),
            KeypointCreator(self.object_classes_map, self.keypoint_map),
            Cuboid2DCreator(self.object_classes_map),
        ]
        for creator in creators:
            try:
                return creator.from_dict(label)
            except:
                continue
        return None
