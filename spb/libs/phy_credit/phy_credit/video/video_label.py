from ..common.label import Label
from ..common.utils import set_properties


class Box(Label):
    def __init__(self, **attributes):
        super().__init__(attributes=attributes)
        self.frames = attributes["frames"]

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotaion_type": "box",
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

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "rbox",
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

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "rbox",
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

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "rbox",
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

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "rbox",
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

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "rbox",
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
