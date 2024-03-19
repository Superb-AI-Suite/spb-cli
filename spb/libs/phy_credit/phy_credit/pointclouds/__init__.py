from ..video.categorization import CategorizationDef
# from .label_info import LabelInfo
from .label_interface import LabelInterface
from .object_tracking import ObjectTrackingDef
from .project_info import ProjectInfo
from ..video.property import PropertyDef, PropertyOptionsDef, PropertyOptionsItemDef


# def build_label_info(label_interface, result=None):
#     if type(label_interface) is dict:
#         label_interface = LabelInterface.from_dict(label_interface)
#     return LabelInfo(label_interface, result)


__all__ = (
    # "LabelInfo",
    "LabelInterface",
    "ObjectTrackingDef",
    # "build_label_info",
    "ProjectInfo",
    "CategorizationDef",
    "PropertyDef",
    "PropertyOptionsDef",
    "PropertyOptionsItemDef",
)
