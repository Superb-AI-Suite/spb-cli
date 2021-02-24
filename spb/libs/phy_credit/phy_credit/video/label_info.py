from uuid import uuid4


class LabelInfo:
    _VERSION = '0.2.1-py'
    _INIT_RESULT = {
        'categories': {
            'frames': [],
            'properties': [],
        },
        'objects': []
    }

    def __init__(self, label_interface, result=_INIT_RESULT):
        self.label_interface = label_interface
        self.result = result
        self.object_classes_map = {
            object_class['name']: object_class
            for object_class in label_interface['object_tracking']['object_classes']
        }

    def init_objects(self):
        self.result['objects'] = []

    def init_categories(self):
        self.result['categories'] = { 'frames': [], 'properties': [] }

    def add_object(self, tracking_id, class_name, annotations, properties=None, id=None):
        id = str(uuid4()) if id is None else id

        self.result['objects'].append({
            'id': id,
            'trackingId': tracking_id,
            'classId': self.object_classes_map[class_name]['id'],
            'className': class_name,
            'annotationType': self.object_classes_map[class_name]['annotation_type'],
            'frames': [
                {
                    "num": anno["frame_num"],
                    "annotation": {
                        "coord": anno["coord"],
                        "meta": anno.get("meta", {}),
                    },
                    "properties": anno.get("properties", []),
                }
                for anno in annotations
            ],
            'properties': properties if properties is not None else [],
        })

    def set_categories(self, categories):
        self.result['categories'] = categories

    def get_objects(self):
        try:
            simple_objects = [
                {
                    'id': obj['id'],
                    'tracking_id': obj['trackingId'],
                    'class_name': obj['className'],
                    'annotations': [
                        {
                            'frame_num': frame['num'],
                            'coord': frame['annotation']['coord'],
                            'properties': frame['properties'],
                        }
                        for frame in obj['frames']
                    ],
                    'properties': obj['properties'],
                }
                for obj in self.result['objects']
            ]
            return simple_objects
        except:
            return []

    def build_tags(self):
        classes_count = {}
        anno_count = {}
        classes_name = {}
        for obj in self.result['objects']:
            classes_count[obj['classId']] = classes_count.get(obj['classId'], 0) + 1
            anno_count[obj['classId']] = anno_count.get(obj['classId'], 0) + len(obj['frames'])
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
            'classes_annotation_count': [
                {
                    'id': k,
                    'name': classes_name[k],
                    'count': v,
                }
                for k, v in anno_count.items()
            ],
        }

    def build_info(self):
        return {
            'version': self._VERSION,
            'meta': {
                'imageInfo': {},
                'editInfo': {
                    'objects': [
                        {
                            'id': obj['id'],
                            'color': self.object_classes_map[obj['className']]['color'],
                            'visible': True,
                            'selected': False,
                            'trackingId': obj['trackingId'],
                        }
                        for obj in self.result['objects']
                    ]
                }
            },
            'result': self.result,
            'tags': self.build_tags(),
        }
