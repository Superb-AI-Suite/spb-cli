from abc import ABC, abstractmethod


class LabelCreator(ABC):
    def __init__(self, object_classes_map):
        self.object_classes_map = object_classes_map

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def from_dict(self):
        pass

    def _get_meta(self, class_name):
        return {
            "z_index": 1,
            "visible": True,
            "alpha": 1,
            "color": self.object_classes_map[class_name]["color"],
        }
