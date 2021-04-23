from spb.exceptions import ModelInitiationFailedException
from spb.core.query import BaseQuery as Query
from spb.core.session import BaseSession as Session


class BaseManager(object):
    ''' Data mapper interface (generic repository) for models '''
    __query = None
    __session = None

    def __init__(self, query: Query = Query(), session: Session = Session()):
        self.__query = query
        self.__session = session

    @property
    def query(self):
        return self.__query

    @query.setter
    def query(self, query: Query):
        self.__query = query

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session: Session):
        self.__session = session
