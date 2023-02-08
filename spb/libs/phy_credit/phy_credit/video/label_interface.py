from .. import __version__
from .categorization import CategorizationDef
from .object_tracking import ObjectTrackingDef


class LabelInterface:
    def __init__(
        self,
        type: str,
        data_type: str,
        categorization: CategorizationDef,
        object_tracking: ObjectTrackingDef,
        version: str = __version__,
    ):
        self._version = version
        self.type = type
        self.data_type = data_type
        self.categorization = categorization
        self.object_tracking = object_tracking

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @classmethod
    def get_default(cls):
        return cls(
            type="video-siesta",
            data_type="image sequence",
            categorization=CategorizationDef.get_default(),
            object_tracking=ObjectTrackingDef.get_default(),
        )

    @classmethod
    def from_dict(cls, label_interface_dict: dict):
        return cls(
            type="video-siesta",
            data_type="image sequence",
            categorization=CategorizationDef.from_dict(
                label_interface_dict["categorization"]
            ),
            object_tracking=ObjectTrackingDef.from_dict(
                label_interface_dict["object_tracking"]
            ),
            version=label_interface_dict["version"],
        )

    def set_categorization(self, categorization: CategorizationDef):
        self.categorization = categorization
        if not "image category" in self.object_tracking.annotation_types:
            self.object_tracking.annotation_types.append("image category")

    def set_object_tracking(self, object_tracking: ObjectTrackingDef):
        if "image category" in self.object_tracking.annotation_types:
            object_tracking.annotation_types.append("image category")
        self.object_tracking = object_tracking

    def to_dict(self):
        return {
            "type": self.type,
            "version": self.version,
            "data_type": self.data_type,
            "categorization": self.categorization.to_dict(),
            "object_tracking": self.object_tracking.to_dict(),
        }
