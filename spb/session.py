import base64
import configparser
import json
import os

import requests

from spb.exceptions import (APIException, APILimitExceededException,
                            APIUnknownException, AuthenticateFailedException,
                            BadRequestException, ConflictException,
                            ForbiddenException, NotAvailableServerException,
                            NotFoundException, SDKInitiationFailedException,
                            UnauthorizedException)
from spb.models.project import Project
from spb.utils.utils import requests_retry_session


class Session:
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com") + '/graphql'
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
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise UnauthorizedException("Unauthorized Exception")
            elif response.status_code == 403:
                raise ForbiddenException("Forbidden Exception")
            raise APIException(f"HTTP Error: {repr(e)}")
        except requests.exceptions.Timeout as e:
            raise APIException(f"Request Time Out Exception: {repr(e)}")
        except requests.exceptions.ConnectionError as e:
            raise APIException(f"Network Connection Error: {repr(e)}")
        except Exception as e:
            raise APIUnknownException(
                "Unknown Error Exception: Check your API response"
            )

        result = response.json()

        if isinstance(result, dict) and len(result.keys()) == 0:
            self.history.appendleft({"APIException": data})
            raise APIException(f"HTTP Error: Empty contents")

        if "error" in result:
            error = result["error"]
            if error["message"] == "Forbidden":
                raise AuthenticateFailedException(
                    "Authentication Failed Exception : Check your credentials"
                )
            elif error["message"] == "Limit Exceeded":
                raise APILimitExceededException(
                    "Limit Exceeded Exception : API request limit exceeded"
                )

        if "errors" in result:
            errors = result["errors"]
            for error in errors:
                if error["extensions"]["code"] == "INTERNAL_SERVER_ERROR":
                    raise APIUnknownException(
                        "Unknown Error Exception: Check your API response"
                    )
                elif int(error["extensions"]["code"]) == 400:
                    raise BadRequestException("Bad Request Exception")
                elif int(error["extensions"]["code"]) == 401:
                    raise UnauthorizedException("Unauthorized Exception")
                elif int(error["extensions"]["code"]) == 403:
                    raise ForbiddenException("Forbidden Exception")
                elif error["message"] == "Request failed with status code 404" or int(
                    error["extensions"]["code"] == 404
                ):
                    raise NotFoundException(
                        "Not Found Exception: Open API returns not found exception with status code 404"
                    )
                elif int(error["extensions"]["code"]) == 409:
                    raise ConflictException("Conflict Exception")
                elif (
                    error["message"] == "Not Available Server"
                    or int(error["extensions"]["code"]) == 503
                ):
                    raise NotAvailableServerException(
                        "Not Available Server Exception: Not connected to the server"
                    )
                else:
                    raise APIUnknownException(
                        "Unknown Error Exception: Check your API response"
                    )
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
            with requests_retry_session() as session:
                response = session.request(
                    "POST", self.endpoint, data=data, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise UnauthorizedException("Unauthorized Exception")
            elif response.status_code == 403:
                raise ForbiddenException("Forbidden Exception")
            raise APIException(f"HTTP Error: {repr(e)}")
        except requests.exceptions.Timeout as e:
            raise APIException(f"Request Time Out Exception: {repr(e)}")
        except requests.exceptions.ConnectionError as e:
            raise APIException(f"Network Connection Error: {repr(e)}")
        except Exception as e:
            raise APIUnknownException(
                "Unknown Error Exception: Check your API response"
            )

        result = response.json()

        if isinstance(result, dict) and len(result.keys()) == 0:
            self.history.appendleft({"APIException": data})
            raise APIException(f"HTTP Error: Empty contents")

        if "error" in result:
            error = result["error"]
            if error["message"] == "Forbidden":
                raise AuthenticateFailedException(
                    "Authentication Failed Exception : Check your credentials"
                )
            elif error["message"] == "Limit Exceeded":
                raise APILimitExceededException(
                    "Limit Exceeded Exception : API request limit exceeded"
                )

        if "errors" in result:
            errors = result["errors"]
            for error in errors:
                if error["extensions"]["code"] == "INTERNAL_SERVER_ERROR":
                    raise APIUnknownException(
                        "Unknown Error Exception: Check your API response"
                    )
                elif int(error["extensions"]["code"]) == 400:
                    raise BadRequestException("Bad Request Exception")
                elif int(error["extensions"]["code"]) == 401:
                    raise UnauthorizedException("Unauthorized Exception")
                elif int(error["extensions"]["code"]) == 403:
                    raise ForbiddenException("Forbidden Exception")
                elif error["message"] == "Request failed with status code 404" or int(
                    error["extensions"]["code"] == 404
                ):
                    raise NotFoundException(
                        "Not Found Exception: Open API returns not found exception with status code 404"
                    )
                elif int(error["extensions"]["code"]) == 409:
                    raise ConflictException("Conflict Exception")
                elif (
                    error["message"] == "Not Available Server"
                    or int(error["extensions"]["code"]) == 503
                ):
                    raise NotAvailableServerException(
                        "Not Available Server Exception: Not connected to the server"
                    )
                else:
                    raise APIUnknownException(
                        "Unknown Error Exception: Check your API response"
                    )
                    
        return result.get('data')

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
