import uuid

from spb.core import Model
from spb.core.models.types import ID, Bytes, ModelObject, String
from spb.projects.project import Project


class Asset(Model):
    id = ID(property_name="id", default_value=uuid.uuid4())
    cursor = Bytes(property_name="cursor")
    project_id = ID(property_name="projectId")

    data_key = String(property_name="dataKey")
    dataset = String(property_name="dataset")
    projects = ModelObject(model=Project(), model_property_name="projects")
