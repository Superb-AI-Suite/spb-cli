import pytest
import unittest
import uuid

from spb.core import Model
from spb.core.manager import BaseManager as Manager
from spb.core.query import BaseQuery as Query
from spb.core.session import BaseSession as Session


class ManagerTest(unittest.TestCase):
    def test_init_manager(self):
        manager = Manager()
        assert isinstance(manager, Manager)

    def test_init_manager_query(self):
        manager = Manager()
        assert isinstance(manager.query, Query)

    def test_init_manager_session(self):
        manager = Manager()
        assert isinstance(manager.session, Session)
