import logging
import uuid
from typing import Optional

from spb.core.manager import BaseManager

from .export import Export
from .query import Query
from .session import Session

logger = logging.getLogger()


class ExportManager(BaseManager):
    def __init__(self, team_name=None, access_key=None):
        self.session = Session(team_name=team_name, access_key=access_key)
        self.query = Query()

    def get_exports(self, project_id: uuid.UUID, page: int = 1, page_size: int = 10):
        self.query.query_id = "exports"
        export = Export(project_id=project_id)
        query_attrs = export.get_attributes_map(include=["project_id"])
        self.query.attrs.update(query_attrs)
        self.query.page = page
        self.query.page_size = page_size
        self.query.response_attrs.extend(
            export.get_property_names(exclude=["project_id"])
        )
        self.query.required_attrs.extend(
            export.get_property_names(include=["project_id"])
        )
        query, values = self.query.build_query()
        response = self.session.execute(query, values)
        _, histories = self.session.get_count_and_data_from_response(response)
        return histories

    def get_export(
        self,
        project_id: uuid.UUID,
        id: Optional[uuid.UUID] = None,
        name: Optional[str] = None,
    ):
        self.query.query_id = "export"
        if id:
            export = Export(project_id=project_id, id=id)
            query_attrs = export.get_attributes_map(include=["project_id", "id"])
            self.query.required_attrs.extend(
                export.get_property_names(include=["project_id", "id"])
            )
        elif name:
            export = Export(project_id=project_id, name=name)
            query_attrs = export.get_attributes_map(include=["project_id", "name"])
            self.query.required_attrs.extend(
                export.get_property_names(include=["project_id", "name"])
            )
        self.query.attrs.update(query_attrs)
        self.query.response_attrs.extend(
            export.get_property_names(exclude=["project_id"])
        )
        query, values = self.query.build_query()
        response = self.session.execute(query, values)
        return self.session.get_data_from_response(response)

    # def get_export_info(
    #     self,
    #     project_id: uuid.UUID,
    #     id: Optional[uuid.UUID] = None,
    #     name: Optional[str] = None,
    # ):
    #     export = self.get_export(project_id=project_id, id=id, name=name)
    #     (count, export_info) = parse_zip_file(get_url_data(export.download_url))
    #     project_info, meta_infos, label_info = self.read_export_info(export_info)
    #     return {"project_info": project_info, "meta_infos": meta_infos, "label_info": label_info}

    # def get_masks(
    #     self,
    #     project_id: uuid.UUID,
    #     id: Optional[uuid.UUID] = None,
    #     name: Optional[str] = None,
    # ):
        
    #     export_info = self.get_export_info(project_id=project_id, id=id, name=name)        
    #     project_info = export_info["project_info"]
    #     meta_infos = export_info["meta_infos"]
    #     label_info = export_info["label_info"]

    #     masks = list()
    #     for meta_info in meta_infos:
    #         mask = mask_from_label(
    #             label_interface=project_info,
    #             meta_info=meta_info,
    #             label_info=label_info[meta_info["label_path"][0]],
    #         )
    #         masks.append(mask)
    #     return masks

    # def read_export_info(self, export_info: dict):
    #     file_names = export_info.keys()
    #     meta_infos = list()
    #     label_info = dict()
    #     project_info = export_info["project.json"]
    #     meta_names = [f for f in file_names if f.startswith("meta/") and f.endswith(".json")]
    #     for meta_name in meta_names:
    #         meta_info = export_info[meta_name]
    #         label_path = meta_info["label_path"][0]
    #         label_info[label_path] = export_info[label_path]
    #         meta_infos.append(meta_info)
    #     return project_info, meta_infos, label_info
