from uuid import uuid4

from .. import __version__
from ..common.image_utils import calculate_imageV2_properties_count
from ..common.label import Label
from .image_label_creator import (
    BoxCreator,
    Cuboid2DCreator,
    KeypointCreator,
    PolygonCreator,
    PolylineCreator,
    RotatedBoxCreator,
    AutoLabelCreator,
)
from ..common.utils import unique_string_builder
from ..exceptions import InvalidObjectException


class LabelInfo:
    @classmethod
    def _get_opt_map(cls, options: list) -> dict:
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
            unique_string_builder(
                object_class["name"],
                object_class["annotation_type"]
            ): object_class
            for object_class in label_interface.object_detection.object_classes
        }
        self.keypoint_map = {
            point["id"]: point
            for point in label_interface.object_detection.keypoints
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
        self.result["categories"] = {"properties": []}

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

    # def add_object(self, label_object: Label):
    #     assert isinstance(label_object, Label)
    #     assert unique_string_builder(
    #         label_object.class_name,
    #         label_object.annotation_type
    #     ) in self.object_classes_map.keys()
    #     self.result["objects"].append(label_object.to_dict())

    def add_object(
        self,
        **kwargs,
    ):
        class_name, annotation, properties, id, tracking_id = (
            kwargs["class_name"],
            kwargs["annotation"],
            kwargs.get("properties", None),
            kwargs.get("id", str(uuid4())),
            kwargs.get("tracking_id", None),
        )
        if id is None:
            id = str(uuid4())

        label = AutoLabelCreator(
            self.object_classes_map,
            self.keypoint_map
        ).from_dict(
            {
                "id": id,
                "class_name": class_name,
                "annotation": annotation,
                "properties": properties,
                "tracking_id": tracking_id,
            }
        )
        if label is None:
            raise InvalidObjectException(f"Invalid object : {class_name}")
        self.result["objects"].append(label.to_dict())

    def get_objects(self):
        try:
            simple_objects = [
                {
                    "id": obj["id"],
                    "class_name": obj["class_name"],
                    "annotation": obj["annotation"],
                    "annotation_type": obj["annotation_type"],
                    "properties": LabelInfo._get_properties(
                        self.object_classes_map[unique_string_builder(
                                obj["class_name"],
                                obj["annotation_type"],
                            )][
                            "properties"
                        ],
                        obj["properties"],
                    ),
                }
                for obj in self.result["objects"]
            ]
            return simple_objects
        except Exception as e:
            return []

    def set_categories(self, categorization=None, properties=None):
        if categorization:
            properties = categorization.to_dict()["properties"]
        self.result["categories"] = {
            "properties": LabelInfo._set_properties(
                self.label_interface.categorization.properties,
                properties if properties is not None else [],
            )
        }

    def get_categories(self):
        try:
            simple_categories = {
                "properties": LabelInfo._get_properties(
                    self.label_interface.categorization.properties,
                    self.result["categories"]["properties"],
                ),
            }
            return simple_categories
        except:
            return {"properties": []}

    def build_tags(self):
        classes_count = {}
        classes_name = {}
        for obj in self.result["objects"]:
            classes_count[obj["class_id"]] = (
                classes_count.get(obj["class_id"], 0) + 1
            )
            classes_name[obj["class_id"]] = obj["class_name"]
        class_val = list(classes_name.values())

        categories_id = []
        if (
            "categories" in self.result
            and "properties" in self.result["categories"]
        ):
            for prop in self.result["categories"]["properties"]:
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
            "classes_properties_count": calculate_imageV2_properties_count(
                self.result["objects"]
            ),
            "categories_id": categories_id,
        }

    def build_info(self):
        return {
            "version": __version__,
            "meta": {
                "image_info": {},
                "edit_info": {
                    "objects": [
                        {
                            "id": obj["id"],
                            "color": self.object_classes_map[
                                unique_string_builder(
                                    obj["class_name"],
                                    obj["annotation_type"]
                                )
                            ]["color"],
                            "visible": True,
                            "selected": False,
                        }
                        for obj in self.result["objects"]
                    ]
                },
            },
            "result": self.result,
            "tags": self.build_tags(),
        }
