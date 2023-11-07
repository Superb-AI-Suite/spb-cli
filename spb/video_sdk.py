import spb
import json
import urllib
import os

from spb.image_sdk import DataHandle
from spb.utils.utils import requests_retry_session
from spb.exceptions import (
    NotSupportedException,
)
from spb.utils import deprecated


class VideoDataHandle(DataHandle):
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
    def get_image_url(self):
        raise NotSupportedException("The video data does not support get_image_url.")

    def get_frame_url(self, idx, data_url=None):
        self._describe_data_detail()
        if self._is_expired_url():
            return None

        if data_url is None:
            data_url = json.loads(self._data.data_url)

        file_ext = data_url["file_infos"][idx]["file_name"].split(".")[-1].lower()
        file_name = f"image_{(idx+1):08}.{file_ext}"
        return f"{data_url['base_url']}{file_name}?{data_url['query']}"

    def get_frame_urls(self):
        self._describe_data_detail()
        if self._is_expired_url():
            return None
        if self._data.data_url is None:
            return None

        data_url = json.loads(self._data.data_url)
        for frame_idx in range(len(data_url["file_infos"])):
            yield self.get_frame_url(frame_idx, data_url)

    def get_frame(self, idx):
        return self.get_frame_url(idx)

    ##############################
    # Simple SDK functions
    ##############################

    def download_image(self, download_to=None):
        raise NotSupportedException(
            "Does not support download label image."
        )

    def get_image(self):
        raise NotSupportedException(
            "Does not support describe label image."
        )

    def download_video(self, download_to=None):
        self._describe_data_detail()
        if self._is_expired_url():
            return None
        if self._data.data_url is None:
            return None

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

    def get_frames(self):
        for url in self.get_frame_urls():
            yield url

    def add_object_label(self, class_name, annotation, properties=None, id=None):
        raise NotSupportedException("Does not support add_object_label. Use set_object_labels instead.")

    @deprecated("Use [update_info] or [update_tag]")
    def update_data(self):
        self._upload_to_suite(info={"tags": self._data.get("result", {})["tags"]})
        with requests_retry_session() as session:
            _ = session.put(
                self._data.info_write_presigned_url,
                data=json.dumps(self._data.result),
            )
        self.label_id_only = False
        return True

    @deprecated("Use [update_tags].")
    def set_tags(self, tags: list = None):
        raise NotSupportedException("[ERROR] Video does not supported.")
