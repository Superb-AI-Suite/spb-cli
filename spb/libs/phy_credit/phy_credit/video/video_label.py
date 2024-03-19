from ..common.label import Label, ClassType
from ..common.utils import set_properties


class Box(Label):
    def __init__(self, **attributes):
        super().__init__(attributes=attributes)
        self.frames = attributes["frames"]
        self.annotation_type = ClassType.BOX

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": self.annotation_type.value,
            "frames": [
                {
                    "num": frame["num"],
                    "properties": frame["properties"],
                    "annotation": frame["annotation"],
                }
                for frame in self.frames
            ],
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class RotatedBox(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.frames = attributes["frames"]
        self.annotation_type = ClassType.RBOX

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": self.annotation_type.value,
            "frames": [
                {
                    "num": frame["num"],
                    "properties": frame["properties"],
                    "annotation": frame["annotation"],
                }
                for frame in self.frames
            ],
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Polyline(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.frames = attributes["frames"]
        self.annotation_type = ClassType.POLYLINE

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": self.annotation_type.value,
            "frames": [
                {
                    "num": frame["num"],
                    "properties": frame["properties"],
                    "annotation": frame["annotation"],
                }
                for frame in self.frames
            ],
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Polygon(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.frames = attributes["frames"]
        self.annotation_type = ClassType.POLYGON

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": self.annotation_type.value,
            "frames": [
                {
                    "num": frame["num"],
                    "properties": frame["properties"],
                    "annotation": frame["annotation"],
                }
                for frame in self.frames
            ],
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Keypoint(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.frames = attributes["frames"]
        self.annotation_type = ClassType.KEYPOINT

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": self.annotation_type.value,
            "frames": [
                {
                    "num": frame["num"],
                    "properties": frame["properties"],
                    "annotation": frame["annotation"],
                }
                for frame in self.frames
            ],
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Cuboid2D(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.frames = attributes["frames"]
        self.annotation_type = ClassType.CUBOID2D

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": self.annotation_type.value,
            "frames": [
                {
                    "num": frame["num"],
                    "properties": frame["properties"],
                    "annotation": frame["annotation"],
                }
                for frame in self.frames
            ],
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }
