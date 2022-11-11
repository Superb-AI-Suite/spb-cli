import uuid


from spb.core import Model
from spb.core.models.types import (
    JsonObject,
    String,
    ID,
    Int,
)

class Task(Model):
    id = ID(property_name='id', default_value=uuid.uuid4())
    project = JsonObject(property_name='project', default_value={})
    progress = Int(property_name='progress')
    status = String(property_name='status')
    type = String(property_name='type')
    params = JsonObject(property_name='params')
    total_count = Int(property_name='totalCount')
    result = JsonObject(property_name='result', default_value={})
    created_at = String(property_name='createdAt')
    created_by = String(property_name='createdBy')
    updated_at = String(property_name='updatedAt')
    planning_start_at = String(property_name='planningStartAt')
    planning_end_at = String(property_name='planningEndAt')
    applying_start_at = String(property_name='applyingStartAt')
    applying_end_at = String(property_name='applyingEndAt')
    finished_at = String(property_name='finishedAt')
    failed_at = String(property_name='failedAt')
    canceled_at = String(property_name='canceledAt')
    canceled_by = String(property_name='canceledBy')
    final_progress = Int(property_name='finalProgress')
