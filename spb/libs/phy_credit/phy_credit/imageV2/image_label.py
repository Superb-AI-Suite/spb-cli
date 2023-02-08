from ..common.label import Label
from ..common.utils import set_properties


class Box(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.coord = attributes["coord"]
        self.meta = attributes["meta"]

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "box",
            "annotation": {
                "coord": self.coord,
                "meta": self.meta,
            },
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class RotatedBox(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.coord = attributes["coord"]
        self.meta = attributes["meta"]

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "rbox",
            "annotation": {
                "coord": self.coord,
                "meta": self.meta,
            },
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Polyline(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.coord = attributes["coord"]
        self.meta = attributes["meta"]
        self.multiple = attributes["multiple"]

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "polyline",
            "annotation": {
                "multiple": self.multiple,
                "coord": self.coord,
                "meta": self.meta,
            },
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Polygon(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.coord = attributes["coord"]
        self.meta = attributes["meta"]
        self.multiple = attributes["multiple"]

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "polygon",
            "annotation": {
                "multiple": self.multiple,
                "coord": self.coord,
                "meta": self.meta,
            },
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Keypoint(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.coord = attributes["coord"]
        self.meta = attributes["meta"]

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "keypoint",
            "annotation": {
                "coord": self.coord,
                "meta": self.meta,
            },
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }


class Cuboid2D(Label):
    def __init__(self, **attributes):
        super().__init__(
            attributes=attributes,
        )
        self.coord = attributes["coord"]
        self.meta = attributes["meta"]

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "class_id": self.class_id,
            "annotation_type": "cuboid2d",
            "annotation": {
                "coord": self.coord,
                "meta": self.meta,
            },
            "properties": set_properties(self.properties_def, self.properties),
            "tracking_id": self.tracking_id,
        }
