import uuid

from spb.core import Model
from spb.core.models.types import JsonObject, String, ID, Int


class Export(Model):
    id = ID(property_name = 'id', default_value = uuid.uuid4())
    project_id = ID(property_name='projectId', )
    name = String(property_name='name')

    meta = JsonObject(property_name = 'meta', default_value = {})
    reason = String(property_name = 'reason')
    download_url = String(property_name = 'downloadUrl')
    processing_updated_at = String(property_name='processingUpdatedAt')
    processing_progress = String(property_name='processingProgress')
    processing_end_at = String(property_name='processingEndAt')
    processing_start_at = String(property_name='processingStartAt')
    created_by = String(property_name='createdBy')
    created_at = String(property_name='createdAt')
    file_size = Int(property_name='fileSize')
    download_label_count = Int(property_name='downloadLabelCount')
    label_count = Int(property_name='labelCount')
    taken_time = Int(property_name='takenTime')
    filter = String(property_name='filter')
    seq_no = Int(property_name='seqNo')
    filter_query = JsonObject(property_name='filterQuery')
    state = String(property_name='state')
