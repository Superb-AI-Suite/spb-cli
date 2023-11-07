import urllib
import json
import os

from spb.image_sdk import DataHandle
from spb.labels.manager import LabelManager
from spb.exceptions import (
    ParameterException,
    NotSupportedException,
    SDKException
)
from spb.utils import deprecated


class PointcloudDataHandle (DataHandle):

    def get_image_url(self):
        raise NotSupportedException("")

    def download_image(self, download_to=None):
        raise NotSupportedException("")

    def get_image(self):
        raise NotSupportedException("")

    def get_category_labels(self):
        raise NotSupportedException("Does not support describe label category.")

    def set_category_labels(self, labels: list = None, category: dict = None, properties=None):
        raise NotSupportedException("Does not support update label result.")

    def set_object_labels(self, labels):
        raise NotSupportedException("Does not support update label result.")

    def add_object_label(self, class_name, annotation, properties=None, id=None):
        raise NotSupportedException("Does not support update label result.")

    def get_data_urls(self):
        self._describe_data_detail()
        if self._is_expired_url():
            return None
        if self._data.data_url is None:
            return None

        data_urls = json.loads(self._data.data_url)
        frames = data_urls.get("frame_infos", [])
        url = data_urls["base_url"]
        query = data_urls["query"]

        result = {
            "manifest_url": f"{url}manifest.json?{query}",
            "manifest_original_file_name": data_urls["manifest_file"],
            "frames": []
        }

        frame_path_prefix = "frames/frame_"
        for i, frame in enumerate(frames):
            index = str(i+1).zfill(8)
            frame_urls = {
                "frame_url": f"{url}{frame_path_prefix}{index}/frame_{index}.pcd?{query}",
                "frame_original_file_name": frame.get("frame_file_name", None),
                "images": []
            }
            images = frame.get("image_infos", [])
            for k, image in enumerate(images):
                image_index = str(k+1).zfill(8)
                frame_urls["images"].append(
                    {
                        "image_url": f"{url}{frame_path_prefix}{index}/image_{index}_{image_index}.png?{query}",
                        "image_original_file_name": image.get("image_file_name", None)
                    }
                )
            result["frames"].append(frame_urls)
        return result
    
    def download_data(self, download_to="./"):
        self._describe_data_detail()
        # Validation
        if download_to is None:
            raise ParameterException("[ERROR] download_to must been specified.")
        
        data_urls = self.get_data_urls()
        if data_urls is None:
            raise SDKException("[ERROR] Unknown Error. Cannot build data download urls.")
        # Download manifest file
        urllib.request.urlretrieve(data_urls["manifest_url"], os.path.join(download_to, data_urls["manifest_original_file_name"]))

        for frame in data_urls["frames"]:
            urllib.request.urlretrieve(frame["frame_url"], os.path.join(download_to, frame["frame_original_file_name"]))
            for image in frame["images"]:
                urllib.request.urlretrieve(image["image_url"], os.path.join(download_to, image["image_original_file_name"]))

        return True
    
    def get_object_labels(self):
        self._describe_data_detail()
        if self._is_expired_url():
            return None
        
        info_url = self.data.info_read_presigned_url
        if info_url is None:
            return None
        
        webURL = urllib.request.urlopen(info_url)
        data = webURL.read()
        encoding = webURL.info().get_content_charset("utf-8")

        return json.loads(data.decode(encoding))

    def download_object_labels(self, download_to, indent=None):
        self._describe_data_detail()
        if not isinstance(download_to, str):
            raise ParameterException("[ERROR] 'download_to' must be a string.")
        labels = self.get_object_labels()
        if labels is None:
            raise SDKException("[ERROR] Unknown Error. Object labels loading failed.")
        
        with open(download_to, 'w') as file:
            file.write(json.dumps(labels, indent=indent))

    @deprecated("Use [update_tags].")
    def update_data(self):
        manager = LabelManager(
            self.credential["team_name"], self.credential["access_key"]
        )

        self._data = manager.update_label(label=self._data)
        self.label_id_only = False
        return True

    def update_info(self):
        raise NotSupportedException("Does not support update info.")
