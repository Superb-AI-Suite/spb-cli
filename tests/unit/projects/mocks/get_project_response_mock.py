from spb.projects import Project

MOCK_PROJECT_JSON = {
    'id': 'a9c1f5fa-e698-446b-ab96-fdf9f68a9625',
    'labelCount': 10,
    'labelInterface': '{"type":"image-siesta","version":"0.4.2","data_type":"image","categorization":{"properties":[{"id":"048ef0e4-87bb-497c-b841-949c16abbff4","name":"ABC","type":"checkbox","options":[{"id":"4376f85c-3c41-4d33-9a03-48417befbc3a","name":"A"},{"id":"d6542da5-bb0e-402e-8672-8b24c1f31e18","name":"B"},{"id":"b78ac87d-21c2-4b11-bb14-21cf452c4a0a","name":"C"}],"required":true,"description":"","render_value":false,"default_value":[]}]},"object_detection":{"keypoints":[{"id":"facial-landmark-15","name":"face","edges":[{"u":1,"v":0,"color":"#64b5f6"},{"u":2,"v":0,"color":"#64b5f6"},{"u":4,"v":3,"color":"#ff8a65"},{"u":5,"v":3,"color":"#ff8a65"},{"u":7,"v":6,"color":"#64b5f6"},{"u":9,"v":8,"color":"#ff8a65"},{"u":13,"v":11,"color":"#64b5f6"},{"u":14,"v":11,"color":"#64b5f6"},{"u":13,"v":12,"color":"#ff8a65"},{"u":14,"v":12,"color":"#ff8a65"}],"points":[{"name":"left '
                    'eye '
                    'center","color":"#64b5f6","default_value":{"x":0.75,"y":0.25,"state":{"visible":true}},"symmetric_idx":3},{"name":"left '
                    'eye inner '
                    'corner","color":"#64b5f6","default_value":{"x":0.625,"y":0.25,"state":{"visible":true}},"symmetric_idx":4},{"name":"left '
                    'eye outer '
                    'corner","color":"#64b5f6","default_value":{"x":0.875,"y":0.25,"state":{"visible":true}},"symmetric_idx":5},{"name":"right '
                    'eye '
                    'center","color":"#ff8a65","default_value":{"x":0.25,"y":0.25,"state":{"visible":true}},"symmetric_idx":0},{"name":"right '
                    'eye inner '
                    'corner","color":"#ff8a65","default_value":{"x":0.375,"y":0.25,"state":{"visible":true}},"symmetric_idx":1},{"name":"right '
                    'eye outer '
                    'corner","color":"#ff8a65","default_value":{"x":0.125,"y":0.25,"state":{"visible":true}},"symmetric_idx":2},{"name":"left '
                    'eyebrow inner '
                    'end","color":"#64b5f6","default_value":{"x":0.625,"y":0,"state":{"visible":true}},"symmetric_idx":8},{"name":"left '
                    'eyebrow outer '
                    'end","color":"#64b5f6","default_value":{"x":1,"y":0,"state":{"visible":true}},"symmetric_idx":9},{"name":"right '
                    'eyebrow inner '
                    'end","color":"#ff8a65","default_value":{"x":0.375,"y":0,"state":{"visible":true}},"symmetric_idx":6},{"name":"right '
                    'eyebrow outer '
                    'end","color":"#ff8a65","default_value":{"x":0,"y":0,"state":{"visible":true}},"symmetric_idx":7},{"name":"nose '
                    'tip","color":"#d50000","default_value":{"x":0.5,"y":0.5,"state":{"visible":true}}},{"name":"mouth '
                    'left '
                    'corner","color":"#64b5f6","default_value":{"x":0.75,"y":0.875,"state":{"visible":true}},"symmetric_idx":12},{"name":"mouth '
                    'right '
                    'corner","color":"#ff8a65","default_value":{"x":0.25,"y":0.875,"state":{"visible":true}},"symmetric_idx":11},{"name":"mouth '
                    'center top '
                    'lip","color":"#d50000","default_value":{"x":0.5,"y":0.75,"state":{"visible":true}},"symmetric_idx":13},{"name":"mouth '
                    'center bottom '
                    'lip","color":"#d50000","default_value":{"x":0.5,"y":1,"state":{"visible":true}},"symmetric_idx":14}],"allow_valid_invisibles":false}],"object_groups":[],"object_classes":[{"id":"ad8215b7-331e-41f0-b741-5a72f15db370","name":"A","color":"#FF625A","properties":[],"constraints":{},"ai_class_map":[{"class_ids":[],"engine_id":""}],"annotation_type":"box"},{"id":"0d39750a-718f-4117-a9ff-85dfb415c722","name":"B","color":"#FE9573","properties":[],"constraints":{},"ai_class_map":[],"annotation_type":"rbox"},{"id":"452ffc5a-4813-4b7c-a17d-8c1c29cde01b","name":"C","color":"#FFAF5A","properties":[],"constraints":{},"ai_class_map":[{"class_ids":[],"engine_id":""}],"annotation_type":"polygon"},{"id":"0ecdb18e-abd9-4a69-a756-8c835e7475f9","name":"D","color":"#FFCC00","properties":[],"constraints":{},"ai_class_map":[],"annotation_type":"polyline"},{"id":"a718da69-08db-4f36-ac94-f4b530b3549b","name":"E","color":"#FFF73E","properties":[],"constraints":{},"ai_class_map":[{"class_ids":[],"engine_id":""}],"annotation_type":"keypoint","keypoint_interface_id":"facial-landmark-15"}],"annotation_types":["box","rbox","polygon","polyline","keypoint","image '
                    'category"]}}',
    'name': 'MOCK_PROJECT',
    'progress': 50,
    'workapp': 'image-siesta',
    'stats': ['{"type": "IN_PROGRESS_COUNT", "info": {"not_submitted": 0, "rejected": 0}}', '{"type": "SUBMITTED_COUNT", "info": {"pending_review": 0, "approved": 0}}', '{"type": "SKIPPED_COUNT", "info": {"pending_review": 0, "approved": 0}}']
}

MOCK_PROJECT_RESPONSE_JSON = {
    'data': {
        'projects': {
            'edges': [
                MOCK_PROJECT_JSON
            ],
            'count': 1
        }
    }
}

MOCK_PROJECT = Project(**MOCK_PROJECT_JSON)