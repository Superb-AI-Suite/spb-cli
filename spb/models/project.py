import json

from spb.orm.type import Type
from spb.orm import Model
from spb.orm import AttributeModel
from spb.orm.type import String, ID, Number, Object

class Class(AttributeModel):
    def __init__(self, *args, **kwargs ):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.annotationType = kwargs['annotationType'] if 'annotationType' in kwargs else None
        self.properties = kwargs['properties'] if 'properties' in kwargs else None


class Configure(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.dataType = kwargs['dataType'] if 'dataType' in kwargs else None
        self.annotationTypes = kwargs['annotationTypes'] if 'annotationTypes' in kwargs else None
        self.classList = [Class(**item) for item in kwargs['classList']] if 'classList' in kwargs else None


class KeypointInterface(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.points = kwargs['points'] if 'points' in kwargs else None


class ObjectClass(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.color = kwargs['color'] if 'color' in kwargs else None
        self.annotationType = kwargs['annotationType'] if 'annotationType' in kwargs else None
        # optional value : annotation_type = keypoint
        self.keypointName = kwargs['keypointName'] if 'keypointName' in kwargs else None


class ObjectGroups(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.objectClasses = kwargs['objectClasses'] if 'objectClasses' in kwargs else None


class ObjectDetection(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.annotationTypes = kwargs['annotationTypes'] if 'annotationTypes' in kwargs else []
        self.objectClasses = [ObjectClass(
            **item) for item in kwargs['objectClasses']] if 'objectClasses' in kwargs else []
        self.objectGroups = [ObjectGroups(
            **item) for item in kwargs['objectGroups']] if 'objectGroups' in kwargs else []
        self.keypointInterfaces = [KeypointInterface(
            **item) for item in kwargs['keypointInterfaces']] if 'keypointInterfaces' in kwargs else []


class ImageCategorization(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.type = kwargs['type'] if 'type' in kwargs else None
        self.options = kwargs['options'] if 'options' in kwargs else []


class ProjectSummary(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.dataType = kwargs['dataType'] if 'dataType' in kwargs else None
        self.objectDetection = ObjectDetection(
            **kwargs['objectDetection']) if 'objectDetection' in kwargs else ObjectDetection()
        self.imageCategorization = [ImageCategorization(
            **item) for item in kwargs['imageCategorization']] if 'imageCategorization' in kwargs else []


class Project(Model):
    MODEL_UUID = '1da666a0-958b-11ea-bb37-0242ac130002'
    RESOURCE_NAME = 'projects'

    id = ID(property_name='id', immutable=True, filterable=True)
    name = String(property_name='name', filterable=True)
    label_count = Number(property_name='labelCount')
    progress = Number(property_name='progress')
    # configure = Type(property_name='configure', express=Configure)
    summary = Object(property_name='configure', express=ProjectSummary)
