# MIT License
#
# Copyright (c) 2020 Superb AI Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
# from spb.projects.manager import ProjectManager
# from spb.labels.manager import LabelManager
# from spb.data.manager import DataManager

from spb.command import Command
from spb.core.session import BaseSession as CoreSession
from spb.exceptions import CommandInitiationFailedException
from spb.sdk_config import (
    DEFAULT_CORE_SESSION,
    DEFAULT_SESSION,
    SDK_AUTHOR,
    SDK_VERSION,
)
from spb.session import Session

# from spb.spb_logger import SPBLogger
from spb.spb_logger import create_logger

# import spb.exceptions


__author__ = SDK_AUTHOR
__version__ = SDK_VERSION


def setup_default_session(**kwargs):
    global DEFAULT_SESSION
    global DEFAULT_CORE_SESSION
    DEFAULT_SESSION = Session(**kwargs)
    DEFAULT_CORE_SESSION = CoreSession(**kwargs)


def _get_default_session(**kwargs):
    if DEFAULT_SESSION is None or DEFAULT_CORE_SESSION is None:
        setup_default_session(**kwargs)

    return DEFAULT_SESSION


def client(**kwargs):
    if "logger_config" in kwargs:
        create_logger(config=kwargs["logger_config"])
    elif "logger" in kwargs:
        create_logger(logger=kwargs["logger"])
    else:
        create_logger()
    return _get_default_session(**kwargs)


def run(
    command: Command,
    option: dict = {},
    page: int = None,
    page_size: int = None,
    optional: dict = {},
):
    try:
        if command is None:
            raise CommandInitiationFailedException("Command required argument")
        optional["page"] = page if page is not None else None
        optional["pageSize"] = page_size if page_size is not None else None
        return command.execute(
            session=DEFAULT_SESSION, option=option, optional=optional
        )
    except Exception as e:
        raise e



# team_name = None
# access_key = None

# ProjectClient = lambda: ProjectManager(team_name=team_name, access_key=access_key)
# LabelClient = lambda: LabelManager(team_name=team_name, access_key=access_key)
# # DataClient = lambda: DataManager(team_name=team_name, access_key=access_key)

# clients = {
#     "project": ProjectClient,
#     "label": LabelClient,
#     # "data": DataClient,
# }
# Client = lambda resource: clients.get(resource.lower())()



__all__ = (
    'setup_default_session',
    '_get_default_session',
    'client',
    'run',
    # 'team_name',
    # 'access_key',
    # 'ProjectClient',
    # 'LabelClient',
    # 'DataClient',
    # 'Client',
)