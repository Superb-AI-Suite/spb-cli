import os
import json
from spb.orm import Model
from spb.orm.type import String, ID, List


class VideoData(Model):
    MODEL_UUID = '4806131c-eeb2-4e90-a5bf-86e12e6cb1da'
    RESOURCE_NAME = 'video_asset'

    id = ID(property_name='id', immutable=True, filterable=True)
    file_infos = String(property_name='fileInfos')
    dataset = String(property_name='dataset')
    data_key = String(property_name='dataKey')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 1 and isinstance(args[0], dict):
            # if args has dict in first row of args -> kwargs
            kwargs = args[0]
        if 'files' in kwargs:
            setattr(self, 'file_infos', kwargs['files'])

    def __setattr__(self, name, value):
        if name is 'file_infos':
            file_infos = []
            path = value['path']
            file_names = value['file_names']
            for file_name in file_names:
                file_path = F'{path}/{file_name}'
                file_contents = None
                file_size = None
                if file_path is None:
                    pass
                elif os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    file_name = os.path.basename(file_path)
                    file_info = {
                        'fileName': file_name,
                        'fileSize': file_size
                    }
                    file_infos.append(file_info)
            file_infos_string = json.dumps(file_infos).replace('"', '\\"') # Must escape double quotes
            super().__setattr__('file_infos', file_infos_string)
        else:
            super().__setattr__(name, value)
