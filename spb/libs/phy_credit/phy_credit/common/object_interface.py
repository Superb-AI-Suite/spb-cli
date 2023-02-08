import random
from uuid import uuid4


class ObjectInterfaceDef:
    def __init__(
        self,
        keypoints: list = [],
        object_groups: list = [],
        object_classes: list = [],
        annotation_types: list = [],
    ):
        self.keypoints = keypoints
        self.object_groups = object_groups
        self.object_classes = object_classes
        self.annotation_types = annotation_types

    @classmethod
    def get_default(cls):
        return cls(
            keypoints=[],
            object_groups=[],
            object_classes=[],
            annotation_types=[],
        )

    @classmethod
    def from_dict(cls, object_detection_dict: dict):
        return cls(
            keypoints=object_detection_dict["keypoints"],
            object_groups=object_detection_dict["object_groups"],
            object_classes=object_detection_dict["object_classes"],
            annotation_types=object_detection_dict["annotation_types"],
        )

    def add_object_group(self, name: str, groups: list, id: str = None):
        id = str(uuid4()) if id is None else id
        new_group = {"id": id, "name": name, "object_class_ids": []}
        for object in self.object_classes:
            if object["name"] in groups:
                new_group["object_class_ids"].append(object["id"])
                groups.remove(object["name"])
        if len(groups) > 0:
            return print(f"[ERROR] {groups} does not exist")
        self.object_groups.append(new_group)

    def add_object_class(
        self,
        name: str,
        annotation_type: str,
        color: str = None,
        properties: list = [],
        id: str = None,
    ):
        for object in self.object_classes:
            if object["name"] == name:
                return print(f"[ERROR] {name} already exists")
        id = str(uuid4()) if id is None else id

        def r():
            return random.randint(0, 255)

        self.object_classes.append(
            {
                "id": id,
                "name": name,
                "color": color if color else "#%02X%02X%02X" % (r(), r(), r()),
                "properties": properties,
                "constraints": {},
                "ai_class_map": [],
                "annotation_type": annotation_type,
            }
        )
        if not annotation_type in self.annotation_types:
            self.annotation_types.append(annotation_type)

    def add_box(
        self,
        name: str,
        id: str = None,
        color: str = None,
        properties: list = [],
    ):
        self.add_object_class(name, "box", color, properties, id)

    def add_rbox(
        self,
        name: str,
        id: str = None,
        color: str = None,
        properties: list = [],
    ):
        self.add_object_class(name, "rbox", color, properties, id)

    def add_polyline(
        self,
        name: str,
        id: str = None,
        color: str = None,
        properties: list = [],
    ):
        self.add_object_class(name, "polyline", color, properties, id)

    def add_polygon(
        self,
        name: str,
        id: str = None,
        color: str = None,
        properties: list = [],
    ):
        self.add_object_class(name, "polygon", color, properties, id)

    def add_2dcuboid(
        self,
        name: str,
        id: str = None,
        color: str = None,
        properties: list = [],
    ):
        self.add_object_class(name, "cuboid2d", color, properties, id)

    def add_keypoint(
        self,
        name: str,
        keypoint_id: str,
        keypoint_template: dict = None,
        color: str = None,
        properties: list = [],
        id: str = None,
    ):
        for object in self.object_classes:
            if object["name"] == name:
                return print(f"[ERROR] {name} already exists")
        template_exists = False
        if keypoint_template == None:
            current_keypoints = self.keypoints
            if len(current_keypoints) == 0:
                return print(
                    f"[ERROR] {keypoint_id} does not exist please add a keypoint template"
                )
            else:
                for template in current_keypoints:
                    if template["id"] == keypoint_id:
                        template_exists = True
                if not template_exists:
                    return print(
                        f"[ERROR] {keypoint_id} does not exist please add a keypoint template"
                    )

        id = str(uuid4()) if id is None else id

        def r():
            return random.randint(0, 255)

        self.object_classes.append(
            {
                "id": id,
                "name": name,
                "color": color if color else "#%02X%02X%02X" % (r(), r(), r()),
                "properties": properties,
                "constraints": {},
                "ai_class_map": [],
                "annotation_type": "keypoint",
                "keypoint_interface_id": keypoint_id,
            }
        )
        if not template_exists:
            keypoint_template["id"] = keypoint_id
            self.keypoints.append(keypoint_template)
        if not "keypoint" in self.annotation_types:
            self.annotation_types.append("keypoint")

    def add_object_property(self, name: str, property: dict):
        for object in self.object_classes:
            if object["name"] == name:
                break
        object["properties"].append(property)

    def remove_objects_by_class_id(self, id: str):
        annotation_type_list = []
        keypoint_id_list = []
        for object in self.object_classes:
            if object["id"] == id:
                annotation_type = object["annotation_type"]
                self.object_classes.remove(object)
                if annotation_type == "keypoint":
                    keypoint_id = object["keypoint_interface_id"]
            else:
                annotation_type = object["annotation_type"]
                annotation_type_list.append(annotation_type)
                if annotation_type == "keypoint":
                    keypoint_id_list.append(object["keypoint_interface_id"])

        if annotation_type == "keypoint":
            for keypoint in self.keypoints:
                if not keypoint_id in keypoint_id_list:
                    self.keypoints.remove(keypoint)
                    break

        if not annotation_type in annotation_type_list:
            self.result["annotation_types"].remove(annotation_type)

    def remove_objects_by_class_name(self, name: str):
        for object in self.object_classes:
            if object["name"] == name:
                self.remove_objects_by_class_id(id=object["id"])
                return

    def to_dict(self):
        return {
            "keypoints": self.keypoints,
            "object_groups": self.object_groups,
            "object_classes": self.object_classes,
            "annotation_types": list(self.annotation_types),
        }
