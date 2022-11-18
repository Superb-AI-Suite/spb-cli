import uuid

from spb.core import Model
from spb.core.models.types import ID, Int, JsonList, JsonObject, String


class Project(Model):
    id = ID(property_name="id", default_value=uuid.uuid4())
    name = String(property_name="name")
    label_interface = JsonObject(property_name="labelInterface")
    workapp = String(property_name="workapp")
    label_count = Int(property_name="labelCount")
    progress = Int(property_name="progress")
    submitted_label_count = Int(property_name="submittedLabelCount", default=0)
    in_progress_label_count = Int(property_name="inProgressLabelCount", default=0)
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
            "label_count": self.label_count,
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
