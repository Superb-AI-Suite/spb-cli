from ..common import is_camel_version
from .categorization import CategorizationDef
from .label_info import LabelInfo
from .label_interface import LabelInterface
from .legacy.label_info import LabelInfo as LegacyLabelInfo
from .object_tracking import ObjectTrackingDef
from .project_info import ProjectInfo
from .property import PropertyDef, PropertyOptionsDef, PropertyOptionsItemDef


def build_label_info(label_interface, result=None):
    if type(label_interface) is dict:
        label_interface = LabelInterface.from_dict(label_interface)
    if is_camel_version(label_interface):
        return LegacyLabelInfo(label_interface, result)
    return LabelInfo(label_interface, result)


__all__ = (
    "LabelInfo",
    "LabelInterface",
    "ObjectTrackingDef",
    "LegacyLabelInfo",
    "build_label_info",
    "ProjectInfo",
    "CategorizationDef",
    "PropertyDef",
    "PropertyOptionsDef",
    "PropertyOptionsItemDef",
)
