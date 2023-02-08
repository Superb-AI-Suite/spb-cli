from abc import ABC


class Label(ABC):
    def __init__(self, attributes):
        self.id = attributes["id"]
        self.class_name = attributes["class_name"]
        self.class_id = attributes["class_id"]
        self.properties_def = attributes["properties_def"]
        self.properties = attributes["properties"]
        self.tracking_id = attributes["tracking_id"]

    def to_dict(self):
        pass
