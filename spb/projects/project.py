import uuid

from spb.core import Model
from spb.core.models.attrs import AttributeModel
from spb.core.models.types import (
    ID,
    Boolean,
    Int,
    JsonList,
    JsonObject,
    String,
    PlainObjectList,
)


class PointcloudData(Model):
    id = ID(property_name="id", default_value=uuid.uuid4())
    key = String(property_name="dataKey")
    group = String(property_name="dataset")
    info = JsonObject(property_name="info")
    last_updated_by = String(property_name='lastUpdatedBy')
    last_updated_at = String(property_name='lastUpdatedAt')
    created_at = String(property_name="createAt")
    create_by = String(property_name="createdBy")

    read_url = JsonObject(property_name="readUrl")
    read_custom_url = JsonObject(property_name="readCustomUrl")
    upload_url = JsonObject(property_name="uploadUrl")

    def __repr__(self):
        return f"Suite Pointcloud Data : <{self.id}> {self.key}"



class Project(Model):
    id = ID(property_name="id", default_value=uuid.uuid4())
    name = String(property_name="name")
    label_interface = JsonObject(property_name="labelInterface")
    workapp = String(property_name="workapp")
    settings = JsonObject(property_name="settings", default={})
    label_count = Int(property_name="labelCount")
    is_public = Boolean(property_name="isPublic")
    created_at = String(property_name="createdAt")
    created_by = String(property_name="createdBy")
    last_updated_at = String(property_name="lastUpdatedAt")
    last_updated_by = String(property_name="lastUpdatedBy")
    progress = Int(property_name="progress")
    submitted_label_count = Int(property_name="submittedLabelCount", default=0)
    in_progress_label_count = Int(
        property_name="inProgressLabelCount", default=0
    )
    skipped_label_count = Int(property_name="skippedLabelCount", default=0)
    stats = JsonList(property_name="stats", default=[])

    def __repr__(self):
        return f"Suite Project with name: <{self.name}>"

    def to_json(self):
        project = {
            "id": str(self.id),
            "name": self.name,
            "label_interface": self.label_interface,
            "workapp": self.workapp,
            "settings": self.settings,
            "label_count": self.label_count,
            "is_public": self.is_public,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "last_updated_at": self.last_updated_at,
            "last_updated_by": self.last_updated_by,
            "progress": self.progress,
            "submitted_label_count": self.submitted_label_count,
            "in_progress_label_count": self.in_progress_label_count,
            "skipped_label_count": self.skipped_label_count,
            "stats": self.stats,
        }
        return project

    def get_project_type(self):
        return self.workapp.split("-")[0]

    def get_stats(self):
        _stats = {
            "in_progress": {
                "rejected": self.stats[0]["info"]["rejected"],
                "not_submitted": self.stats[0]["info"]["not_submitted"],
            },
            "submitted": {
                "approved": self.stats[1]["info"]["approved"],
                "pending_review": self.stats[1]["info"]["pending_review"],
            },
            "skipped": {
                "approved": self.stats[2]["info"]["approved"],
                "pending_review": self.stats[1]["info"]["pending_review"],
            },
        }
        return _stats


class Tag(Model):
    id = ID(property_name="id", default_value=uuid.uuid4())
    name = String(property_name="name")
