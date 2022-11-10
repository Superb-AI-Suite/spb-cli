import base64
import configparser
import json
import logging
import os
from collections import deque

import requests
from spb.core.models.attrs import AttributeEncoder
from spb.exceptions import (
    APIException,
    APILimitExceededException,
    APIUnknownException,
    AuthenticateFailedException,
    BadRequestException,
    ConflictException,
    ForbiddenException,
    NotAvailableServerException,
    NotFoundException,
    SDKInitiationFailedException,
    UnauthorizedException,
)
from spb.utils.utils import requests_retry_session

logger = logging.getLogger()


class BaseSession:
    endpoint = (
        os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com") + "/graphql"
    )
    headers = {
        "content-type": "application/json",
        "cache-control": "no-cache",
        "X-API-KEY": None,
        "Authorization": None,
    }
    history = deque(10 * ["EMPTY"], 10)

    def __init__(self, profile="default", team_name=None, access_key=None):
        self.credential = None
        self._set_credential(profile, team_name, access_key)

    def _set_credential(self, profile="default", team_name=None, access_key=None):
        if not profile and not team_name and not access_key:
            profile = "default"
        self.headers = None
        if team_name and access_key:
            # 1st priority
            self.credential = {"team_name": team_name, "access_key": access_key}
        elif os.getenv("SPB_ACCESS_KEY", None) and os.getenv("SPB_TEAM_NAME", None):
            # 2nd priority
            self.credential = {
                "team_name": os.getenv("SPB_TEAM_NAME"),
                "access_key": os.getenv("SPB_ACCESS_KEY"),
            }
        elif profile and not team_name and not access_key:
            # 3rd
            credential_path = os.path.join(os.path.expanduser("~"), ".spb", "config")
            # check exists credentials
            if not os.path.exists(credential_path):
                self.credential = None
                return
            config = self._read_config(
                credential_path=credential_path, profile=profile
            )  # get values from credential
            self.credential = config
        else:
            # To raise SDKInitiationFailedException error
            raise SDKInitiationFailedException("** [ERROR] credential does not exists")

    def _set_headers(self):
        if self.headers is None and self.credential is not None:
            if self.credential["team_name"] is None:
                raise SDKInitiationFailedException(
                    "** [ERROR] credential [team_name] does not exists"
                )
            if self.credential["access_key"] is None:
                raise SDKInitiationFailedException(
                    "** [ERROR] credential [access_key] does not exists"
                )

            self.headers = dict()
            self.headers["X-API-KEY"] = self.credential["access_key"]
            authorization_string = base64.b64encode(
                f'{self.credential["team_name"]}:{self.credential["access_key"]}'.encode(
                    "UTF-8"
                )
            )
            self.headers[
                "Authorization"
            ] = f'Basic {authorization_string.decode("UTF-8")}'
        elif self.headers is not None:
            return
        else:
            raise SDKInitiationFailedException("** [ERROR] credential does not exists.")

    def _read_config(self, credential_path, profile):
        config = configparser.ConfigParser()
        config.read(credential_path)
        ret = {}
        vars = ["team_name", "access_key"]
        for var in vars:
            try:
                ret[var] = config.get(profile, var)
            except (configparser.NoSectionError, configparser.NoOptionError):
                ret = None
                break
        if ret is not None:
            return ret

        ret = {}
        vars = ["access_key", "account_name"]
        for var in vars:
            try:
                ret["team_name" if var == "account_name" else var] = config.get(
                    profile, var
                )
            except (configparser.NoSectionError, configparser.NoOptionError):
                return None
                break

        return ret

    def check_session(self):
        try:
            response = self.execute("{projects{edges{id}}}")
        except Exception:
            return False

        if not "data" in response.json():
            return False
        else:
            return True

    def execute(self, query: str, values: dict = {}):
        self._set_headers()
        data = {"query": query, "variables": values}
        request_param = json.dumps(data, cls=AttributeEncoder)
        try:
            with requests_retry_session() as session:
                response = session.post(
                    self.endpoint, data=request_param, headers=self.headers
                )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                self.history.appendleft({"Unauthorized Exception": data})
                raise UnauthorizedException("Unauthorized Exception")
            elif response.status_code == 403:
                self.history.appendleft({"ForbiddenException"})
                raise ForbiddenException("Forbidden Exception")
            self.history.appendleft({"APIException": data})
            raise APIException(f"HTTP Error: {repr(e)}")
        except requests.exceptions.Timeout as e:
            self.history.appendleft({"APIException": data})
            raise APIException(f"Request Time Out Exception: {repr(e)}")
        except requests.exceptions.ConnectionError as e:
            self.history.appendleft({"APIException": data})
            raise APIException(f"Network Connection Error: {repr(e)}")
        except Exception as e:
            self.history.appendleft({"APIException": data})
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
                self.history.appendleft({"AuthenticateFailedException": data})
                raise AuthenticateFailedException(
                    "Authentication Failed Exception : Check your credentials"
                )
            elif error["message"] == "Limit Exceeded":
                self.history.appendleft({"AuthenticateFailedException": data})
                raise APILimitExceededException(
                    "Limit Exceeded Exception : API request limit exceeded"
                )

        if "errors" in result:
            errors = result["errors"]
            for error in errors:
                if error["extensions"]["code"] == "INTERNAL_SERVER_ERROR":
                    self.history.appendleft({"Unknown Error": data})
                    raise APIUnknownException(
                        "Unknown Error Exception: Check your API response"
                    )
                elif int(error["extensions"]["code"]) == 400:
                    self.history.appendleft({"BadRequestException": data})
                    raise BadRequestException("Bad Request Exception")
                elif int(error["extensions"]["code"]) == 401:
                    self.history.appendleft({"Unauthorized Exception": data})
                    raise UnauthorizedException("Unauthorized Exception")
                elif int(error["extensions"]["code"]) == 403:
                    self.history.appendleft({"ForbiddenException"})
                    raise ForbiddenException("Forbidden Exception")
                elif error["message"] == "Request failed with status code 404" or int(
                    error["extensions"]["code"] == 404
                ):
                    self.history.appendleft({"NotFoundException": data})
                    raise NotFoundException(
                        "Not Found Exception: Open API returns not found exception with status code 404"
                    )
                elif int(error["extensions"]["code"]) == 409:
                    self.history.appendleft({"ConflictException": data})
                    raise ConflictException("Conflict Exception")
                elif (
                    error["message"] == "Not Available Server"
                    or int(error["extensions"]["code"]) == 503
                ):
                    self.history.appendleft({"NotAvailableException": data})
                    raise NotAvailableServerException(
                        "Not Available Server Exception: Not connected to the server"
                    )
                else:
                    self.history.appendleft({"Unknown Error": data})
                    raise APIUnknownException(
                        "Unknown Error Exception: Check your API response"
                    )

        self.history.appendleft({"success": data})
        return response
