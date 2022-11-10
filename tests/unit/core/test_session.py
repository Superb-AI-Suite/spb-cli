import unittest
import os

from unittest.mock import patch, Mock

from spb.core.session import BaseSession as Session
from spb.exceptions import AuthenticateFailedException, APILimitExceededException, SDKInitiationFailedException, APIException


class SessionConfigurationTest(unittest.TestCase):
    def test_make_session_with_right_access_key_and_team_name(self):
        session = Session(team_name='RIGHT_TEAM_NAME', access_key='RIGHT_ACCESS_KEY')
        assert session.credential == {
            'team_name': 'RIGHT_TEAM_NAME',
            'access_key': 'RIGHT_ACCESS_KEY'
        }

    @patch('spb.core.session.os.path.exists', return_value=False)
    def test_make_session_raises_exceptions_with_none_access_key(self, mock_file):
        team_name = 'RIGHT_TEAM_NAME'

        if not os.getenv('SPB_ACCESS_KEY', None) and not os.getenv('SPB_TEAM_NAME', None):
            with self.assertRaises(SDKInitiationFailedException):
                session = Session(team_name=team_name, access_key=None)
        else:
            session = Session(team_name=team_name, access_key=None)
            self.assertEqual(session.credential, {
                'team_name': os.getenv('SPB_TEAM_NAME', None),
                'access_key': os.getenv('SPB_ACCESS_KEY', None)
            })

    @patch('spb.core.session.os.path.exists', return_value=False)
    def test_make_session_raises_exceptions_with_none_team_name(self, mock_file):
        access_key = 'RIGHT_ACCESS_KEY'

        if not os.getenv('SPB_ACCESS_KEY', None) and not os.getenv('SPB_TEAM_NAME', None):
            with self.assertRaises(SDKInitiationFailedException):
                session = Session(team_name=None, access_key=access_key)
        else:
            session = Session(team_name=None, access_key=access_key)
            self.assertEqual(session.credential, {
                'team_name': os.getenv('SPB_TEAM_NAME', None),
                'access_key': os.getenv('SPB_ACCESS_KEY', None)
            })


class SessionActivateTest(unittest.TestCase):
    @patch('requests.sessions.Session.post')
    def test_session_is_activate_with_right_access_key(self, mock_graphql):
        response = mock_graphql.return_value
        response.status_code = 200
        response.json.return_value = {'data': {'projects': {'edges': []}}}

        session = Session(team_name='DUMMY_TEAM_NAME', access_key='DUMMY_ACCESS_KEY')
        result = session.check_session()

        self.assertEqual(result, True)

    @patch('requests.sessions.Session.post')
    def test_session_raises_Exceptions_with_wrong_access_key(self, mock_graphql):
        response = mock_graphql.return_value
        response.status_code = 403
        response.json.return_value = {
            "error": {
                "message": "Forbidden"
            }
        }

        session = Session(team_name='WRONG_ACCOUNT_NAME', access_key='WRONG_ACCESS_KEY')
        self.assertEqual(session.check_session(), False)

