# from phy_credit.common.categorization import CategorizationDef
from ..common import is_camel_version
from .categorization import CategorizationDef
from .label_info import LabelInfo
from .label_interface import LabelInterface
from .legacy.label_info import LabelInfo as LegacyLabelInfo
from .object_detection import ObjectDetectionDef
from .project_info import ProjectInfo
from .property import PropertyDef, PropertyOptionsDef, PropertyOptionsItemDef


def build_label_info(label_interface, result=None):
    if type(label_interface) is dict:
        label_interface = LabelInterface.from_dict(label_interface)
    if is_camel_version(label_interface):
        return LegacyLabelInfo(label_interface, result)
    return LabelInfo(label_interface, result)


# def build_project_info(name: str = None, project_info: dict = None) -> ProjectInfo:
#     if name or project_info:
#         return ProjectInfo(name=name, project_info=project_info)
#     else:
#         return ProjectInfo()


# def build_label_interface(label_interface: dict = None) -> LabelInterface:
#     if label_interface:
#         return LabelInterface(label_interface=label_interface)
#     else:
#         return LabelInterface()


# def build_categorization(categorization: dict = None) -> Categorization:
#     if categorization:
#         return Categorization(categorization=categorization)
#     else:
#         return Categorization()


# def build_category_options(options: list = None) -> CategoryOptions:
#     if options:
#         return CategoryOptions(options=options)
#     else:
#         return CategoryOptions()


# def build_class_property(name: str = None, options: list = None) -> ClassProperty:
#     if name:
#         return ClassProperty(name=name, options=options)
#     else:
#         return ClassProperty()


# def build_object_dection(object: dict = None) -> ObjectDetection:
#     if object:
#         return ObjectDetection(object=object)
#     else:
#         return ObjectDetection()


__all__ = (
    "LabelInfo",
    "LegacyLabelInfo",
    "ObjectDetectionDef",
    "build_label_info",
    "LabelInterface",
    "ProjectInfo",
    "CategorizationDef",
    "PropertyDef",
    "PropertyOptionsDef",
    "PropertyOptionsItemDef",
    # "build_project_info",
    # "build_label_interface",
    # "build_categorization",
    # "build_category_options",
    # "build_class_property",
    # "build_object_dection",
)
