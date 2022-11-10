import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry


def requests_retry_session(retries=3,
                           backoff_factor=0.5,
                           status_forcelist=(408, 413, 429, 500, 502, 503, 504),
                           session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session