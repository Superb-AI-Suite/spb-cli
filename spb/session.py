import os
import configparser
import requests
import json
import copy
import base64

from spb.command import Command
from spb.models.project import Project
from spb.exceptions.exceptions import APIException, SDKInitiationFailedException, AuthenticateFailedException, APILimitExceededException, APIUnknowException

class Session:
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com/graphql")
    headers = {
        'content-type': 'application/json',
        'cache-control': 'no-cache',
        'X-API-KEY': None,
        'Authorization': None
    }

    def __init__(self, profile=None, account_name=None, access_key=None):
        self.credential = None
        self._set_credential(
            profile=profile, account_name=account_name, access_key=access_key)

    def _set_credential(self, profile=None, account_name=None, access_key=None):
        if not profile and not account_name and not access_key:
            profile = 'default'

        if profile and not account_name and not access_key:
            credential_path = os.path.expanduser('~') + '/.spb/config'
            credential_path = credential_path.replace(os.sep, '/')

            # check exists credentials
            assert os.path.exists(credential_path), SDKInitiationFailedException(
                '** [ERROR] credentials file does not exists')
            config = self._read_config(credential_path=credential_path,
                                       profile=profile)  # get values from credential
            self.credential = config
        elif profile and account_name and access_key:
            # To make credential
            self.credential = {
                'account_name': account_name,
                'access_key': access_key
            }
        else:
            if account_name is None:
                raise SDKInitiationFailedException(
                    '** [ERROR] credential [account_name] does not exists')
            if access_key is None:
                raise SDKInitiationFailedException(
                    '** [ERROR] credential [access_key] does not exists')

            self.credential = {
                'account_name': account_name,
                'access_key': access_key,
            }
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

    def validate(self):
        # TODO(mjlee): 나중에 root에 validate url 이 새로 열릴 예정임
        data = {
            'query': '{projects{id}}',
            'variables': {}
        }
        data = json.dumps(data)
        try:
            response = requests.request(
                "POST", self.endpoint, data=data, headers=self.headers)
        except requests.exceptions.Timeout:
            raise APIException('Occurred Time out of this request')
        except requests.exceptions.RequestException:
            raise APIException('Network Error')
        except Exception:
            raise APIException('Unknown Error on requests')

        try:
            response = response.json()
        except:
            raise APIException(
                "Failed to parse response as JSON: %s", response.text)
        errors = response.get('errors', [])
        if 'message' in response and response.get('message', None) == 'Forbidden':
            return False
        elif 'message' in response and response.get('message', None) == 'Limit Exceeded':
            raise APILimitExceededException()
        elif 'message' in response:
            raise APIUnknowException(response.get('message', None))
        if errors:
            raise APIException(errors[0]['message'])
        if 'data' not in response:
            return False
        return True

    def execute(self, query):
        data = {
            'query': query,
            'variables': {}
        }
        data = json.dumps(data)
        try:
            response = requests.request(
                "POST", self.endpoint, data=data, headers=self.headers)
        except requests.exceptions.Timeout:
            raise APIException('Occurred Time out of this request')
        except requests.exceptions.RequestException:
            raise APIException('Network Error')
        except Exception:
            raise APIException('Unknown Error on requests')

        try:
            response = response.json()
        except:
            raise APIException(
                "Failed to parse response as JSON: %s", response.text)
        errors = response.get('errors', [])
        # TODO: Error Handling from Server
        if 'message' in response and response.get('message', None) == 'Forbidden':
            raise AuthenticateFailedException('Check your credentials')
        elif 'message' in response and response.get('message', None) == 'Limit Exceeded':
            raise APILimitExceededException()
        elif 'message' in response:
            raise APIUnknowException(response.get('message', None))
        if errors:
            raise APIException(errors[0]['message'])
        return response.get('data')

    def execute_mutation(self, model, query):
        data = self.execute(query)
        if data is None:
            return None
        json_datas = None
        json_datas = data[list(data.keys())[0]]
        if json_datas is None:
            raise APIException('Response doesnt have any data')
        if isinstance(json_datas, list):
            result = []
            for json in json_datas:
                temp = self._json_to_model(model=model, args=json)
                result.append(temp)
            return result
        else:
            return self._json_to_model(model=model, args=json_datas)

    def execute_query(self, model, query):
        data = self.execute(query)
        if data is None:
            return None
        json_datas = None
        json_datas = data[list(data.keys())[0]]
        if json_datas is None:
            raise APIException('Response doesnt have any data')
        if isinstance(json_datas['edges'], list):
            result = []
            for json in json_datas['edges']:
                temp = self._json_to_model(model=model, args=json)
                result.append(temp)
            if query.find('page') > -1 :
                return result, json_datas['count']
            else:
                return result
        else:
            if query.find('page') > -1 :
                return self._json_to_model(model=model, args=json_datas), json_datas['count']
            else:
                return self._json_to_model(model=model, args=json_datas)


    def _json_to_model(self, model, args):
        return model.res_to_model(args)
