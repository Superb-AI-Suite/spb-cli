import os

from spb.core.session import BaseSession


class Session(BaseSession):
    endpoint = os.getenv("SPB_APP_API_ENDPOINT", "https://api.superb-ai.com/v2/graphql")
