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
    _IMAGE_URL_LIFETIME_IN_SECONDS = 3600

    def __init__(self, data, project, credential=None):
        super().__init__()
        self.credential = credential
        if data.project_id is None or data.id is None:
            raise ParameterException(f"[ERROR] Data Handler cannot be initiated.")
        self._project = project
        self._data=data
        self._created = time.time()
        self._init_label_build_info()

    def _init_label_build_info(self):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            self._label_build_params = LabelInfoBuildParams(
                label_interface=self._project.label_interface,
                result=self._data.result,
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
    def get_workapp(self):
        return self._data.workapp

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

    def get_review_status(self):
        return self._data.last_review_action

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

        return self._data.data_url

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

        return True

    def update_info(self):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        build_params = (
            self._label_build_params
            if self._data.workapp == WorkappType.IMAGE_SIESTA.value
            else None
        )
        self._data = manager.update_info(
            label=self._data, info_build_params=build_params
        )
        self._init_label_build_info()
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
        return self._data

    def update_status(self, status: str):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_status(
            label=self._data,
            status=status
        )
        return self._data

    def update_review_status(self, status: str):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_review_status(
            label=self._data,
            status=status
        )
        return self._data

    def update_assignee(self, assignee: Optional[Union[User, str]]):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_assignee(
            label=self._data,
            assignee=assignee
        )
        return self._data

    def update_reviewer(self, reviewer: Optional[Union[User, str]]):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_reviewer(
            label=self._data,
            reviewer=reviewer
        )
        return self._data
