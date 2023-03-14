from uuid import uuid4

from .. import __version__
from ..common.video_utils import (
    calculate_annotated_frame_count,
    calculate_video_properties_count,
)
from .video_label_creator import (
    BoxCreator,
    Cuboid2DCreator,
    KeypointCreator,
    PolygonCreator,
    PolylineCreator,
    RotatedBoxCreator,
)


class LabelInfo:
    @classmethod
    def _get_opt_map(cls, options):
        res = {}
        for opt in options:
            if "children" in opt:
                res.update(LabelInfo._get_opt_map(opt["children"]))
            else:
                res[opt["name"]] = opt
        return res

    @classmethod
    def _set_properties(cls, properties_def, properties):
        prop_def_map = {
            prop_def["name"]: prop_def for prop_def in properties_def
        }
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop["name"]]
            if prop_def["type"] in ["radio", "dropdown", "checkbox"]:
                opt_map = LabelInfo._get_opt_map(prop_def["options"])
                if prop_def["type"] == "checkbox":
                    converted_properties.append(
                        {
                            "type": prop_def["type"],
                            "property_id": prop_def["id"],
                            "property_name": prop_def["name"],
                            "option_ids": [
                                opt_map[val]["id"] for val in prop["value"]
                            ],
                            "option_names": [
                                opt_map[val]["name"] for val in prop["value"]
                            ],
                        }
                    )
                else:
                    converted_properties.append(
                        {
                            "type": prop_def["type"],
                            "property_id": prop_def["id"],
                            "property_name": prop_def["name"],
                            "option_id": opt_map[prop["value"]]["id"],
                            "option_name": opt_map[prop["value"]]["name"],
                        }
                    )
            elif prop_def["type"] == "free response":
                converted_properties.append(
                    {
                        "type": prop_def["type"],
                        "property_id": prop_def["id"],
                        "property_name": prop_def["name"],
                        "value": prop["value"],
                    }
                )
        return converted_properties

    @classmethod
    def _get_properties(cls, properties_def, properties):
        prop_def_map = {
            prop_def["name"]: prop_def for prop_def in properties_def
        }
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop["property_name"]]
            if prop_def["type"] in ["radio", "dropdown"]:
                converted_properties.append(
                    {
                        "name": prop["property_name"],
                        "value": prop["option_name"],
                    }
                )
            elif prop_def["type"] == "checkbox":
                converted_properties.append(
                    {
                        "name": prop["property_name"],
                        "value": prop["option_names"],
                    }
                )
            elif prop_def["type"] == "free response":
                converted_properties.append(
                    {
                        "name": prop["property_name"],
                        "value": prop["value"],
                    }
                )
        return converted_properties

    def __init__(self, label_interface, result=None):
        self.label_interface = label_interface
        self.object_classes_map = {
            object_class["name"]: object_class
            for object_class in label_interface.object_tracking.object_classes
        }
        self.keypoint_map = {
            point["id"]: point
            for point in label_interface.object_tracking.keypoints
        }
        if result is None:
            self.result = {}
            self.init_objects()
            self.init_categories()
        else:
            self.result = result

    def init_objects(self):
        self.result["objects"] = []

    def init_categories(self):
        self.result["categories"] = {"frames": [], "properties": []}

    def get_box_creator(self):
        return BoxCreator(self.object_classes_map)

    def get_rotated_box_creator(self):
        return RotatedBoxCreator(self.object_classes_map)

    def get_polyline_creator(self):
        return PolylineCreator(self.object_classes_map)

    def get_polygon_creator(self):
        return PolygonCreator(self.object_classes_map)

    def get_keypoint_creator(self):
        return KeypointCreator(self.object_classes_map, self.keypoint_map)

    def get_2D_cubid_creator(self):
        return Cuboid2DCreator(self.object_classes_map)

    def add_object(
        self, tracking_id, class_name, annotations, properties=None, id=None
    ):
        id = str(uuid4()) if id is None else id

        self.result["objects"].append(
            {
                "id": id,
                "tracking_id": tracking_id,
                "class_id": self.object_classes_map[class_name]["id"],
                "class_name": class_name,
                "annotation_type": self.object_classes_map[class_name][
                    "annotation_type"
                ],
                "frames": [
                    {
                        "num": anno["frame_num"],
                        "annotation": {
                            "multiple": anno.get("multiple", False),
                            "coord": anno["coord"],
                            "meta": anno.get("meta", {}),
                        },
                        "properties": LabelInfo._set_properties(
                            self.object_classes_map[class_name]["properties"],
                            anno.get("properties", []),
                        ),
                    }
                    for anno in annotations
                ],
                "properties": LabelInfo._set_properties(
                    self.object_classes_map[class_name]["properties"],
                    properties if properties is not None else [],
                ),
            }
        )

    # def add_object(self, label_object):
    #     self.result["objects"].append(label_object.to_dict())

    def get_objects(self):
        ocm = self.object_classes_map
        try:
            simple_objects = [
                {
                    "id": obj["id"],
                    "tracking_id": obj["tracking_id"],
                    "class_name": obj["class_name"],
                    "annotations": [
                        {
                            "frame_num": frame["num"],
                            "multiple": frame["annotation"].get(
                                "multiple", False
                            ),
                            "coord": frame["annotation"]["coord"],
                            "properties": LabelInfo._get_properties(
                                ocm[obj["class_name"]]["properties"],
                                frame["properties"],
                            ),
                        }
                        for frame in obj["frames"]
                    ],
                    "properties": LabelInfo._get_properties(
                        ocm[obj["class_name"]]["properties"],
                        obj["properties"],
                    ),
                }
                for obj in self.result["objects"]
            ]
            return simple_objects
        except Exception as e:
            return []

    # TODO: set by categorization need to be added
    def set_categories(self, frames=None, properties=None):
        self.result["categories"] = {
            "frames": [
                {
                    "num": frame["num"],
                    "properties": LabelInfo._set_properties(
                        self.label_interface.categorization.properties,
                        frame["properties"],
                    ),
                }
                for frame in (frames if frames is not None else [])
            ],
            "properties": LabelInfo._set_properties(
                self.label_interface.categorization.properties,
                properties if properties is not None else [],
            ),
        }

    def get_categories(self):
        try:
            simple_categories = {
                "frames": [
                    {
                        "num": frame["num"],
                        "properties": LabelInfo._get_properties(
                            self.label_interface.categorization.properties,
                            frame["properties"],
                        ),
                    }
                    for frame in self.result["categories"]["frames"]
                ],
                "properties": LabelInfo._get_properties(
                    self.label_interface.categorization.properties,
                    self.result["categories"]["properties"],
                ),
            }
            return simple_categories
        except:
            return {
                "frames": [],
                "properties": [],
            }

    def build_tags(self):
        classes_count = {}
        anno_count = {}
        classes_name = {}
        for obj in self.result["objects"]:
            cid = obj["class_id"]
            classes_count[cid] = classes_count.get(cid, 0) + 1
            anno_count[cid] = anno_count.get(cid, 0) + len(obj["frames"])
            classes_name[cid] = obj["class_name"]
        class_val = list(classes_name.values())

        categories_id = []
        if (
            "categories" in self.result
            and "properties" in self.result["categories"]
        ):
            properties_list = [self.result["categories"]["properties"]] + [
                frame["properties"]
                for frame in self.result["categories"]["frames"]
            ]
            for properties in properties_list:
                for prop in properties:
                    if "option_id" in prop:
                        categories_id.append(prop["option_id"])
                    elif "option_ids" in prop:
                        for o_id in prop["option_ids"]:
                            categories_id.append(o_id)
            class_val.extend(categories_id)

        return {
            "classes_id": list(classes_count.keys()),
            "class": class_val,
            "classes_count": [
                {
                    "id": k,
                    "name": classes_name[k],
                    "count": v,
                }
                for k, v in classes_count.items()
            ],
            "classes_properties_count": calculate_video_properties_count(
                self.result["objects"]
            ),
            "classes_annotation_count": [
                {
                    "id": k,
                    "name": classes_name[k],
                    "count": v,
                }
                for k, v in anno_count.items()
            ],
            "categories_id": categories_id,
            "annotated_frame_count": calculate_annotated_frame_count(
                self.result["objects"]
            ),
        }

    def build_info(self):
        ocm = self.object_classes_map
        return {
            "version": __version__,
            "meta": {
                "image_info": {},
                "edit_info": {
                    "objects": [
                        {
                            "id": obj["id"],
                            "color": ocm[obj["class_name"]]["color"],
                            "visible": True,
                            "selected": False,
                            "tracking_id": obj["tracking_id"],
                        }
                        for obj in self.result["objects"]
                    ]
                },
            },
            "result": self.result,
            "tags": self.build_tags(),
        }
