import time
import spb
import json
import urllib
import os

from typing import Union, List

from spb.utils.utils import requests_retry_session
from spb.libs.phy_credit.phy_credit.video import build_label_info
from spb.exceptions import (
    NotSupportedException,
)
from spb.labels.manager import LabelManager
from spb.users.user import User
from spb.utils import deprecated
from spb.labels.label import Tags
from spb.labels.serializer import LabelInfoBuildParams


class VideoDataHandle(object):
    _VIDEO_URL_LIFETIME_IN_SECONDS = 3600

    def __init__(self, data, project, credential=None):
        super().__init__()
        self.credential = credential
        self._data = data
        self._project = project
        self._info = None
        self._created = time.time()
        self._init_label_build_info()

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
                command=command,
                option=self._data,
                optional={"info": json.dumps(info)},
            )

    def _init_label_build_info(self):
        self._data.result = self._get_result()
        self._label_build_params = LabelInfoBuildParams(
            label_interface=self._project.label_interface,
            result=self._data.result,
            workapp=self._data.workapp,
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
    
    def get_review_status(self):
        return self._data.last_review_action

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

        return self.get_frame_url(idx)

    def get_frames(self):
        if self._is_expired_video_url():
            return None

        for url in self.get_frame_urls():
            yield url
    
    def get_tags(self):
        return [tag.name for tag in self._data.tags]

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
        self._label_build_params.init_objects()
        for label in labels:
            self._label_build_params.add_object(**label)
        info = self._label_build_params.build_info()
        self._info = info
        objects = []
        if "result" in info and "objects" in info["result"]:
            objects = info["result"]["objects"]
        # apply
        self._data.result = {
            **(self._data.result or {}),
            "objects": objects,
        }

    def get_object_labels(self):
        try:
            labels = self._label_build_params.get_objects()
        except:
            labels = []
        return labels

    def set_category_labels(self, label):
        self._label_build_params.set_categories(**label)
        info = self._label_build_params.build_info()
        self._info = info
        categories = {"properties": []}
        if "result" in info and "categories" in info["result"]:
            categories = info["result"]["categories"]
        # apply
        self._data.result = {
            **(self._data.result or {}),
            "categories": categories,
        }

    def get_category_labels(self):
        return self._label_build_params.get_categories()

    @deprecated("Use [update_info] or [update_tag]")
    def update_data(self):
        self._upload_to_suite(info={"tags": self._info["tags"]})
        with requests_retry_session() as session:
            write_response = session.put(
                self._data.info_write_presigned_url,
                data=json.dumps(self._info),
            )
        return True

    def update_info(self):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        self._data = manager.update_info(
            label=self._data, info_build_params=self._label_build_params
        )
        if self._label_build_params is not None:
            self._init_label_build_info()
        return self._data

    @deprecated("Use [update_tags].")
    def set_tags(self, tags: list = None):
        raise NotSupportedException("[ERROR] Video does not supported.")

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

    def update_assignee(self, assignee: Union[str, User]):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if isinstance(assignee, str):
            assignee = User(email=assignee)
        self._data = manager.update_assignee(
            label=self._data,
            assignee=assignee
        )
        return self._data

    def update_reviewer(self, reviewer: Union[str, User]):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )
        if isinstance(reviewer, str):
            reviewer = User(email=reviewer)
        self._data = manager.update_reviewer(
            label=self._data,
            reviewer=reviewer
        )
        return self._data
