import numbers
import inspect
import re
from .type_base import Type

class Query(object):

    @classmethod
    def get(cls, model, optional):
        where = cls._where_message(cls, model=model, optional=optional)
        query_id = cls._query_id(cls, model=model)
        attrs = cls._model_attrs_to_query(cls, model=model)
        return cls._make_query(cls, query_id=query_id, where=where, attrs=attrs)

    @classmethod
    def mutation(cls, model, optional):
        query_id = cls._mutation_query_id(cls, model=model)
        attrs = cls._model_attrs_to_query(cls, model=model)
        values = cls._model_attrs_to_values(
            cls, model=model, optional=optional)
        return cls._make_mutation(cls, query_id=query_id, values=values, attrs=attrs)

    @classmethod
    def delete(cls, model, optional):
        pass

    def _model_attrs_to_values(self, model, optional):
        query = Query()
        immutable_attrs = model._immutables
        attrs = model.get_attr_names().keys()
        mutable_attrs = [attr for attr in attrs if attr not in immutable_attrs]
        for key, value in model._attrs.items():
            if isinstance(value, Type) and repr(value) == 'ID' and not key in mutable_attrs:
                mutable_attrs.append(key)
        return query._params(mode='MUTATION', model=model, used_attrs=mutable_attrs, optional=optional)

    def _where_message(self, model, optional):
        query = Query()
        filterable_attrs = model._filterables
        return query._params(model=model, used_attrs=filterable_attrs, optional=optional)

    def _params(self, model, used_attrs, optional, mode='QUERY'):
        if used_attrs is None:
            return None
        attr_classes = model._attrs_classes
        temp = {}
        for attr in used_attrs:
            name = model.get_attr_names().get(attr, None)
            if name is not None:
                value = model.attribute_values[name]
                if value is not None:
                    temp.update(attr_classes[name]._type_to_query(attr, value))

        if mode == 'QUERY':
            for key, value in optional.items():
                if value is not None:
                    temp[key] = value if str(value).isdigit() else Query._safe_double_quote(value)

        elif mode == 'MUTATION':
            for key, value in optional.items():
                if value is not None and key != 'page' and key != 'pageSize':
                    temp[key] = value if str(value).isdigit() else Query._safe_double_quote(value)

        params = []
        for key, value in temp.items():
            params.append(f'{key}:{value}')

        if len(params) > 0:
            return f'({",".join(params)})'
        else:
            return None

    def _query_id(self, model):
        return Query._camelcase(model.get_resource_name())

    def _mutation_query_id(self, model):
        if model.id is None:
            return Query._camelcase('create_' + model.get_resource_name())
        else:
            return Query._camelcase('update_' + model.get_resource_name())

    def _model_attrs_to_query(self, model):
        model_attrs = model.get_attr_names()
        # TODO: add subquery code
        return ' '.join(model_attrs.keys())

    def _make_query(self, query_id, where=None, attrs=None):
        query_str = '{' + query_id
        query_str += where if where is not None else ''
        query_str += '{count, edges{' + attrs + '}}}'
        return query_str

    def _make_mutation(self, query_id, values, attrs):
        mutation_str = 'mutation {' + query_id + values + '{' + attrs + '}}'
        return mutation_str

    @classmethod
    def _camelcase(cls, value):
        value = re.sub(r"^[\-_\.]", '', str(value))
        if not value:
            return value
        return value[0].lower() + re.sub(r"[\-_\.\s]([a-z])", lambda matched: matched.group(1).upper(), value[1:])

    @classmethod
    def _safe_double_quote(cls, value):
        replaced_value = str(value).replace('"', '\\"')
        return f'"{replaced_value}"'
