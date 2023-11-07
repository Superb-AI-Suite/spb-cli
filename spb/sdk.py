# MIT License
#
# Copyright (c) 2020 Superb AI Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import glob
import json
import logging
import os
import random
import time
import uuid
from typing import List, Optional, Dict, Union

import boto3
import spb
from natsort import natsorted

# from spb.assets.asset import Asset
# from spb.assets.manager import AssetManager
from spb.exceptions import (
    NotSupportedException,
    ParameterException,
    PreConditionException,
)
from spb.exports.manager import ExportManager
from spb.labels.manager import LabelManager
from spb.labels.label import Label, WorkappType
from spb.projects import Project, Tag
from spb.projects.manager import ProjectManager
from spb.tasks.manager import TaskManager
from spb.utils.utils import requests_retry_session
from spb.image_sdk import DataHandle
from spb.video_sdk import VideoDataHandle
from spb.pointcloud_sdk import PointcloudDataHandle
from spb.utils.search_filter import SearchFilter
from spb.users.manager import UserManager
from spb.users import User

logger = logging.getLogger()

__author__ = spb.__author__
__version__ = spb.__version__

__all__ = ("Client", "DataHandle", "VideoDataHandle", "PointcloudDataHandle")


class Client(object):
    def __init__(
        self, project_name=None, team_name: str = None, access_key: str = None
    ):
        super().__init__()

        if team_name is not None and access_key is not None:
            spb.setup_default_session(team_name=team_name, access_key=access_key)
            self.credential = {
                "team_name": team_name,
                "access_key": access_key,
            }
        else:
            self.credential = {"team_name": None, "access_key": None}

        if project_name is None:
            self._project = None
        else:
            self._project = self.get_project(name=project_name)
        self._s3 = boto3.client("s3")

    ##############################
    # Immutable variables
    ##############################

    def get_project_id(self):
        if self._project is None:
            print("[WARNING] Project is not described.")
            return None
        return self._project.id

    def get_project_name(self):
        if self._project is None:
            print("[WARNING] Project is not described.")
            return None
        return self._project.name

    def get_project_type(self):
        if self._project is None:
            print("[WARNING] Project is not described.")
            return None
        return self._project.get_project_type()

    ##############################
    # Constructor
    ##############################

    def create_project(
        self,
        name: str,
        label_interface: dict,
        description: str = "",
        is_public: bool = False,
        allow_advanced_qa: bool = False,
    ):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        project = manager.create_project(
            name=name,
            label_interface=label_interface,
            description=description,
            is_public=is_public,
            allow_advanced_qa=allow_advanced_qa,
        )
        if project:
            self._project = project
            print(f"[INFO] create project success: {self._project.name}.")

    def update_project(
        self,
        id: uuid.UUID,
        new_name: str = None,
        label_interface: dict = None,
        description: str = None,
        is_public: bool = None,
        allow_advanced_qa: bool = None,
    ):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if not (id or new_name or label_interface or description or is_public):
            raise ParameterException(
                "[ERROR] More than one paramter should be described."
            )
        project = manager.update_project(
            id=id,
            new_name=new_name,
            label_interface=label_interface,
            description=description,
            is_public=is_public,
            allow_advanced_qa=allow_advanced_qa,
        )

        if project:
            self._project = project
            print(f"[INFO] Update project success: {self._project.name}.")

    def get_project(self, name: str = None, id: uuid.UUID = None):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if id:
            project = manager.get_project_by_id(id=id)
        elif name:
            project = manager.get_project_by_name(name=name)
        else:
            raise ParameterException(f"[ERROR] Project name or id should be described.")
        return project

    def get_projects(
        self,
        page: int = 1,
        page_size: int = 10,
        name_icontains: str = None,
        data_type: str = None,
        annotation_type: List[str] = None,
    ):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if page < 1:
            raise ParameterException(
                f"[ERROR] page: index out of bound, must be in [1, inf]."
            )
        count, projects = manager.get_project_list(
            page=page,
            page_size=page_size,
            name_icontains=name_icontains,
            data_type=data_type,
            annotation_type=annotation_type,
        )
        return (count, projects)

    def set_project(
        self, project: Project = None, name: str = None, id: uuid.UUID = None
    ):
        if project:
            self._project = project
        elif name:
            self._project = self.get_project(name=name)
        elif id:
            self._project = self.get_project(id=id)
        else:
            raise ParameterException(f"[ERROR] Project or name should be described.")
        if self._project:
            print(f"[INFO] Set project success: {self._project.name}")

    def delete_project(self, name: str = None, id: uuid.UUID = None):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if id is None and name:
            id = manager.get_project_by_name(name=name).id
        if id:
            try:
                manager.delete_project(id=id)
            except PreConditionException as e:
                print(
                    f"[ERROR] If the project contains any labels, the project cannot be deleted."
                )
                raise e
        else:
            raise ParameterException(f"[ERROR] Project name or id should be described.")
        print(f"[INFO] Delete project success {id}.")

    def get_project_users(self) -> (int, List[User]):
        user_manager = UserManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        return user_manager.get_project_users(
            project_id=self._project.id
        )
    
    def get_project_tags(self) -> (int, List[Tag]):
        projects = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        return projects.get_tags(
            project_id=self._project.id
        )

    @property
    def project(self):
        if self._project is None:
            print("[WARNING] Project is not described.")
            return None
        else:
            return self._project

    @project.setter
    def project(self, project: Project):
        self._project = project

    ##############################
    # Simple SDK functions
    ##############################

    def get_num_data(self, tags=[], **kwargs):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project is not described.")

        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        tags = [{"name": tag} for tag in tags]
        option = {"project_id": self._project.id, "tags": tags, **kwargs}
        num_data = manager.get_labels_count(**option)

        if num_data == 0:
            print("[WARNING] Label list is empty.")

        return num_data

    def get_num_labels(
        self,
        filter: Optional[SearchFilter] = None,
    ):
        if self._project is None:
            raise ParameterException("[ERROR] Project is not described.")

        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        count = manager.search_labels_count(
            project=self._project,
            filter=filter
        )
        if count == 0:
            print("[WARNING] Label list is empty.")
        return count

    def get_labels(
        self,
        filter: Optional[SearchFilter] = None,
        cursor: Optional[str] = None,
        page_size: int = 10,
    ):
        if self._project is None:
            raise ParameterException("[ERROR] Project is not described.")

        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        count, labels, cursor = manager.search_labels(
            project=self._project,
            filter=filter,
            cursor=cursor,
            page_size=page_size
        )
        workapp = self._project.workapp
        handlers = []
        for label in labels:
            if workapp == "video-siesta":
                handlers.append(VideoDataHandle(label, self._project, self.credential))
            elif workapp == "pointclouds-siesta":
                handlers.append(PointcloudDataHandle(label, self._project, self.credential))
            else:
                handlers.append(DataHandle(label, self._project, self.credential))
        return count, handlers, cursor
    
    def get_label_ids(
        self,
        filter: Optional[SearchFilter] = None,
        cursor: Optional[str] = None,
        page_size: int = 100,
    ):
        if self._project is None:
            raise ParameterException("[ERROR] Project is not described.")
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        count, labels, cursor = manager.search_label_ids(
            project=self._project,
            filter=filter,
            cursor=cursor,
            page_size=page_size
        )
        handlers = []
        for label in labels:
            handlers.append(self.build_data_handle(label_id=label.id))
        return count, handlers, cursor

    def build_data_handle(self, label_id: Union[uuid.UUID, str]):
        """
        Build data handle from label id
        :param label_id: label id
        :return: data handle (DataHandle, VideoDataHandle, PointcloudDataHandle)
        """
        if self._project is None:
            raise ParameterException("[ERROR] Project is not described.")
        label = Label(
            id=label_id if isinstance(label_id, uuid.UUID) else uuid.UUID(label_id),
            project_id=self._project.id,
        )
        if self._project.workapp == "image-siesta":
            label.workapp = WorkappType.IMAGE_SIESTA.value
            return DataHandle(
                data=label,
                project=self._project,
                credential=self.credential,
                label_id_only=True,
            )
        elif self._project.workapp == "video-siesta":
            label.workapp = WorkappType.VIDEO_SIESTA.value
            return VideoDataHandle(
                data=label,
                project=self._project,
                credential=self.credential,
                label_id_only=True,
            )
        elif self._project.workapp == "pointclouds-siesta":
            label.workapp = WorkappType.POINTCLOUDS_SIESTA.value
            return PointcloudDataHandle(
                data=label,
                project=self._project,
                credential=self.credential,
                label_id_only=True
            )
        else:
            raise NotSupportedException(f"[ERROR] {label.workapp} is not supported.")

    def get_data_page(
        self,
        page_idx=0,
        page_size=10,
        tags=[],
        dataset=None,
        data_key=None,
        page=1,
        **kwargs,
    ):
        if page < 1:
            raise ParameterException(
                f"[ERROR] page: index out of bound, must be in [1, inf]."
            )

        if page_idx >= 0:
            page_idx += 1

        if page > 1:
            page_idx = page

        if self._project is None:
            raise ParameterException(f"[ERROR] Project is not described.")

        workapp = self._project.workapp
        if workapp == "video-siesta":
            # Video
            command = spb.Command(type="describe_videolabel")
            tags = [{"name": tag} for tag in tags]
            option = {"project_id": self._project.id, "tags": tags, **kwargs}
            # manager = VideoLabelManager(self.credential["team"], self.credential["access_key"])
            # _, data_page = manager.get_labels(**option)
            data_page, _ = spb.run(
                command=command,
                option=option,
                page=page_idx,
                page_size=page_size,
            )
            for data in data_page:
                yield VideoDataHandle(data, self._project, self.credential)
        elif workapp == "pointclouds-siesta":
            manager = LabelManager(
                self.credential["team_name"], self.credential["access_key"]
            )
            tags = [{"name": tag} for tag in tags]
            option = {
                "project_id": self._project.id,
                "tags": tags,
                "page": page_idx,
                "page_size": page_size,
                "dataset": dataset,
                "data_key": data_key,
                **kwargs,
            }
            _, data_page = manager.get_labels(**option)
            for data in data_page:
                yield PointcloudDataHandle(data, self._project, self.credential)
        else:
            manager = LabelManager(
                self.credential["team_name"], self.credential["access_key"]
            )
            tags = [{"name": tag} for tag in tags]
            option = {
                "project_id": self._project.id,
                "tags": tags,
                "page": page_idx,
                "page_size": page_size,
                "dataset": dataset,
                "data_key": data_key,
                **kwargs,
            }
            _, data_page = manager.get_labels(**option)
            for data in data_page:
                yield DataHandle(data, self._project, self.credential)

    def get_data(self, id: uuid.UUID):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project is not described.")
        if id is None:
            raise ParameterException(f"[ERROR] ID is required.")

        workapp = self._project.workapp
        if workapp == "video-siesta":
            raise NotSupportedException("[ERROR] Video does not supported.")

        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        label = manager.get_label(project_id=self._project.id, id=id)
        if label is not None:
            if workapp == "pointclouds-siesta":
                return PointcloudDataHandle(label, self._project, self.credential)
            else:
                return DataHandle(label, self._project, self.credential)

    def upload_image(self, path, dataset_name, key=None, name=None):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        if not os.path.isfile(path):
            raise ParameterException(f"[ERROR] Invalid path.")

        if name is None:
            name = path.split("/")[-1]

        if key is None:
            key = name

        command = spb.Command(type="create_data")
        option = {
            "file": path,
            "file_name": name,
            "dataset": dataset_name,
            "data_key": key,
        }

        result = spb.run(
            command=command,
            optional={"projectId": self._project.id},
            option=option,
        )
        
        presigned_url = result.presigned_url
        data = open(path, "rb").read()
        with requests_retry_session() as session:
            response = session.put(presigned_url, data=data)
        return result

    def upload_image_s3(self, bucket_name, path, dataset_name, key=None):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID is not described.")

        name = path.split("/")[-1]
        ext = path.split(".")[-1]
        temp_path = "{:032x}.{}".format(random.getrandbits(128), ext)

        self._s3.download_file(bucket_name, path, temp_path)

        result = self.upload_image(temp_path, dataset_name, key, name=name)

        if os.path.isfile(temp_path):
            os.remove(temp_path)

        return result

    def upload_video(self, path, dataset_name, key=None):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        if not os.path.isdir(path):
            raise ParameterException(f"[ERROR] Invalid path. Upload failed.")

        # TODO: support_img_format is const
        support_img_format = ("png", "jpg", "bmp", "jpeg", "tiff", "tif")
        file_names = [
            os.path.basename(file_path)
            for file_path in glob.glob(os.path.join(path, "*"))
            if file_path.lower().endswith(support_img_format)
        ]
        if len(file_names) == 0:
            raise ParameterException(f"[ERROR] Invalid path. Upload failed.")

        if key is None:
            key = os.path.split(path)[-1]

        asset_video = {
            "dataset": dataset_name,
            "data_key": key,
            "files": {
                "path": path,
                "file_names": natsorted(file_names),
            },
        }
        command = spb.Command(type="create_videodata")
        result = spb.run(
            command=command,
            option=asset_video,
            optional={"projectId": self._project.id},
        )
        file_infos = json.loads(result.file_infos)
        for file_info in file_infos:
            file_name = file_info["file_name"]
            file_path = os.path.join(path, file_name)
            data = open(file_path, "rb").read()
            with requests_retry_session() as session:
                response = session.put(file_info["presigned_url"], data=data)
        return result
    

    def upload_pointcloud_data(self, manifest_file_path:str, dataset_name:str, data_key:str = None, manifest_file_name:str =None):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        return manager.upload_pointcloud_data(
            manifest_file_path=manifest_file_path,
            dataset_name=dataset_name,
            data_key=data_key,
            manifest_file_name=manifest_file_name
        )
        

    def get_export_list(self, page: int = 1, page_size: int = 10):
        if page < 1:
            raise ParameterException(
                f"[ERROR] page: index out of bound, must be in [1, inf]."
            )
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")
        manager = ExportManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        exports = manager.get_exports(
            project_id=self._project.id, page=page, page_size=page_size
        )
        return exports

    def get_export(self, id: uuid.UUID = None, name: str = None):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")
        if id is None and name is None:
            raise ParameterException(f"[ERROR] id or name is required.")

        manager = ExportManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        export = manager.get_export(project_id=self._project.id, id=id, name=name)
        return export

    def get_task_list(self, status_in, page: int = 1, page_size: int = 10):
        if page < 1:
            raise ParameterException(
                f"[ERROR] page: index out of bound, must be in [1, inf]."
            )

        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        task_list = manager.get_task_list(
            project_id=self._project.id,
            status_in=status_in,
            page=page,
            page_size=page_size,
        )
        return task_list

    def get_task_by_id(self, task_id: str):
        if task_id is None:
            raise ParameterException(f"[ERROR] Task ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        task_detail = manager.get_task_by_id(task_id=task_id)
        return task_detail

    def get_task_progress_by_id(self, task_id: str):
        if task_id is None:
            raise ParameterException(f"[ERROR] Task ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        task_progress = manager.get_task_progress_by_id(task_id=task_id)
        return task_progress

    def wait_until_complete(self, task_id: str):
        if task_id is None:
            raise ParameterException(f"[ERROR] Task ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )

        while True:
            time.sleep(5)
            task_progress = manager.get_task_progress_by_id(task_id=task_id)
            progress_percentage = 0
            if task_progress.progress > 0:
                progress_percentage = (
                    task_progress.total_count / task_progress.progress
                ) * 100
            print("Progress Percentage: {}".format(progress_percentage))
            if task_progress.status == "FINISHED":
                print("Task Completed.")
                break
            elif task_progress.status == "FAILED":
                print("Task Failed.")
                break
            elif task_progress.status == "CANCELED":
                print("Task has been canceled.")
                break

        return task_progress

    def request_auto_label_task(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        auto_label_task_request = manager.request_auto_label_task(
            project_id=self._project.id, tags=tags, filter=filter
        )

        return auto_label_task_request

    def assign_reviewer(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None,
        distribution_method: str = "EQUAL",
        work_assignee: list = [],
    ):
        if filter is None:
            filter = SearchFilter()
        temp_filter = SearchFilter()
        temp_filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        if len(work_assignee) == 0:
            raise ParameterException(
                f"[ERROR] Number of work assignee must be greater than 0."
            )

        if distribution_method.upper() not in ["EQUAL", "PROPORTIONAL"]:
            raise ParameterException(
                f"[ERROR] Distribution method must be EQUAL or PROPORTIONAL."
            )

        label_manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        limit = label_manager.search_labels_count(
            project=self._project, filter=temp_filter
        )
        if limit == 0:
            print(
                "[WARNING] There is no label detected by filter. Please check the filter again."
            )
            return None

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        assign_reviewer_task = manager.assign_reviewer(
            project_id=self._project.id,
            tags=[],
            filter=filter,
            limit=limit,
            distribution_method=distribution_method.upper(),
            work_assignee=work_assignee,
        )
        return assign_reviewer_task

    def unassign_reviewer(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        unassign_reviewer_task = manager.unassign_reviewer(
            project_id=self._project.id,
            tags=tags,
            filter=filter
        )
        return unassign_reviewer_task

    def assign_labeler(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None,
        distribution_method: str = "EQUAL",
        work_assignee: list = [],
    ):
        if filter is None:
            filter = SearchFilter()
        temp_filter = SearchFilter()
        temp_filter.tag_name_all = filter.tag_name_all + tags if isinstance(filter.tag_name_all, list) else tags
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        if len(work_assignee) == 0:
            raise ParameterException(
                f"[ERROR] The number of work assignee must be greater than 0."
            )

        if distribution_method.upper() not in ["EQUAL", "PROPORTIONAL"]:
            raise ParameterException(
                f"[ERROR] Distribution method must be EQUAL or PROPORTIONAL."
            )

        label_manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        limit = label_manager.search_labels_count(
            project=self._project, filter=temp_filter
        )
        if limit == 0:
            print(
                "[WARNING] There is no label detected by filter. Please check the filter again."
            )
            return None

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        assign_labeler_task = manager.assign_labeler(
            project_id=self._project.id,
            tags=tags,
            filter=filter,
            limit=limit,
            distribution_method=distribution_method.upper(),
            work_assignee=work_assignee,
        )
        return assign_labeler_task

    def export_labels(
            self,
            export_name: Optional[str] = None,
            tags: list = [],
            filter: Optional[SearchFilter] = None,
            request_custom_auto_label: bool = False,
            request_transform: bool = False,
            custom_auto_label_configuration: Optional[Dict[str, str]] = None,
            transform_configuration: Optional[Dict[str, str]] = None
    ):
        """Request export labels

        Args:
            project_id (string): project id to request
            export_name (Optional[string]): Export name to be made (default auto generation)
            tags (List[string]): tag names to be exported of labels
            request_custom_auto_label (boolean): Request custom auto label with this export
            request_transform (boolean): Request export transform with this export
            custom_auto_label_configuration (Optional[Dict[str, str]]):
                Custom auto label configuration (format : {"name": "CUSTOM_AUTO_LABEL_NAME"})
            transform_configuration (Optional[Dict[str, str]]):
                Export transform configuration (format : {"type": "COCO" | "YOLO"})

        Returns:
            Task: export labels task
        """
        if self._project is None:
            raise ParameterException("[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        export_labels_task = manager.export_labels_task(
            project=self._project,
            export_name=export_name,
            tags=tags,
            filter=filter,
            request_custom_auto_label=request_custom_auto_label,
            request_transform=request_transform,
            custom_auto_label_configuration=custom_auto_label_configuration,
            transform_configuration=transform_configuration
        )
        return export_labels_task

    def unassign_labeler(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        unassign_labeler_task = manager.unassign_labeler(
            project_id=self._project.id,
            tags=tags,
            filter=filter,
        )
        return unassign_labeler_task

    def initialize_label(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        initialize_label_task_request = manager.initialize_label(
            project_id=self._project.id, tags=tags, filter=filter,
        )

        return initialize_label_task_request

    def submit_label(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        submit_label_task_request = manager.submit_label(
            project_id=self._project.id, tags=tags, filter=filter,
        )

        return submit_label_task_request

    def skip_label(
        self,
        tags: list = [],
        filter: Optional[SearchFilter] = None
    ):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        skip_task_request = manager.skip_label(
            project_id=self._project.id, tags=tags, filter=filter,
        )

        return skip_task_request

    # TO BE ADDED
    # def edit_label_tags(self, label_ids: list=[], add_tags: list=[], remove_tags: list=[]):
    #     if self._project is None:
    #         raise ParameterException(f'[ERROR] Project ID does not exist.')

    #     try:
    #         manager = TaskManager()
    #         edit_label_tags_task = manager.edit_label_tags(
    #             project_id=self._project.id,
    #             label_ids=label_ids,
    #             add_tags=add_tags,
    #             remove_tags=remove_tags
    #         )
    #         return edit_label_tags_task

    #     except Exception as e:
    #         raise CustomBaseException(e)
