import unittest
from unittest.mock import patch, Mock

from spb.core.session import BaseSession as Session
from spb.exceptions import AuthenticateFailedException, APILimitExceededException, SDKInitiationFailedException, APIException


class SessionConfigurationTest(unittest.TestCase):
    def test_make_session_with_right_access_key_and_account_name(self):
        session = Session(account_name='RIGHT_ACCOUNT_NAME', access_key='RIGHT_ACCESS_KEY')
        assert session.credential == {
            'account_name': 'RIGHT_ACCOUNT_NAME',
            'access_key': 'RIGHT_ACCESS_KEY'
        }

    @patch('spb.core.session.os.path.exists', return_value=False)
    def test_make_session_raises_exceptions_with_none_access_key(self, mock_file):
        account_name = 'RIGHT_ACCOUNT_NAME'

        with self.assertRaises(SDKInitiationFailedException):
            session = Session(account_name=account_name, access_key=None)

    @patch('spb.core.session.os.path.exists', return_value=False)
    def test_make_session_raises_exceptions_with_none_account_name(self, mock_file):
        access_key = 'RIGHT_ACCESS_KEY'

        with self.assertRaises(SDKInitiationFailedException):
            session = Session(account_name=None, access_key=access_key)


class SessionActivateTest(unittest.TestCase):
    @patch('spb.core.session.requests.post')
    def test_session_is_activate_with_right_access_key(self, mock_graphql):
        response = mock_graphql.return_value
        response.status_code = 200
        response.json.return_value = {'data': {'projects': {'edges': []}}}

        session = Session(account_name='DUMMY_ACCOUNT_NAME', access_key='DUMMY_ACCESS_KEY')
        result = session.check_session()

        self.assertEqual(result, True)

    @patch('spb.core.session.requests.post')
    def test_session_raises_Exceptions_with_wrong_access_key(self, mock_graphql):
        response = mock_graphql.return_value
        response.status_code = 403
        response.json.return_value = {
            "error": {
                "message": "Forbidden"
            }
        }

        session = Session(account_name='WRONG_ACCOUNT_NAME', access_key='WRONG_ACCESS_KEY')
        self.assertEqual(session.check_session(), False)

