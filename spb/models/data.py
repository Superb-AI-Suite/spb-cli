import os
import requests
import base64
from spb.datauri import DataURI
from spb.orm import Model
from spb.orm.utils import is_data_url, is_url
from spb.orm.type import String, ID, Number


class Data(Model):
    MODEL_UUID = '0a8bb642-958b-11ea-bb37-0242ac130002'
    RESOURCE_NAME = 'asset'

    id = ID(property_name='id', immutable=True, filterable=True)
    file = String(property_name='file')
    file_name = String(property_name='fileName')
    file_size = Number(property_name='fileSize')
    dataset = String(property_name='dataset')
    data_key = String(property_name='dataKey')
    presigned_url = String(property_name='presignedURL')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 1 and isinstance(args[0], dict):
            # if args has dict in first row of args -> kwargs
            kwargs = args[0]
        if 'file' in kwargs:
            setattr(self, 'file', kwargs['file'])

    def __setattr__(self, name, value):
        if name == 'file':
            file_contents = None
            file_size = None
            if value is None:
                pass
            elif os.path.exists(value):
                file_size = os.path.getsize(value)
                file_name = os.path.basename(value)
                # file_contents = DataURI.from_file(value)
                # file_contents = file_contents.replace('\n', '') # I don't know why
                # file_contents가 Null이면 S3 url 반환 / None이 아니면 Data 직접 전송
                file_contents = ""
                super().__setattr__('file_name', file_name)
            elif is_data_url(value):
                #TODO
                file_contents = DataURI(value)
                file_size = 0
            elif is_url(value):
                reshead = requests.head(value)
                response = requests.get(value)
                content_type = response.headers["content-type"]
                encoded_body = base64.b64encode(response.content)
                file_size = reshead.headers['Content-length']
                # file_contents = f"data:{content_type};base64,{encoded_body.decode()}"
                file_contents = ""
            super().__setattr__('file_size', file_size)
            super().__setattr__('file', file_contents)
        else:
            super().__setattr__(name, value)




