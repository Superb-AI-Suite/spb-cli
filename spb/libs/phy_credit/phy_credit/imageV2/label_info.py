from uuid import uuid4
from .. import __version__


class LabelInfo:
    @classmethod
    def _get_opt_map(cls, options):
        res = {}
        for opt in options:
            if 'children' in opt:
                res.update(LabelInfo._get_opt_map(opt['children']))
            else:
                res[opt['name']] = opt
        return res


    @classmethod
    def _set_properties(cls, properties_def, properties):
        prop_def_map = {prop_def['name']: prop_def for prop_def in properties_def}
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop['name']]
            if prop_def['type'] in ['radio', 'dropdown', 'checkbox']:
                opt_map = LabelInfo._get_opt_map(prop_def['options'])
                if prop_def['type'] == 'checkbox':
                    converted_properties.append({
                        'type': prop_def['type'],
                        'property_id': prop_def['id'],
                        'property_name': prop_def['name'],
                        'option_ids': [opt_map[val]['id'] for val in prop['value']],
                        'option_names': [opt_map[val]['name'] for val in prop['value']],
                    })
                else:
                    converted_properties.append({
                        'type': prop_def['type'],
                        'property_id': prop_def['id'],
                        'property_name': prop_def['name'],
                        'option_id': opt_map[prop['value']]['id'],
                        'option_name': opt_map[prop['value']]['name'],
                    })
            elif prop_def['type'] == 'free response':
                converted_properties.append({
                    'type': prop_def['type'],
                    'property_id': prop_def['id'],
                    'property_name': prop_def['name'],
                    'value': prop['value'],
                })
        return converted_properties

    @classmethod
    def _get_properties(cls, properties_def, properties):
        prop_def_map = {prop_def['name']: prop_def for prop_def in properties_def}
        converted_properties = []
        for prop in properties:
            prop_def = prop_def_map[prop['property_name']]
            if prop_def['type'] in ['radio', 'dropdown']:
                converted_properties.append({
                    'name': prop['property_name'],
                    'value': prop['option_name']
                })
            elif prop_def['type'] == 'checkbox':
                converted_properties.append({
                    'name': prop['property_name'],
                    'value': prop['option_names']
                })
            elif prop_def['type'] == 'free response':
                converted_properties.append({
                    'name': prop['property_name'],
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

    def init_objects(self):
        self.result['objects'] = []

    def init_categories(self):
        self.result['categories'] = {'properties': []}

    def add_object(self, class_name, annotation, properties=None, id=None):
        id = str(uuid4()) if id is None else id
        annotation_type = self.object_classes_map[class_name]['annotation_type']

        self.result['objects'].append({
            'id': id,
            'class_id': self.object_classes_map[class_name]['id'],
            'class_name': class_name,
            'annotation_type': annotation_type,
            'annotation': {
                'multiple': annotation.get('multiple', False),
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
                    'class_name': obj['class_name'],
                    'annotation': obj['annotation'],
                    'properties': LabelInfo._get_properties(self.object_classes_map[obj['class_name']]['properties'], obj['properties']),
                }
                for obj in self.result['objects']
            ]
            return simple_objects
        except Exception as e:
            return []

    def set_categories(self, properties=None):
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
            classes_count[obj['class_id']] = classes_count.get(obj['class_id'], 0) + 1
            classes_name[obj['class_id']] = obj['class_name']
        class_val = list(classes_name.values())

        categories_id = []
        if 'categories' in self.result and 'properties' in self.result['categories']:
            for prop in self.result['categories']['properties']:
                if 'option_id' in prop:
                    categories_id.append(prop['option_id'])
                elif 'option_ids' in prop:
                    for o_id in prop['option_ids']:
                        categories_id.append(o_id)
            class_val.extend(categories_id)

        return {
            'classes_id': list(classes_count.keys()),
            'class': class_val,
            'classes_count': [
                {
                    'id': k,
                    'name': classes_name[k],
                    'count': v,
                }
                for k, v in classes_count.items()
            ],
            'categories_id': categories_id,
        }

    def build_info(self):
        return {
            'version': __version__,
            'meta': {
                'image_info': {},
                'edit_info': {
                    'objects': [
                        {
                            'id': obj['id'],
                            'color': self.object_classes_map[obj['class_name']]['color'],
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
