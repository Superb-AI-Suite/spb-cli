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
import urllib
import uuid

import boto3
import skimage.io

from natsort import natsorted

import spb
from spb.exceptions import (
    CustomBaseException,
    NotSupportedException,
    ParameterException,
    NotFoundException,
)
from spb.exports.manager import ExportManager
from spb.labels.label import Tags, WorkappType
from spb.labels.manager import LabelManager
from spb.labels.serializer import LabelInfoBuildParams
from spb.libs.phy_credit.phy_credit.video import build_label_info
from spb.projects import Project
from spb.projects.manager import ProjectManager
from spb.tasks.manager import TaskManager
from spb.utils.utils import requests_retry_session

logger = logging.getLogger()

__author__ = spb.__author__
__version__ = spb.__version__

__all__ = ("Client", "DataHandle", "VideoDataHandle")


class Client(object):
    def __init__(
        self, project_name=None, team_name: str = None, access_key: str = None
    ):
        super().__init__()

        if team_name is not None and access_key is not None:
            print(f"[INFO] Usage: Client has been started with {team_name}")
            spb.setup_default_session(team_name=team_name, access_key=access_key)
            self.credential = {
                "team_name": team_name,
                "access_key": access_key,
            }
        else:
            self.credential = {"team_name": None, "access_key": None}

        if project_name is None:
            # print("[WARNING] Client cannot be used to describe label without project")
            self._project = None
        else:
            self._project = self.get_project(project_name)
        self._s3 = boto3.client("s3")

    ##############################
    # Immutable variables
    ##############################

    def get_project_id(self):
        if self._project is None:
            print("[WARNING] Project is not described")
            return None
        return self._project.id

    def get_project_name(self):
        if self._project is None:
            print("[WARNING] Project is not described")
            return None
        return self._project.name

    def get_project_type(self):
        if self._project is None:
            print("[WARNING] Project is not described")
            return None
        return self._project.get_project_type()

    ##############################
    # Constructor
    ##############################

    # def create_project(self, project_info):
    #     manager = ProjectManager(
    #         self.credential["team_name"], self.credential["access_key"]
    #     )
    #     return manager.create_project(project_info)

    def get_project(self, project_name: str = None, project_id: str = None):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if project_name:
            project = manager.get_project_by_name(name=project_name)
        elif project_id:
            project = manager.get_project_by_id(id=project_id)
        else:
            raise ParameterException(f"[ERROR] Project name or id should be described")

        if project is None:
            raise NotFoundException("[ERROR] Project {} not found".format(project_name))

        return project

    def get_projects(self, page: int = 1, page_size: int = 10):
        manager = ProjectManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if page < 1:
            raise ParameterException(
                f"[ERROR] page: index out of bound, must be in [1, inf]"
            )
        count, projects = manager.get_project_list(page=page, page_size=page_size)
        return (count, projects)

    def set_project(self, project: Project):
        self._project = project
        if self._project:
            print(f"[INFO] set project success: {self._project.name}")

    def set_project_by_name(self, project_name: str):
        self._project = self.get_project(project_name)
        if self._project:
            print(f"[INFO] set project success: {project_name}")

    @property
    def project(self):
        if self._project is None:
            print("[WARNING] Project is not described")
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
            raise ParameterException(f"[ERROR] Project is not described")

        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        tags = [{"name": tag} for tag in tags]
        option = {"project_id": self._project.id, "tags": tags, **kwargs}
        num_data = manager.get_labels_count(**option)

        if num_data == 0:
            print("[WARNING] Label list is empty")

        return num_data

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
                f"[ERROR] page: index out of bound, must be in [1, inf]"
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
            data_page, _ = spb.run(
                command=command, option=option, page=page_idx, page_size=page_size
            )
            for data in data_page:
                yield VideoDataHandle(data, self._project, self.credential)
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
        else:
            manager = LabelManager(
                self.credential["team_name"], self.credential["access_key"]
            )
            label = manager.get_label(project_id=self._project.id, id=id)
            if label is not None:
                return DataHandle(label, self._project, self.credential)

    def upload_image(self, path, dataset_name, key=None, name=None):
        # TODO: command -> asset manager 로 만들기.
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
            command=command, optional={"projectId": self._project.id}, option=option
        )
        presigned_url = result.presigned_url
        data = open(path, "rb").read()
        with requests_retry_session() as session:
            response = session.put(presigned_url, data=data)
        return True

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
            raise ParameterException(f"[ERROR] Invalid path. Upload failed")

        # TODO: support_img_format is const
        support_img_format = ("png", "jpg", "bmp", "jpeg", "tiff", "tif")
        file_names = [
            os.path.basename(file_path)
            for file_path in glob.glob(os.path.join(path, "*"))
            if file_path.lower().endswith(support_img_format)
        ]
        if len(file_names) == 0:
            raise ParameterException(f"[ERROR] Invalid path. Upload failed")

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
        return True

    # def get_asset_by_id(self, id: uuid.UUID):
    #     manager = AssetManager(
    #         self.credential["team_name"], self.credential["access_key"]
    #     )
    #     asset = manager.get_asset_by_id(id)
    #     return asset

    # def get_asset_list(self, cursor: bytes = None, page_size: int = 10):
    #     manager = AssetManager(
    #         self.credential["team_name"], self.credential["access_key"]
    #     )
    #     count, prev, nxt, assets = manager.get_assets(
    #         cursor=cursor, page_size=page_size
    #     )
    #     return count, prev, nxt, assets

    # def get_asset_download_url(self, asset: Asset):
    #     manager = AssetManager(
    #         self.credential["team_name"], self.credential["access_key"]
    #     )
    #     download_url = manager.get_download_url(asset)
    #     return download_url

    # def assign_asset(self, asset: Asset, project: Project):
    #     manager = AssetManager(
    #         self.credential["team_name"], self.credential["access_key"]
    #     )
    #     result = manager.assign_asset(asset, project)
    #     return result

    def get_export_list(self, page: int = 1, page_size: int = 10):
        if page < 1:
            raise ParameterException(
                f"[ERROR] page: index out of bound, must be in [1, inf]"
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

    # def get_masks_by_export(self, id: uuid.UUID = None, name: str = None):
    #     if self._project is None:
    #         raise ParameterException(f"[ERROR] Project ID does not exist.")
    #     if id is None and name is None:
    #         raise ParameterException(f"[ERROR] id or name is required.")

    #     manager = ExportManager(
    #         self.credential["team_name"], self.credential["access_key"]
    #     )
    #     masks = manager.get_masks(project_id=self._project.id, id=id, name=name)
    #     return masks

    def get_task_list(self, status_in, page: int = 1, page_size: int = 10):
        if page < 1:
            raise ParameterException(
                f"[ERROR] page: index out of bound, must be in [1, inf]"
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
                progress_percentage = (task_progress.total_count / task_progress.progress) * 100
            print("Progress Percentage: {}".format(progress_percentage))
            if task_progress.status == "FINISHED":
                print("Task Completed")
                break
            elif task_progress.status == "FAILED":
                print("Task Failed")
                break
            elif task_progress.status == "CANCELED":
                print("Task has been canceled")
                break

        return task_progress

    def request_auto_label_task(self, tags: list = []):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        auto_label_task_request = manager.request_auto_label_task(
            project_id=self._project.id, tags=tags
        )

        return auto_label_task_request

    def assign_reviewer(
        self,
        tags: list = [],
        distribution_method: str = "EQUAL",
        work_assignee: list = [],
    ):
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
        limit = label_manager.get_labels_count(
            project_id=self._project.id, tags=[{"name": tag} for tag in tags]
        )

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        assign_reviewer_task = manager.assign_reviewer(
            project_id=self._project.id,
            tags=tags,
            limit=limit,
            distribution_method=distribution_method.upper(),
            work_assignee=work_assignee,
        )
        return assign_reviewer_task

    def unassign_reviewer(self, tags: list = []):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        unassign_reviewer_task = manager.unassign_reviewer(
            project_id=self._project.id,
            tags=tags,
        )
        return unassign_reviewer_task

    def assign_labeler(
        self,
        tags: list = [],
        distribution_method: str = "EQUAL",
        work_assignee: list = [],
    ):
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
        limit = label_manager.get_labels_count(
            project_id=self._project.id, tags=[{"name": tag} for tag in tags]
        )

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        assign_labeler_task = manager.assign_labeler(
            project_id=self._project.id,
            tags=tags,
            limit=limit,
            distribution_method=distribution_method.upper(),
            work_assignee=work_assignee,
        )
        return assign_labeler_task

    def unassign_labeler(self, tags: list = []):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        unassign_labeler_task = manager.unassign_labeler(
            project_id=self._project.id,
            tags=tags,
        )
        return unassign_labeler_task

    def initialize_label(self, tags: list = []):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        initialize_label_task_request = manager.initialize_label(
            project_id=self._project.id, tags=tags
        )

        return initialize_label_task_request

    def submit_label(self, tags: list = []):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        submit_label_task_request = manager.submit_label(
            project_id=self._project.id, tags=tags
        )

        return submit_label_task_request

    def skip_label(self, tags: list = []):
        if self._project is None:
            raise ParameterException(f"[ERROR] Project ID does not exist.")

        manager = TaskManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        skip_task_request = manager.skip_label(
            project_id=self._project.id, tags=tags
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


class DataHandle(object):
    _IMAGE_URL_LIFETIME_IN_SECONDS = 3600

    def __init__(self, data, project, credential=None):
        super().__init__()
        self.credential = credential
        if data.project_id is None or data.id is None:
            raise ParameterException(f"[ERROR] Data Handler cannot be initiated.")
        self._data = data
        self._project = project
        self._created = time.time()

        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            self._init_label_build_info()

    def _init_label_build_info(self):
        self._label_build_params = LabelInfoBuildParams(
            label_interface=self._project.label_interface, result=self._data.result
        )

    def _is_expired_image_url(self):
        global _IMAGE_URL_LIFETIME

        is_expired = (
            time.time() - self._created > DataHandle._IMAGE_URL_LIFETIME_IN_SECONDS
        )

        if is_expired:
            print(
                "[WARNING] Image URL has been expired. Call get_data(...) of SuiteProject to renew URL"
            )

        return is_expired

    ##############################
    # Immutable variables
    ##############################

    @property
    def data(self):
        return self._data

    def get_id(self):
        return self._data.id

    def get_key(self):
        return self._data.data_key

    def get_dataset_name(self):
        return self._data.dataset

    def get_status(self):
        return self._data.status

    def get_last_review_action(self):
        return self._data.last_review_action

    def get_image_url(self):
        if self._is_expired_image_url():
            return None

        return self._data.data_url

    def get_label_interface(self):
        try:
            return self._project.label_interface
        except:
            return None

    ##############################
    # Simple SDK functions
    ##############################

    def download_image(self, download_to=None):
        if self._is_expired_image_url():
            return None, None

        if download_to is None:
            download_to = self._data.data_key
            print("[INFO] Downloaded to {}".format(download_to))

        return urllib.request.urlretrieve(self._data.data_url, download_to)

    def get_image(self):
        if self._is_expired_image_url():
            return None

        return skimage.io.imread(self._data.data_url)

    def get_category_labels(self):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            return self._label_build_params.get_categories()
        else:
            category_map = self._project.label_interface["categorization"]["word_map"]
            id_to_name = {c["id"]: c["name"] for c in category_map if c["id"] != "root"}

            try:
                labels = [
                    id_to_name[id]
                    for id in self._data.result["categorization"]["value"]
                ]
            except:
                # The given image does not have any image categorizations
                labels = []

            return labels

    def get_object_labels(self):
        try:
            if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
                labels = self._label_build_params.get_objects()
            else:
                labels = self._data.result.get("objects", [])
        except:
            # The given image does not have any object annotations
            labels = []

        return labels

    def get_tags(self):
        return [tag.name for tag in self._data.tags]

    def set_category_labels(
        self, labels: list = None, category: dict = None, properties=None
    ):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            # build new info
            self._label_build_params.set_categories(properties=properties)
            info = self._label_build_params.build_info()
            categories = {"properties": []}
            if "result" in info and "categories" in info["result"]:
                categories = info["result"]["categories"]
            # apply
            self._data.result = {
                **(self._data.result or {}),
                "categories": categories,
            }
        else:
            category_map = self._project.label_interface["categorization"]["word_map"]
            name_to_id = {c["name"]: c["id"] for c in category_map if c["id"] != "root"}

            try:
                label_ids = [name_to_id[name] for name in labels]
            except KeyError:
                raise ParameterException(f"[ERROR] Invalid category name exists")

            if not self._data.result:
                self._data.result = {}
            if "objects" not in self._data.result:
                self._data.result["objects"] = []
            self._data.result = {
                **self._data.result,
                "categorization": {"value": label_ids},
            }

    def set_object_labels(self, labels):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            # build new info
            self._label_build_params.init_objects()
            for label in labels:
                self._label_build_params.add_object(**label)
            info = self._label_build_params.build_info()
            objects = []
            if "result" in info and "objects" in info["result"]:
                objects = info["result"]["objects"]
            # apply
            self._data.result = {
                **(self._data.result or {}),
                "objects": objects,
            }
        else:
            if not self._data.result:
                self._data.result = {}
            if "categorization" not in self._data.result:
                self._data.result["categorization"] = {"value": []}
            self._data.result = {**self._data.result, "objects": labels}

    def add_object_label(self, class_name, annotation, properties=None, id=None):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            self._label_build_params.add_object(class_name, annotation, properties, id)
        elif self._data.workapp == WorkappType.IMAGE_DEFAULT.value:
            print("[ERROR] add_object_list doesn't support.")

    def update_data(self):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        build_params = (
            self._label_build_params
            if self._data.workapp == WorkappType.IMAGE_SIESTA.value
            else None
        )
        self._data = manager.update_label(
            label=self._data, info_build_params=build_params
        )
        if build_params is not None:
            self._init_label_build_info()
        
        return True

    def set_tags(self, tags: list = None):
        label_tags = []
        if tags is not None and isinstance(tags, list):
            for tag in tags:
                label_tags.append(Tags(name=tag))

        self._data.tags = label_tags


class VideoDataHandle(object):
    _VIDEO_URL_LIFETIME_IN_SECONDS = 3600

    def __init__(self, data, project, credential=None):
        super().__init__()
        self.credential = credential
        self._data = data
        self._project = project
        self._info = None
        self._created = time.time()

    def _is_expired_video_url(self):
        is_expired = time.time() - self._created > self._VIDEO_URL_LIFETIME_IN_SECONDS

        if is_expired:
            print(
                "[WARNING] Video URL has been expired. Call get_data(...) of SuiteProject to renew URL"
            )

        return is_expired

    def _upload_to_suite(self, info=None):
        command = spb.Command(type="update_videolabel")
        if info is None:
            _ = spb.run(command=command, option=self._data)
        else:
            _ = spb.run(
                command=command, option=self._data, optional={"info": json.dumps(info)}
            )

    ##############################
    # Immutable variables
    ##############################

    @property
    def data(self):
        return self._data

    def get_id(self):
        return self._data.id

    def get_key(self):
        return self._data.data_key

    def get_dataset_name(self):
        return self._data.dataset

    def get_status(self):
        return self._data.status

    def get_last_review_action(self):
        return self._data.last_review_action

    def get_frame_url(self, idx, data_url=None):
        if self._is_expired_video_url():
            return None

        if data_url is None:
            data_url = json.loads(self._data.data_url)

        file_ext = data_url["file_infos"][idx]["file_name"].split(".")[-1].lower()
        file_name = f"image_{(idx+1):08}.{file_ext}"
        return f"{data_url['base_url']}{file_name}?{data_url['query']}"

    def get_frame_urls(self):
        if self._is_expired_video_url():
            return None

        data_url = json.loads(self._data.data_url)
        for frame_idx in range(len(data_url["file_infos"])):
            yield self.get_frame_url(frame_idx, data_url)

    def get_label_interface(self):
        try:
            return self._project.label_interface
        except:
            return None

    ##############################
    # Simple SDK functions
    ##############################

    def download_video(self, download_to=None):
        if self._is_expired_video_url():
            return None, None

        if download_to is None:
            download_to = self._data.data_key
            print("[INFO] Downloaded to {}".format(download_to))

        data_url = json.loads(self._data.data_url)
        for frame_idx, file_info in enumerate(data_url["file_infos"]):
            url = self.get_frame_url(frame_idx, data_url)
            urllib.request.urlretrieve(
                url, os.path.join(download_to, file_info["file_name"])
            )

        return True

    def get_frame(self, idx):
        if self._is_expired_video_url():
            return None

        return skimage.io.imread(self.get_frame_url(idx))

    def get_frames(self):
        if self._is_expired_video_url():
            return None

        for url in self.get_frame_urls():
            yield skimage.io.imread(url)

    def _get_result(self):
        try:
            label_result = None
            with requests_retry_session() as session:
                read_response = session.get(self._data.info_read_presigned_url)
                label_result = read_response.json()
            return label_result["result"]
        except:
            return None

    def set_object_labels(self, labels):
        result = self._get_result()
        if result is None:
            label_info = build_label_info(self._project.label_interface)
        else:
            label_info = build_label_info(self._project.label_interface, result=result)
            label_info.init_objects()

        for label in labels:
            label_info.add_object(**label)
        info = label_info.build_info()
        self._info = info

    def get_object_labels(self):
        result = self._get_result()
        if result is None:
            return None
        label_info = build_label_info(self._project.label_interface, result=result)
        return label_info.get_objects()

    def set_category_labels(self, label):
        result = self._get_result()
        if result is None:
            label_info = build_label_info(self._project.label_interface)
        else:
            label_info = build_label_info(self._project.label_interface, result=result)
            label_info.init_categories()

        label_info.set_categories(**label)
        info = label_info.build_info()
        self._info = info

    def get_category_labels(self):
        result = self._get_result()
        if result is None:
            return None
        label_info = build_label_info(self._project.label_interface, result=result)
        return label_info.get_categories()

    def update_data(self):
        self._upload_to_suite(info={"tags": self._info["tags"]})
        with requests_retry_session() as session:
            write_response = session.put(
                self._data.info_write_presigned_url, data=json.dumps(self._info)
            )
        return True

    def get_tags(self):
        return [tag.name for tag in self._data.tags]

    def set_tags(self, tags: list = None):
        raise NotSupportedException("[ERROR] Video does not supported.")