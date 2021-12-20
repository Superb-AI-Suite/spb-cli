import uuid
import json


from spb.core import Model
from spb.core.models.attrs import AttributeModel
from spb.core.models.types import (
    JsonObject,
    String,
    ID,
    Int,
    JsonList,
)


class Project(Model):
    id = ID(property_name='id', default_value=uuid.uuid4())
    name = String(property_name='name')

    label_interface = JsonObject(property_name='labelInterface')
    workapp = String(property_name='workapp')

    label_count = Int(property_name='labelCount')
    progress = Int(property_name='progress')
    submitted_label_count = Int(property_name='submittedLabelCount', default = 0)
    in_progress_label_count = Int(property_name='inProgressLabelCount', default = 0)
    skipped_label_count = Int(property_name='skippedLabelCount', default = 0)
    stats = JsonList(property_name='stats', default = [])