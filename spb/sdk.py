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

import spb
import math
import time
import urllib
import os, random
import skimage.io
import boto3
import json
import glob
import requests
import logging

from natsort import natsorted
from spb.labels import Label
from spb.projects import Project
from spb.libs.phy_credit.phy_credit.video import build_label_info
from spb.labels.manager import LabelManager
from spb.projects.manager import ProjectManager
from spb.labels.label import Tags, WorkappType
from spb.labels.serializer import LabelInfoBuildParams

logger = logging.getLogger()

__author__ = spb.__author__
__version__ = spb.__version__

__all__ = ('Client', 'DataHandle', 'VideoDataHandle')


class Client(object):
    def __init__(self, project_name=None, team_name: str = None, access_key: str = None):
        super().__init__()

        if team_name is not None and access_key is not None:
            print(f'[INFO] Usage: Client has been started with {team_name}')
            spb.setup_default_session(team_name = team_name, access_key = access_key)

        if project_name is None:
            print('[WARNING] Client cannot be used to describe label without project')
            self._project = None
        else:
            self._project = Client.get_project(project_name)
        self._s3 = boto3.client('s3')

    ##############################
    # Immutable variables
    ##############################

    def get_project_name(self):
        if self._project is None:
            print('[WARNING] Project is not described')
            return None
        return self._project.name

    ##############################
    # Constructor
    ##############################

    @classmethod
    def get_project(cls, name):
        manager = ProjectManager()
        project = manager.get_project(name=name)
        if project is None:
            print('[WARNING] Project {} not found'.format(name))
            return None

        return project

    @classmethod
    def get_projects(cls, page: int = 1, page_size: int = 10):
        manager = ProjectManager()
        count, projects = manager.get_project_list(page = page, page_size = page_size)
        return (count, projects)

    def set_project(self, project: Project):
        self._project = project

    @property
    def project(self):
        if self._project is None:
            print('[WARNING] Project is not described')
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
            print('[WARNING] Project is not described')
            return None

        manager = LabelManager()
        tags = [{'name': tag} for tag in tags]
        option = {'project_id': self._project.id, 'tags': tags, **kwargs}
        num_data = manager.get_labels_count(**option)

        if num_data == 0:
            print('[WARNING] Data list is empty')

        return num_data

    def get_data_page(self, page_idx, page_size=10, num_data=None, tags=[], dataset=None, data_key=None, **kwargs):
        if self._project is None:
            print('[WARNING] Project is not described')
            return None

        if num_data is None:
            num_data = self.get_num_data(tags=tags, **kwargs)

        num_pages = math.ceil(float(num_data) / page_size)
        if page_idx >= num_pages:
            print('[WARNING] Index out of bounds. Empty list returned')
            return []

        workapp = self._project.workapp
        if workapp == 'video-siesta':
            # Video
            command = spb.Command(type='describe_videolabel')
            tags = [{'name': tag} for tag in tags]
            option = {'project_id': self._project.id, 'tags': tags, **kwargs}
            data_page, _ = spb.run(command=command, option=option, page=page_idx+1, page_size=page_size)
            for data in data_page:
                yield VideoDataHandle(data, self._project)
        else:
            manager = LabelManager()
            tags = [{'name': tag} for tag in tags]
            option = {
                'project_id': self._project.id,
                'tags': tags,
                'page':page_idx+1,
                'page_size': page_size,
                'dataset': dataset,
                'data_key': data_key,
                **kwargs
            }
            count, data_page = manager.get_labels(**option)
            for data in data_page:
                yield DataHandle(data, self._project)

    def upload_image(self, path, dataset_name, key=None, name=None):
        if self._project is None:
            print('[WARNING] Project is not described')
            return
        if not os.path.isfile(path):
            print('[WARNING] Invalid path. Upload failed')
            return

        if name is None:
            name = path.split('/')[-1]

        if key is None:
            key = name

        command = spb.Command(type='create_data')
        option = {'file': path, 'file_name': name, 'dataset': dataset_name, 'data_key': key}

        try:
            return spb.run(command=command, optional={'projectId': self._project.id}, option=option)

        except Exception as e:
            print('[WARNING] Duplicate data key. Upload failed')

    def upload_image_s3(self, bucket_name, path, dataset_name, key=None):
        if self._project is None:
            print('[WARNING] Project is not described')
            return

        name = path.split('/')[-1]
        ext = path.split('.')[-1]
        temp_path = '{:032x}.{}'.format(random.getrandbits(128), ext)

        try:
            self._s3.download_file(bucket_name, path, temp_path)
            return self.upload_image(temp_path, dataset_name, key, name=name)

        except Exception as e:
            print('[WARNING] Cannot access S3 path. Check your access permission. Upload failed')

        finally:
            if os.path.isfile(temp_path):
                os.remove(temp_path)

    def upload_video(self, path, dataset_name, key=None):
        if self._project is None:
            print('[WARNING] Project is not described')
            return

        if not os.path.isdir(path):
            print('[WARNING] Invalid path. Upload failed')
            return

        # TODO: support_img_format is const
        support_img_format = ('png', 'jpg', 'bmp', 'jpeg', 'tiff', 'tif')
        file_names = [os.path.basename(file_path) for file_path in glob.glob(os.path.join(path, '*')) if file_path.lower().endswith(support_img_format)]
        if len(file_names) == 0:
            print('[WARNING] Invalid path. Upload failed')
            return

        if key is None:
            key = os.path.split(path)[-1]

        asset_video = {
            'dataset': dataset_name,
            'data_key': key,
            'files': {
                'path': path,
                'file_names': natsorted(file_names),
            },
        }

        try:
            command = spb.Command(type='create_videodata')
            result = spb.run(command=command, option=asset_video, optional={'projectId': self._project.id})
            file_infos = json.loads(result.file_infos)
            for file_info in file_infos:
                file_name = file_info['file_name']
                file_path = os.path.join(path, file_name)
                data = open(file_path,'rb').read()
                response = requests.put(file_info['presigned_url'], data=data)
        except Exception as e:
            print('[WARNING] Duplicate data key. Upload failed')


class DataHandle(object):
    _IMAGE_URL_LIFETIME_IN_SECONDS = 3600

    def __init__(self, data, project):
        super().__init__()

        manager = LabelManager()
        if data.project_id is None or data.id is None:
            print('[ERROR] Data Handler cannot be initiated.')
            return
        self._data = data
        self._project = project
        self._created = time.time()

        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            self._init_label_build_info()

    def _init_label_build_info(self):
        self._label_build_params = LabelInfoBuildParams(
            label_interface = self._project.label_interface,
            result = self._data.result
        )

    def _is_expired_image_url(self):
        global _IMAGE_URL_LIFETIME

        is_expired = time.time() - self._created > DataHandle._IMAGE_URL_LIFETIME_IN_SECONDS

        if is_expired:
            print('[WARNING] Image URL has been expired. Call get_data(...) of SuiteProject to renew URL')

        return is_expired

    ##############################
    # Immutable variables
    ##############################

    def get_key(self):
        return self._data.data_key

    def get_dataset_name(self):
        return self._data.dataset

    def get_status(self):
        return self._data.status

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
            print('[INFO] Downloaded to {}'.format(download_to))

        return urllib.request.urlretrieve(self._data.data_url, download_to)

    def get_image(self):
        if self._is_expired_image_url():
            return None

        return skimage.io.imread(self._data.data_url)

    def get_category_labels(self):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            return self._label_build_params.get_categories()
        else:
            category_map = self._project.label_interface['categorization']['word_map']
            id_to_name = {c['id']: c['name'] for c in category_map if c['id'] != 'root'}

            try:
                labels = [id_to_name[id] for id in self._data.result['categorization']['value']]
            except:
                # The given image does not have any image categorizations
                labels = []

            return labels

    def get_object_labels(self):
        try:
            if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
                labels = self._label_build_params.get_objects()
            else:
                labels = self._data.result.get('objects', [])
        except:
            # The given image does not have any object annotations
            labels = []

        return labels

    def get_tags(self):
        return [tag.name for tag in self._data.tags]

    def set_category_labels(self, labels:list = None, category:dict = None, properties = None):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            # build new info
            self._label_build_params.set_categories(properties=properties)
            info = self._label_build_params.build_info()
            categories = {'properties': []}
            if 'result' in info and 'categories' in info['result']:
                categories = info['result']['categories']
            # apply
            self._data.result = {
                **(self._data.result or {}),
                'categories': categories,
            }
        else:
            category_map = self._project.label_interface['categorization']['word_map']
            name_to_id = {c['name']: c['id'] for c in category_map if c['id'] != 'root'}

            try:
                label_ids = [name_to_id[name] for name in labels]
            except KeyError:
                print('[WARNING] Invalid category name exists')
                return

            if not self._data.result:
                self._data.result = {}
            if 'objects' not in self._data.result:
                self._data.result['objects'] = []
            self._data.result = {**self._data.result, 'categorization': {'value': label_ids}}

    def set_object_labels(self, labels):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            # build new info
            self._label_build_params.init_objects()
            for label in labels:
                self._label_build_params.add_object(**label)
            info = self._label_build_params.build_info()
            objects = []
            if 'result' in info and 'objects' in info['result']:
                objects = info['result']['objects']
            # apply
            self._data.result = {
                **(self._data.result or {}),
                'objects': objects,
            }
        else:
            if not self._data.result:
                self._data.result = {}
            if 'categorization' not in self._data.result:
                self._data.result['categorization'] = {'value': []}
            self._data.result = {**self._data.result, 'objects': labels}

    def add_object_label(self, class_name, annotation, properties=None, id=None):
        if self._data.workapp == WorkappType.IMAGE_SIESTA.value:
            self._label_build_params.add_object(class_name, annotation, properties, id)
        elif self._data.workapp == WorkappType.IMAGE_DEFAULT.value:
            print('[ERROR] add_object_list doesn\'t support.')

    def update_data(self):
        manager = LabelManager()
        build_params = self._label_build_params if self._data.workapp == WorkappType.IMAGE_SIESTA.value else None
        self._data = manager.update_label(label=self._data, info_build_params=build_params)
        if build_params is not None:
            self._init_label_build_info()

    def set_tags(self, tags: list = None):
        label_tags = []
        if tags is not None and isinstance(tags, list):
            for tag in tags:
                label_tags.append(Tags(name=tag))

        self._data.tags = label_tags


class VideoDataHandle(object):
    _VIDEO_URL_LIFETIME_IN_SECONDS = 3600

    def __init__(self, data, project):
        super().__init__()

        self._data = data
        self._project = project
        self._created = time.time()

    def _is_expired_video_url(self):
        is_expired = time.time() - self._created > self._VIDEO_URL_LIFETIME_IN_SECONDS

        if is_expired:
            print('[WARNING] Video URL has been expired. Call get_data(...) of SuiteProject to renew URL')

        return is_expired

    def _upload_to_suite(self, info=None):
        command = spb.Command(type='update_videolabel')
        if info is None:
            _ = spb.run(command=command, option=self._data)
        else:
            _ = spb.run(command=command, option=self._data, optional={'info': json.dumps(info)})

    ##############################
    # Immutable variables
    ##############################

    def get_key(self):
        return self._data.data_key

    def get_dataset_name(self):
        return self._data.dataset

    def get_status(self):
        return self._data.status

    def get_frame_url(self, idx, data_url=None):
        if self._is_expired_video_url():
            return None

        if data_url is None:
            data_url = json.loads(self._data.data_url)
        file_info = data_url['file_infos'][idx]
        return f"{data_url['base_url']}{file_info['file_name']}?{data_url['query']}"

    def get_frame_urls(self):
        if self._is_expired_video_url():
            return None

        data_url = json.loads(self._data.data_url)
        for frame_idx in range(len(data_url['file_infos'])):
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
            print('[INFO] Downloaded to {}'.format(download_to))

        data_url = json.loads(self._data.data_url)
        for frame_idx, file_info in enumerate(data_url['file_infos']):
            url = self.get_frame_url(frame_idx, data_url)
            urllib.request.urlretrieve(url, os.path.join(download_to, file_info['file_name']))

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
            read_response = requests.get(self._data.info_read_presigned_url)
            label_result = read_response.json()
            return label_result['result']
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

        self._upload_to_suite(info={'tags': info['tags']})
        write_response = requests.put(self._data.info_write_presigned_url, data=json.dumps(info))

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

        self._upload_to_suite(info={'tags': info['tags']})
        write_response = requests.put(self._data.info_write_presigned_url, data=json.dumps(info))

    def get_category_labels(self):
        result = self._get_result()
        if result is None:
            return None
        label_info = build_label_info(self._project.label_interface, result=result)
        return label_info.get_categories()

    def get_tags(self):
        return [tag.name for tag in self._data.tags]
