from uuid import uuid4

from ..common.label_creator import LabelCreator
from ..common.utils import dim, set_properties, unique_string_builder, is_sublist
from .video_label import Box, Cuboid2D, Keypoint, Polygon, Polyline, RotatedBox
from ..common.label import ClassType


class VideoLabelCreator(LabelCreator):
    def change_annotations_to_frames(self, label, annotation_type):
        if label.get("annotations") is not None:
            frames = []
            for annotation in label.get("annotations"):
                meta = annotation.get("meta") if annotation.get("meta") else self._get_meta(
                    label["class_name"],
                    annotation_type,
                )
                frames.append(
                    {
                        "num": annotation["frame_num"],
                        "properties": annotation["properties"],
                        "annotation": {
                            "coord": annotation.get("coord"),
                            "meta": meta,
                        },
                    }
                )
        elif label.get("frames") is not None:
            frames = []
            for frame in label.get("frames"):
                meta = frame["annotation"].get("meta") if frame["annotation"].get("meta") else self._get_meta(
                    label["class_name"],
                    annotation_type,
                )
                frames.append({
                    "num": frame["num"],
                    "properties": frame["properties"],
                    "annotation": {
                        "coord": frame["annotation"].get("coord"),
                        "meta": meta,
                    },
                })
        else:
            raise Exception("No frames or annotations in frame")
        return frames

class BoxCreator(VideoLabelCreator):
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
        raise NotImplementedError

    def from_dict(self, box):
        class_name = box["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.BOX
        ) in self.object_classes_map.keys()
        frames = self.change_annotations_to_frames(box, ClassType.BOX)
        coord = frames[0]["annotation"]["coord"]
        assert is_sublist(
            ["x", "y", "width", "height"],
            coord.keys(),
        )

        return Box(
            id=box["id"] if "id" in box else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.BOX
            )]["id"],
            frames=frames,
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.BOX
            )]["properties"],
            properties=box["properties"] if "properties" in box else [],
            tracking_id=box["tracking_id"] if "tracking_id" in box else 0,
        )


class RotatedBoxCreator(VideoLabelCreator):
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
        raise NotImplementedError

    def from_dict(self, rbox):
        class_name = rbox["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.RBOX
        ) in self.object_classes_map.keys()
        frames = self.change_annotations_to_frames(rbox, ClassType.RBOX)
        assert is_sublist(
            ["cx", "cy", "width", "height", "angle"],
            frames[0]["annotation"]["coord"].keys(),
        )
        return RotatedBox(
            id=rbox["id"] if "id" in rbox else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.RBOX
            )]["id"],
            frames=frames,
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.RBOX
            )]["properties"],
            properties=rbox["properties"] if "properties" in rbox else [],
            tracking_id=rbox["tracking_id"] if "tracking_id" in rbox else 0,
        )


class PolylineCreator(VideoLabelCreator):
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
        raise NotImplementedError

    def from_dict(self, polyline):
        class_name = polyline["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.POLYLINE
        ) in self.object_classes_map.keys()
        frames = self.change_annotations_to_frames(polyline, ClassType.POLYLINE)
            
        coord = frames[0]["annotation"]["coord"]
        assert len(dim(coord["points"])) == 2
        assert dim(coord["points"])[-1] >= 1

        return Polyline(
            id=polyline["id"] if "id" in polyline else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYLINE
            )]["id"],
            frames=frames,
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYLINE
            )]["properties"],
            properties=polyline["properties"]
            if "properties" in polyline
            else [],
            tracking_id=polyline["tracking_id"]
            if "tracking_id" in polyline
            else 0,
        )


class PolygonCreator(VideoLabelCreator):
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
        raise NotImplementedError

    def from_dict(self, polygon):
        class_name = polygon["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.POLYGON
        ) in self.object_classes_map.keys()
        frames = self.change_annotations_to_frames(polygon, ClassType.POLYGON)
        coord = frames[0]["annotation"]["coord"]
        assert len(dim(coord["points"])) == 3
        assert dim(coord["points"])[-1] >= 3

        return Polygon(
            id=polygon["id"] if "id" in polygon else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYGON
            )]["id"],
            frames=frames,
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.POLYGON
            )]["properties"],
            properties=polygon["properties"]
            if "properties" in polygon
            else [],
            tracking_id=polygon["tracking_id"]
            if "tracking_id" in polygon
            else 0,
        )


class KeypointCreator(VideoLabelCreator):
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
        raise NotImplementedError

    def from_dict(self, keypoint):
        class_name = keypoint["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.KEYPOINT
        ) in self.object_classes_map.keys()
        frames = self.change_annotations_to_frames(keypoint, ClassType.KEYPOINT)
        coord = frames[0]["annotation"]["coord"]
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
                ClassType.KEYPOINT
            )]["id"],
            frames=frames,
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.KEYPOINT
            )]["properties"],
            properties=keypoint["properties"]
            if "properties" in keypoint
            else [],
            tracking_id=keypoint["tracking_id"]
            if "tracking_id" in keypoint
            else 0,
        )


class Cuboid2DCreator(VideoLabelCreator):
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
        raise NotImplementedError

    def from_dict(self, cuboid2d):
        class_name = cuboid2d["class_name"]
        assert unique_string_builder(
            class_name,
            ClassType.CUBOID2D
        ) in self.object_classes_map.keys()
        frames = self.change_annotations_to_frames(cuboid2d, ClassType.CUBOID2D)
        coord = frames[0]["annotation"]["coord"]
        assert is_sublist(
            ["near", "far"],
            coord.keys(),
        )

        return Cuboid2D(
            id=cuboid2d["id"] if "id" in cuboid2d else str(uuid4()),
            class_name=class_name,
            class_id=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.CUBOID2D
            )]["id"],
            frames=frames,
            properties_def=self.object_classes_map[unique_string_builder(
                class_name,
                ClassType.CUBOID2D
            )]["properties"],
            properties=cuboid2d["properties"]
            if "properties" in cuboid2d
            else [],
            tracking_id=cuboid2d["tracking_id"]
            if "tracking_id" in cuboid2d
            else 0,
        )


class AutoLabelCreator(VideoLabelCreator):
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
