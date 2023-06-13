import time
import spb
import json
import urllib
import os
import skimage.io

from spb.utils.utils import requests_retry_session
from spb.libs.phy_credit.phy_credit.video import build_label_info
from spb.exceptions import (
    NotSupportedException,
)



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
                command=command,
                option=self._data,
                optional={"info": json.dumps(info)},
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
                self._data.info_write_presigned_url,
                data=json.dumps(self._info),
            )
        return True

    def get_tags(self):
        return [tag.name for tag in self._data.tags]

    def set_tags(self, tags: list = None):
        raise NotSupportedException("[ERROR] Video does not supported.")