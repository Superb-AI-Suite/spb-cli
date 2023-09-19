import uuid
import json
import os
from typing import List, Optional

from spb.core.manager import BaseManager
from spb.exceptions import PreConditionException, ParameterException, APIFormatException, APIUnknownException
from spb.libs.phy_credit.phy_credit.imageV2.project_info import ProjectInfo
from spb.utils.utils import requests_retry_session

from .project import Project, PointcloudData, Tag
from .query import Query
from .session import Session


class ProjectManager(BaseManager):
    PROJECT_LIST_QUERY_ID = "projects"
    PROJECT_QUERY_ID = "project"

    def __init__(self, team_name=None, access_key=None):
        self.session = Session(team_name=team_name, access_key=access_key)
        self.query = Query()

    def get_tags(
        self,
        project_id: uuid.UUID
    ) -> (int, List[Tag]):
        QUERY_ID = "tags"
        self.query.query_id = QUERY_ID
        tag = Tag()
        self.query.response_attrs.extend(tag.get_property_names())
        query, values = self.query.build_tags_query(project_id)
        response = self.session.execute(query, values)
        return self.session.extract_tags(
            response=response,
            query_id=QUERY_ID
        )

    def create_project(
        self,
        name: str,
        label_interface: dict,
        description: str = "",
        is_public: bool = False,
        allow_advanced_qa: bool = False,
    ) -> Optional[Project]:
        query_id = "createProject"
        self.query.query_id = query_id
        project_info = {
            "name": name,
            "description": description,
            "label_interface": label_interface,
            "is_public": is_public,
            "settings": {
                "allow_advanced_qa": allow_advanced_qa,
            },
        }
        if "workapp" not in project_info:
            project_info["workapp"] = label_interface["type"]

        project = Project()
        response_attrs = "\n".join(project.get_property_names())
        query = f"mutation ($projectInfo:JSONObject!) {{{query_id}(projectInfo: $projectInfo) {{{response_attrs}}}}}"
        values = {"projectInfo": project_info}
        response = self.session.execute(query, values)
        return self.session.get_result_from_response_project(
            response, query_id
        )

    def update_project(
        self,
        id: uuid.UUID,
        new_name: str = None,
        label_interface: dict = None,
        description: str = None,
        is_public: bool = None,
        allow_advanced_qa: bool = None,
    ):
        existing_project = self.get_project_by_id(id=id)

        query_id = "updateProject"
        self.query.query_id = query_id
        project_info = dict()
        if new_name is not None:
            project_info.update({"name": new_name})
        if description is not None:
            project_info.update({"description": description})
        if label_interface is not None:
            project_info.update({"label_interface": label_interface})
            if (
                existing_project.label_interface["type"]
                != label_interface["type"]
            ):
                raise PreConditionException(
                    "[ERROR] Workapp type cannot be changed"
                )
        if is_public is not None:
            project_info.update({"is_public": is_public})
        if allow_advanced_qa is not None:
            project_info.update(
                {
                    "settings": {
                        "allow_advanced_qa": allow_advanced_qa,
                    }
                }
            )

        project = Project(id=id)
        id = project.to_json()["id"]
        response_attr = "\n".join(project.get_property_names())
        query = f"mutation ($id: String!, $projectInfo: JSONObject!) {{{query_id}(id: $id, projectInfo: $projectInfo) {{{response_attr}}}}}"
        values = {"id": id, "projectInfo": project_info}
        response = self.session.execute(query, values)
        return self.session.get_result_from_response_project(
            response, query_id
        )

    def get_project_list(
        self,
        page: int = 1,
        page_size: int = 10,
        name_icontains: str = None,
        data_type: str = None,
        annotation_type: List[str] = None,
    ):
        self.query.query_id = self.PROJECT_LIST_QUERY_ID

        project = Project()

        self.query.name_icontains = name_icontains
        self.query.data_type = data_type
        self.query.annotation_type = annotation_type
        self.query.page = page
        self.query.page_size = page_size

        self.query.response_attrs.extend(project.get_property_names())

        query, _ = self.query.build_query()

        response = self.session.execute(query, None)
        return self.session.extract_project_list(
            response, self.PROJECT_LIST_QUERY_ID
        )

    def get_project_by_name(self, name: str) -> Optional[Project]:
        self.query.query_id = self.PROJECT_QUERY_ID

        project = Project(name=name)

        query_attrs = project.get_attributes_map(include=["name"])
        self.query.attrs.update(query_attrs)

        self.query.response_attrs.extend(project.get_property_names())

        query, value = self.query.build_query()

        response = self.session.execute(query, value)
        project = self.session.extract_project(response, self.PROJECT_QUERY_ID)

        return project

    def get_project_by_id(self, id: uuid.UUID):
        self.query.query_id = self.PROJECT_QUERY_ID

        project = Project(id=id)

        query_attrs = project.get_attributes_map(include=["id"])
        self.query.attrs.update(query_attrs)

        self.query.response_attrs.extend(project.get_property_names())

        query, value = self.query.build_query()

        response = self.session.execute(query, value)
        project = self.session.extract_project(response, self.PROJECT_QUERY_ID)

        return project

    def delete_project(self, id: uuid.UUID):
        query_id = "deleteProject"
        self.query.query_id = query_id
        project = Project(id=id)
        query_attrs = project.get_attributes_map(include=["id"])
        self.query.attrs.update(query_attrs)
        self.query.required_attrs.extend(
            project.get_property_names(include=["id"])
        )

        query, values = self.query.build_mutation_query()

        response = self.session.execute(query, values)

        return self.session.get_result_from_response(response, query_id)


    def upload_pointcloud_data(self, manifest_file_path:str, dataset_name:str, data_key:str = None, manifest_file_name:str = None):
        if not os.path.isfile(manifest_file_path):
            raise ParameterException("[ERROR] Invalid meta path. Upload failed.")
        if dataset_name is None or not isinstance(dataset_name, str):
            raise ParameterException("[ERROR] Invalid dataset name. Upload failed")
        
        # Load manifest file
        with open(manifest_file_path, 'r') as file:
            try:
                manifest_file_name = manifest_file_name if manifest_file_name is not None else "manifest.json"
                manifest_file_size = os.path.getsize(manifest_file_path)
                meta = json.load(file)
            except json.decoder.JSONDecodeError as e:
                print("[ERROR] Manifest file does not json file. Upload failed.")
                raise e
            
        # Manifest validation
        try:
            data_key = meta["key"] if data_key is None else data_key
        except:
            print("[ERROR] Key load failed. Check manifest file contents.")
        try:
            manifest = meta["manifest"]
            frame_count = manifest["frame_count"]
            frames = manifest["frames"]
            if len(frames) != frame_count:
                raise ParameterException
            total_image_count = 0
            for i in range(0, len(frames)):
                total_image_count += len(frames[i]['images'])
            total_file_count = len(frames) + total_image_count
            prefix = os.path.dirname(manifest_file_path)
        except Exception as e:
            raise ParameterException("[ERROR] Manifest load failed. Check manifest file contents.")
        
        # Frame info validation & Data transform
        try:
            frame_infos = []
            for frame in frames:
                frame_infos.append({
                    "frame_number": frame["frame_number"],
                    "frame_file_name": frame["frame_path"],
                    "frame_file_size": os.path.getsize(os.path.join(prefix, frame["frame_path"])),
                    "image_count": len(frame["images"]),
                    "image_infos": [{
                        "image_file_name": image["image_path"],
                        "image_file_size": os.path.getsize(os.path.join(prefix, image["image_path"])),
                    } for image in frame["images"]]
                })
        except Exception as e:
            raise ParameterException("[ERROR] Build frame info failed. Check manifest file contents.")
        
        # Build assets_request body
        try:
            pointcloud_data = {
                "key": data_key,
                "group": dataset_name,
                "manifest_file_name": manifest_file_name,
                "manifest_file_size": manifest_file_size,
                "total_file_count": total_file_count,
                "frame_count": frame_count,
                "frame_infos": frame_infos,
            }
        except Exception as e:
            print("[ERROR] Error build assets data. Check manifest file contents.")
            raise e

        try:
            request_body = {
                "type": "pointclouds-presigned-url",
                "fileInfo": pointcloud_data
            }
        except Exception as e:
            print("[ERROR] Error build create request data. Check manifest file contents.")
            raise e
        # Generate graphql query
        query = "mutation ($type:String!, $fileInfo:JSONObject!) { createDatum (type: $type, fileInfo: $fileInfo) {id info dataKey dataset readUrl readCustomUrl { base_url query } uploadUrl createdAt createdBy lastUpdatedAt lastUpdatedBy}}"
        response = self.session.execute(query, request_body)
        response_json = response.json()
        if 'errors' in response_json:
            errors = response_json['errors']
            raise APIFormatException(message=errors[0]['message'])

        data = response_json['data']['createDatum']
        created_asset = PointcloudData(**data)

        # Build upload urls
        try:
            urls = created_asset.upload_url["url"]["image_urls"]
            manifest_upload_url = urls["manifest_url"]
            frame_upload_urls = urls["frame_urls"]
        except Exception as e:
            raise APIUnknownException("[ERROR] Error build upload file urls. Plz, delete data from suite.")

        # Upload manifest file

        with open(manifest_file_path, 'rb') as file, requests_retry_session() as session:
            session.put(
                manifest_upload_url,
                data=file
            )

        for idx, value in enumerate(frame_upload_urls):
            frame_url = value["frame_url"]
            frame_info = frame_infos[idx]
            # Upload frame content
            with open(os.path.join(prefix, frame_info["frame_file_name"]), 'rb') as file, requests_retry_session()  as session:
                session.put(
                    frame_url,
                    data=file
                )
            
            # Extract image contents
            image_urls = value["image_urls"]
            image_infos = frame_info["image_infos"]
            for image_idx, image_url in enumerate(image_urls):
                image_info = image_infos[image_idx]
                # Upload image content
                with open(os.path.join(prefix, image_info["image_file_name"]), 'rb') as file, requests_retry_session()  as session :
                    session.put(
                        image_url,
                        data=file
                    )

        return created_asset
    