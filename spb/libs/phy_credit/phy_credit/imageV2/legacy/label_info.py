from uuid import uuid4
from . import __version__


class LabelInfo:

    @classmethod
    def _set_properties(cls, properties_def, properties):
        prop_def_map = {prop_def['name']: prop_def for prop_def in properties_def}
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop['name']]

            if prop_def['type'] in ['radio', 'dropdown', 'checkbox']:
                opt_map = {opt['name']: opt for opt in prop_def['options']}

                if prop_def['type'] == 'checkbox':
                    option_id = [opt_map[val]['id'] for val in prop['value']]
                    option_name = [opt_map[val]['name'] for val in prop['value']]
                else:
                    option_id = opt_map[prop['value']]['id']
                    option_name = opt_map[prop['value']]['name']

                converted_properties.append({
                    'propertyId': prop_def['id'],
                    'propertyName': prop_def['name'],
                    'optionId': option_id,
                    'optionName': option_name,
                })
            elif prop_def['type'] == 'free response':
                converted_properties.append({
                    'propertyId': prop_def['id'],
                    'propertyName': prop_def['name'],
                    'value': prop['value'],
                })
        return converted_properties

    @classmethod
    def _get_properties(cls, properties_def, properties):
        prop_def_map = {prop_def['name']: prop_def for prop_def in properties_def}
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop['propertyName']]

            if prop_def['type'] in ['radio', 'dropdown', 'checkbox']:
                converted_properties.append({
                    'name': prop['propertyName'],
                    'value': prop['optionName']
                })
            elif prop_def['type'] == 'free response':
                converted_properties.append({
                    'name': prop['propertyName'],
                    'value': prop['value'],
                })
        return converted_properties

    def __init__(self, label_interface, result=None):
        self.label_interface = label_interface
        self.object_classes_map = {
            object_class['name']: object_class
            for object_class in label_interface['object_detection']['object_classes']
        }
        if result is None:
            self.result = {}
            self.init_objects()
            self.init_categories()
        else:
            self.result = result

    def default_categories_value(self):
        try:
            return {
                'properties': [
                    {
                        "propertyId": prop_def['id'],
                        "propertyName": prop_def['name'],
                        "optionId": [],
                        "optionName": []
                    }
                    for prop_def in self.label_interface['categorization']['properties']
                ]
            }
        except:
            return {'properties': []}

    def init_objects(self):
        self.result['objects'] = []

    def init_categories(self):
        self.result['categories'] = self.default_categories_value()

    def add_object(self, class_name, annotation, properties=None, id=None):
        id = str(uuid4()) if id is None else id
        annotation_type = self.object_classes_map[class_name]['annotation_type']

        self.result['objects'].append({
            'id': id,
            'classId': self.object_classes_map[class_name]['id'],
            'className': class_name,
            'annotationType': annotation_type,
            'annotation': {
                'coord': annotation['coord'],
                'meta': annotation.get('meta', {}),
            },
            'properties': LabelInfo._set_properties(self.object_classes_map[class_name]['properties'], properties if properties is not None else []),
        })

    def get_objects(self):
        try:
            simple_objects = [
                {
                    'id': obj['id'],
                    'class_name': obj['className'],
                    'annotation': obj['annotation'],
                    'properties': LabelInfo._get_properties(self.object_classes_map[obj['className']]['properties'], obj['properties']),
                }
                for obj in self.result['objects']
            ]
            return simple_objects
        except Exception as e:
            return []

    def set_categories(self, frames=None, properties=None):
        self.result['categories'] = {
            'properties': LabelInfo._set_properties(self.label_interface['categorization']['properties'], properties if properties is not None else [])
        }

    def get_categories(self):
        try:
            simple_categories = {
                'properties': LabelInfo._get_properties(self.label_interface['categorization']['properties'], self.result['categories']['properties']),
            }
            return simple_categories
        except:
            return {'properties': []}

    def build_tags(self):
        classes_count = {}
        classes_name = {}
        for obj in self.result['objects']:
            classes_count[obj['classId']] = classes_count.get(obj['classId'], 0) + 1
            classes_name[obj['classId']] = obj['className']

        return {
            'classes_id': list(classes_count.keys()),
            'class': list(classes_name.values()),
            'classes_count': [
                {
                    'id': k,
                    'name': classes_name[k],
                    'count': v,
                }
                for k, v in classes_count.items()
            ],
        }

    def build_info(self):
        return {
            'version': __version__,
            'meta': {
                'imageInfo': {},
                'editInfo': {
                    'objects': [
                        {
                            'id': obj['id'],
                            'color': self.object_classes_map[obj['className']]['color'],
                            'visible': True,
                            'selected': False,
                        }
                        for obj in self.result['objects']
                    ]
                }
            },
            'result': self.result,
            'tags': self.build_tags(),
        }
