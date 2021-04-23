import os
import configparser
import requests
import json
import base64

from collections import deque
from spb.exceptions import APIException, SDKInitiationFailedException, AuthenticateFailedException, APILimitExceededException, APIUnknownException, NotFoundException


class BaseSession:
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com/graphql")
    headers = {
        'content-type': 'application/json',
        'cache-control': 'no-cache',
        'X-API-KEY': None,
        'Authorization': None
    }
    history = deque(10*['EMPTY'], 10)

    def __init__(self, profile='default', account_name=None, access_key=None):
        self.credential = None
        self._set_credential(profile, account_name, access_key)

    def _set_credential(self, profile='default', account_name=None, access_key=None):

        if account_name and access_key:
            # To make credential
            self.credential = {
                'account_name': account_name,
                'access_key': access_key
            }
        elif not account_name or not access_key:
            credential_path = os.path.join(os.path.expanduser('~'), '.spb', 'config')

            # check exists credentials
            if not os.path.exists(credential_path):
                raise SDKInitiationFailedException('** [ERROR] credentials file does not exists')
            config = self._read_config(credential_path=credential_path,
                                       profile=profile)  # get values from credential
            self.credential = config

        self.headers['X-API-KEY'] = self.credential['access_key']
        authorization_string = base64.b64encode(f'{self.credential["account_name"]}:{self.credential["access_key"]}'.encode("UTF-8"))
        self.headers['Authorization'] = f'Basic {authorization_string.decode("UTF-8")}'

    def _read_config(self, credential_path, profile):
        config = configparser.ConfigParser()
        config.read(credential_path)
        ret = {}
        vars = ['account_name', 'access_key']
        for var in vars:
            try:
                ret[var] = config.get(profile, var)
            except (configparser.NoSectionError, configparser.NoOptionError):
                raise SDKInitiationFailedException(
                    '** [ERROR] credential - key [{0}] does not exists'.format(var))
        return ret

    def check_session(self):
        try:
            response = self.execute('{projects{edges{id}}}')
        except Exception:
            return False

        if not 'data' in response.json():
            return False
        else:
            return True

    def execute(self, query: str, values: dict = {}):
        data = {
            'query': query,
            'variables': values
        }
        request_param = json.dumps(data)
        try:
            response = requests.post(self.endpoint, data=request_param, headers=self.headers)
        except requests.exceptions.HTTPError as e:
            self.history.appendleft({'APIException': data})
            raise APIException(f'HTTP Error: {repr(e)}')
        except requests.exceptions.Timeout as e:
            self.history.appendleft({'APIException': data})
            raise APIException(f'Request Time Out Exception: {repr(e)}')
        except requests.exceptions.ConnectionError as e:
            self.history.appendleft({'APIException': data})
            raise APIException(f'Network Connection Error: {repr(e)}')
        result = response.json()

        if isinstance(result, dict) and len(result.keys()) == 0:
            self.history.appendleft({'APIException': data})
            raise APIException(f'HTTP Error: Empty contents')

        if 'error' in result:
            error = result['error']
            if error['message'] == 'Forbidden':
                self.history.appendleft({'AuthenticateFailedException': data})
                raise AuthenticateFailedException('Authencation Failed Exception : Check your credentials')
            elif error['message'] == 'Limit Exceeded':
                self.history.appendleft({'AuthenticateFailedException': data})
                raise APILimitExceededException('Limit Exceeded Exception : API request limit exceeded')

        if 'errors' in result:
            errors = result['errors']
            for error in errors:
                if error['message'] == 'Request failed with status code 404':
                    self.history.appendleft({'NotFoundException': data})
                    raise NotFoundException('Not Found Exception: Open API returns not found exception with status code 404')

        self.history.appendleft({
            'success': data
        })
        return response
