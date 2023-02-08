from .. import __version__
from .categorization import CategorizationDef
from .object_detection import ObjectDetectionDef


class LabelInterface:
    def __init__(
        self,
        type: str,
        data_type: str,
        categorization: CategorizationDef,
        object_detection: ObjectDetectionDef,
        version: str = __version__,
    ):
        self._version = version
        self.type = type
        self.data_type = data_type
        self.categorization = categorization
        self.object_detection = object_detection

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @classmethod
    def get_default(cls):
        return cls(
            type="image-siesta",
            data_type="image",
            categorization=CategorizationDef.get_default(),
            object_detection=ObjectDetectionDef.get_default(),
        )

    @classmethod
    def from_dict(cls, label_interface_dict: dict):
        return cls(
            type="image-siesta",
            data_type="image",
            categorization=CategorizationDef.from_dict(
                label_interface_dict["categorization"]
            ),
            object_detection=ObjectDetectionDef.from_dict(
                label_interface_dict["object_detection"]
            ),
            version=label_interface_dict["version"],
        )

    def set_categorization(self, categorization: CategorizationDef):
        self.categorization = categorization
        if not "image category" in self.object_detection.annotation_types:
            self.object_detection.annotation_types.append("image category")

    def set_object_detection(self, object_detection: ObjectDetectionDef):
        if "image category" in self.object_detection.annotation_types:
            object_detection.annotation_types.append("image category")
        self.object_detection = object_detection

    def to_dict(self):
        return {
            "type": self.type,
            "version": self.version,
            "data_type": self.data_type,
            "categorization": self.categorization.to_dict(),
            "object_detection": self.object_detection.to_dict(),
        }
