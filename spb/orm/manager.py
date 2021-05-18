import spb

from .utils import *
from .query import Query
from spb.exceptions import ModelInitiationFailedException

class Manager(object):  # pylint: disable=R0205
    ''' Data mapper interface (generic repository) for models '''

    def __init__(self, model, type_check=True):
        self.model = model
        self.type_check = type_check
        self.session = spb._get_default_session()

    def _get_model_object(self, options):
        try:
            model = None
            if options == None:
                model = self.model
            optionUUID = options.MODEL_UUID if hasattr(options, 'MODEL_UUID') else False
            if optionUUID and optionUUID == self.model.MODEL_UUID:
                model = options
            if isinstance(options, dict):
                model = self.model.__class__(options)
            if model == None : raise ModelInitiationFailedException
            return model
        except Exception as e:
            raise Exception(e)

    def query(self, options=None, optional={}):
        '''Convert model to graphql query string'''
        model = self._get_model_object(options)
        query = Query.get(model, optional)
        return self.session.execute_query(self.model, query)

    def mutation(self, options=None, optional={}):
        '''"Convert model to graphql mutation string'''
        query = None
        model = self._get_model_object(options)
        query = Query.mutation(model, optional)
        return self.session.execute_mutation(self.model, query)

    def get_query(self, options=None, optional={}):
        model = self._get_model_object(options)
        return Query.get(model, optional)

    def get_mutation(self, options=None, optional={}):
        model = self._get_model_object(options)
        return Query.mutation(model, optional)

    def delete(self, options, optional):
        pass
