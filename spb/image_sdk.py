import time
import urllib

from typing import Union, Optional, List

from spb.exceptions import (
    ParameterException,
)
from spb.labels.serializer import LabelInfoBuildParams
from spb.labels.label import WorkappType, Tags
from spb.labels.manager import LabelManager
from spb.users.user import User
from spb.utils import deprecated


class DataHandle(object):
    _URL_LIFETIME_IN_SECONDS = 3600

    def __init__(self, data, project, credential=None, label_id_only=False):
        super().__init__()
        self.credential = credential
        if data.project_id is None or data.id is None:
            raise ParameterException(f"[ERROR] Data Handler cannot be initiated.")
        self._project = project
        self._data = data
        self._created = time.time()
        self._init_label_build_info()
        self.label_id_only = label_id_only

    def _init_label_build_info(self):
        self._label_build_params = LabelInfoBuildParams(
            label_interface=self._project.label_interface,
            result=self._data.result,
            workapp=self._data.workapp,
        )

    def _describe_data_detail(self):
        if self.label_id_only:
            manager = LabelManager(
                self.credential["team_name"], self.credential["access_key"]
            )
            self._data = manager.get_label(
                project_id=self._data.project_id,
                id=self._data.id,
            )
            self._created = time.time()
            self._init_label_build_info()
            self.label_id_only = False

    def _is_expired_url(self):
        is_expired = (
            time.time() - self._created > DataHandle._URL_LIFETIME_IN_SECONDS
        )

        if is_expired:
            print(
                "[WARNING] Download URL has been expired. Call get_data(...) of SuiteProject to renew URL"
            )

        return is_expired

    ##############################
    # Immutable variables
    ##############################
    def get_workapp(self):
        return self._data.workapp

    @property
    def data(self):
        self._describe_data_detail()
        return self._data

    def get_id(self):
        return self._data.id

    def get_key(self):
        self._describe_data_detail()
        return self._data.data_key

    def get_dataset_name(self):
        self._describe_data_detail()
        return self._data.dataset

    def get_status(self):
        self._describe_data_detail()
        return self._data.status

    def get_review_status(self):
        self._describe_data_detail()
        return self._data.last_review_action

    def get_last_review_action(self):
        self._describe_data_detail()
        return self._data.last_review_action

    def get_image_url(self):
        self._describe_data_detail()
        if self._is_expired_url():
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
        self._describe_data_detail()
        if self._is_expired_url():
            return None, None

        if download_to is None:
            download_to = self._data.data_key
            print("[INFO] Downloaded to {}".format(download_to))

        return urllib.request.urlretrieve(self._data.data_url, download_to)

    def get_image(self):
        self._describe_data_detail()
        if self._is_expired_url():
            return None

        return self._data.data_url

    def get_category_labels(self):
        self._describe_data_detail()
        return self._label_build_params.get_categories()

    def get_object_labels(self):
        self._describe_data_detail()
        try:
            labels = self._label_build_params.get_objects()
        except:
            # The given image does not have any object annotations
            labels = []

        return labels

    def get_tags(self):
        self._describe_data_detail()
        return [tag.name for tag in self._data.tags]

    def set_category_labels(
        self, labels: list = None, category: dict = None, properties=None
    ):
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

    def set_object_labels(self, labels):
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

    def add_object_label(self, class_name, annotation, properties=None, id=None):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            self._label_build_params.add_object(
                class_name=class_name,
                annotation=annotation,
                properties=properties,
                id=id
            )
            info = self._label_build_params.build_info()
            objects = []
            if "result" in info and "objects" in info["result"]:
                objects = info["result"]["objects"]
            self._data.result = {
                **(self._data.result or {}),
                "objects": objects,
            }
        elif self._data.workapp == WorkappType.IMAGE_DEFAULT.value:
            print("[ERROR] add_object_label doesn't support.")

    @deprecated("Use [update_info] or [update_tags]")
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
        self.label_id_only = False
        return True

    def update_info(self):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_info(
            label=self._data, info_build_params=self._label_build_params
        )
        self._init_label_build_info()
        self.label_id_only = False
        return self._data

    @deprecated("Use [update_tags].")
    def set_tags(self, tags: list = None):
        label_tags = []
        if tags is not None and isinstance(tags, list):
            for tag in tags:
                label_tags.append(Tags(name=tag))

        self._data.tags = label_tags

    def update_tags(self, tags: List[Union[str, Tags]] = []):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_tags(
            label=self._data,
            tags=tags
        )
        self.label_id_only = False
        return self._data

    def update_status(self, status: str):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_status(
            label=self._data,
            status=status
        )
        self.label_id_only = False
        return self._data

    def update_review_status(self, status: str):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_review_status(
            label=self._data,
            status=status
        )
        self.label_id_only = False
        return self._data

    def update_assignee(self, assignee: Optional[Union[User, str]]):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_assignee(
            label=self._data,
            assignee=assignee
        )
        self.label_id_only = False
        return self._data

    def update_reviewer(self, reviewer: Optional[Union[User, str]]):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_reviewer(
            label=self._data,
            reviewer=reviewer
        )
        self.label_id_only = False
        return self._data
