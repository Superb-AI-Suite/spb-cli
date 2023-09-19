from uuid import UUID
from typing import List

from .session import Session
from .query import Query
from .user import User
from spb.core.manager import BaseManager


class UserManager(BaseManager):
    def __init__(self, team_name=None, access_key=None):
        self.session = Session(
            team_name=team_name,
            access_key=access_key
        )
        self.team_name = team_name
        self.access_key = access_key
        self.query = Query()

    def get_project_users(self, project_id: UUID) -> (int, List[User]):
        QUERY_ID = "projectUsers"
        self.query.query_id = QUERY_ID

        user = User()
        self.query.response_attrs.extend(user.get_property_names())
        query, values = self.query.build_project_users_query(
            project_id=project_id
        )
        response = self.session.execute(query, values)
        return self.session.extract_project_users(response, QUERY_ID)
