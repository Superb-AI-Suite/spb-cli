import json
import re
from urllib.parse import urlparse


def attrs(obj):
    ''' Return attribute values dictionary for an object '''
    return dict(i for i in vars(obj).items() if i[0][0] != '_')


def copy_attrs(obj, remove=None):
    ''' Copy attribute values for an object '''
    if remove is None:
        remove = []
    return dict(i for i in attrs(obj).items() if i[0] not in remove)

def is_json(value):
    try:
        json.loads(value)
    except (ValueError, TypeError):
        return False
    return True


def is_data_url(value):
    pattern = re.compile("data:([\\w\\/\\+]+);(charset=[\\w-]+|base64).*,([a-zA-Z0-9+/]+={0,2})")
    return pattern.match(value)

def is_url(value):
    try:
        urlparse(value)
        return True
    except:
        return False
