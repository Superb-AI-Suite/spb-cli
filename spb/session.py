import os
import configparser
import requests
import json
import copy
import base64

from spb.command import Command
from spb.models.project import Project
from spb.exceptions import APIException, SDKInitiationFailedException, AuthenticateFailedException, APILimitExceededException, APIUnknownException

class Session:
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com/graphql")
    headers = {
        'content-type': 'application/json',
        'cache-control': 'no-cache',
        'X-API-KEY': None,
        'Authorization': None
    }

    def __init__(self, profile=None, team_name=None, access_key=None):
        self.credential = None
        self._set_credential(
            profile=profile, team_name=team_name, access_key=access_key)

    def _set_credential(self, profile=None, team_name=None, access_key=None):
        if not profile and not team_name and not access_key:
            profile = 'default'
        self.headers = None
        if team_name and access_key:
            # 1st priority
            self.credential = {
                'team_name': team_name,
                'access_key': access_key
            }
        elif os.getenv("SPB_ACCESS_KEY", None) and os.getenv("SPB_TEAM_NAME", None):
            # 2nd priority
            self.credential = {
                'team_name': os.getenv("SPB_TEAM_NAME"),
                'access_key': os.getenv("SPB_ACCESS_KEY")
            }
        elif profile and not team_name and not access_key:
            # 3rd
            credential_path = os.path.join(os.path.expanduser('~'), '.spb', 'config')
            # check exists credentials
            if not os.path.exists(credential_path):
                self.credential = None
                return
            config = self._read_config(credential_path=credential_path,
                                       profile=profile)  # get values from credential
            self.credential = config
        else:
            # To raise SDKInitiationFailedException error
            raise SDKInitiationFailedException('** [ERROR] credential does not exists')

    def _set_headers(self):
        if self.headers is None and self.credential is not None:
            if self.credential['team_name'] is None:
                raise SDKInitiationFailedException(
                    '** [ERROR] credential [team_name] does not exists')
            if self.credential['access_key'] is None:
                raise SDKInitiationFailedException(
                    '** [ERROR] credential [access_key] does not exists')

            self.headers = dict()
            self.headers['X-API-KEY'] = self.credential['access_key']
            authorization_string = base64.b64encode(f'{self.credential["team_name"]}:{self.credential["access_key"]}'.encode("UTF-8"))
            self.headers['Authorization'] = f'Basic {authorization_string.decode("UTF-8")}'
        elif self.headers is not None:
            return
        else:
            raise SDKInitiationFailedException('** [ERROR] credential does not exists.')

    def _read_config(self, credential_path, profile):
        config = configparser.ConfigParser()
        config.read(credential_path)
        ret = {}
        vars = ['team_name', 'access_key']
        for var in vars:
            try:
                ret[var] = config.get(profile, var)
            except (configparser.NoSectionError, configparser.NoOptionError):
                ret = None
                break
        if ret is not None:
            return ret

        ret = {}
        vars = ['access_key', 'account_name']
        for var in vars:
            try:
                ret['team_name' if var == 'account_name' else var] = config.get(profile, var)
            except (configparser.NoSectionError, configparser.NoOptionError):
                return None
                break

        return ret

    def validate(self):
        # TODO(mjlee): 나중에 root에 validate url 이 새로 열릴 예정임
        self._set_headers()
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
            raise APIUnknownException(response.get('message', None))
        if errors:
            raise APIException(errors[0]['message'])
        if 'data' not in response:
            return False
        return True

    def execute(self, query):
        self._set_headers()
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
            raise APIUnknownException(response.get('message', None))
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
        try:
            return model.res_to_model(args)
        except Exception as e:
            raise Exception(e)
