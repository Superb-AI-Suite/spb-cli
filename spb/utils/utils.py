import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry


def requests_retry_session(
    retries=5,
    backoff_factor=0.5,
    status_forcelist=(500, 502, 504),
    session=None,
    allowed_methods=[
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS',
        'HEAD',
        'PATCH',
        'TRACE',
        'CONNECT'
    ]
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(allowed_methods),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def retrieve_file(*, url, file_path):
    folder, _ = os.path.split(file_path)
    if folder:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with requests_retry_session() as session:
        response = session.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    return file_path