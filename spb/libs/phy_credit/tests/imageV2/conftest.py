import pytest


@pytest.fixture
def label_interface_sample():
    return {
        "type": "image-siesta",
        "version": "0.2.6",
        "data_type": "image",
        "categorization": {
            "properties": [
                {
                    "id": "root",
                    "name": "Root",
                    "type": "checkbox",
                    "options": [
                        {
                            "id": "f2c19b26-37fa-4b74-baaf-1105a4b51841",
                            "name": "alphabet",
                            "children": [
                                {
                                    "id": "b2ad46b3-ab05-41e1-be71-6b454daadf8c",
                                    "name": "a",
                                },
                                {
                                    "id": "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                                    "name": "b",
                                },
                                {
                                    "id": "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a",
                                    "name": "c",
                                },
                            ],
                        },
                        {
                            "id": "4964136d-8ebf-4692-98ee-8f81b0fb1234",
                            "name": "number",
                            "children": [
                                {
                                    "id": "a1200bca-41c2-43e5-85d9-4d51554d552b",
                                    "name": "1",
                                },
                                {
                                    "id": "d6711d55-aae5-4dbe-a92e-55d87c1c02ef",
                                    "name": "2",
                                },
                                {
                                    "id": "87c0bf6a-6dfb-46d8-99b4-5112340529c9",
                                    "name": "3",
                                },
                            ],
                        },
                    ],
                    "required": True,
                    "description": "",
                    "render_value": False,
                    "default_value": [],
                }
            ]
        },
        "object_detection": {
            "keypoints": [
                {
                    "id": "keypoint-id",
                    "name": "human",
                    "edges": [
                        {"u": 2, "v": 4, "color": "#ff8a65"},
                        {"u": 0, "v": 2, "color": "#ff8a65"},
                        {"u": 8, "v": 6, "color": "#ff8a65"},
                        {"u": 10, "v": 8, "color": "#ff8a65"},
                        {"u": 12, "v": 6, "color": "#ff8a65"},
                        {"u": 14, "v": 12, "color": "#ff8a65"},
                        {"u": 16, "v": 14, "color": "#ff8a65"},
                        {"u": 1, "v": 2, "color": "#4db6ac"},
                        {"u": 5, "v": 6, "color": "#4db6ac"},
                        {"u": 11, "v": 12, "color": "#4db6ac"},
                        {"u": 1, "v": 0, "color": "#64b5f6"},
                        {"u": 3, "v": 1, "color": "#64b5f6"},
                        {"u": 7, "v": 5, "color": "#64b5f6"},
                        {"u": 9, "v": 7, "color": "#64b5f6"},
                        {"u": 11, "v": 5, "color": "#64b5f6"},
                        {"u": 13, "v": 11, "color": "#64b5f6"},
                        {"u": 15, "v": 13, "color": "#64b5f6"},
                    ],
                    "points": [
                        {
                            "name": "nose",
                            "color": "#d50000",
                            "default_value": {
                                "x": 0.5,
                                "y": 0.1,
                                "state": {"visible": True},
                            },
                        },
                        {
                            "name": "left eye",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.55,
                                "y": 0.05,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 2,
                        },
                        {
                            "name": "right eye",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.45,
                                "y": 0.05,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 1,
                        },
                        {
                            "name": "left ear",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.075,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 4,
                        },
                        {
                            "name": "right ear",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.075,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 3,
                        },
                        {
                            "name": "left shoulder",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.65,
                                "y": 0.2,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 6,
                        },
                        {
                            "name": "right shoulder",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.35,
                                "y": 0.2,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 5,
                        },
                        {
                            "name": "left elbow",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.85,
                                "y": 0.3,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 8,
                        },
                        {
                            "name": "right elbow",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.15,
                                "y": 0.3,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 7,
                        },
                        {
                            "name": "left wrist",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.75,
                                "y": 0.45,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 10,
                        },
                        {
                            "name": "right wrist",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.25,
                                "y": 0.45,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 9,
                        },
                        {
                            "name": "left hip",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.62,
                                "y": 0.5,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 12,
                        },
                        {
                            "name": "right hip",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.38,
                                "y": 0.5,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 11,
                        },
                        {
                            "name": "left knee",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.7,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 14,
                        },
                        {
                            "name": "right_knee",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.7,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 13,
                        },
                        {
                            "name": "left ankle",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.9,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 16,
                        },
                        {
                            "name": "right ankle",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.9,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 15,
                        },
                    ],
                    "allow_valid_invisibles": False,
                }
            ],
            "object_groups": [],
            "object_classes": [
                {
                    "id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "name": "bb",
                    "color": "#FF625A",
                    "properties": [
                        {
                            "id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                            "name": "pc",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "1"},
                                {"id": "2", "name": "2"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "name": "ps",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "1"},
                                {"id": "4", "name": "2"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [{"class_ids": [], "engine_id": ""}],
                    "annotation_type": "box",
                },
                {
                    "id": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                    "name": "pp",
                    "color": "#FE9573",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [{"class_ids": [], "engine_id": ""}],
                    "annotation_type": "polygon",
                },
                {
                    "id": "df8aa5dc-ae20-417d-a522-555b981dcc77",
                    "name": "kk",
                    "color": "#FFAF5A",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "keypoint",
                    "keypoint_interface_id": "keypoint-id",
                },
            ],
            "annotation_types": [
                "box",
                "polygon",
                "keypoint",
                "image category",
            ],
        },
    }


@pytest.fixture
def add_object_1():
    return {
        "class_name": "bb",
        "annotation": {
            "coord": {"x": 173, "y": 92, "width": 188, "height": 161}
        },
        "properties": [
            {"name": "pc", "value": "2"},
            {"name": "ps", "value": ["1"]},
        ],
    }


@pytest.fixture
def add_object_2():
    return {
        "class_name": "bb",
        "annotation": {"coord": {"x": 99, "y": 74, "width": 78, "height": 77}},
        "properties": [
            {"name": "pc", "value": "1"},
            {"name": "ps", "value": ["2", "1"]},
        ],
    }


@pytest.fixture
def add_object_3():
    return {
        "class_name": "pp",
        "annotation": {
            "coord": {
                "points": [
                    {"x": 441, "y": 158},
                    {"x": 483, "y": 301},
                    {"x": 547, "y": 293},
                    {"x": 557, "y": 174},
                ]
            }
        },
    }


@pytest.fixture
def add_object_4():
    return {
        "class_name": "kk",
        "annotation": {
            "coord": {
                "graph": {
                    "nodes": [
                        {"x": 102.5, "y": 178.4},
                        {"x": 108.75, "y": 166.7},
                        {"x": 96.25, "y": 166.7},
                        {"x": 115, "y": 172.55},
                        {"x": 90, "y": 172.55},
                        {"x": 121.25, "y": 201.8},
                        {"x": 83.75, "y": 201.8},
                        {"x": 146.25, "y": 225.2},
                        {"x": 58.75, "y": 225.2},
                        {"x": 133.75, "y": 260.3},
                        {"x": 71.25, "y": 260.3},
                        {"x": 117.5, "y": 272},
                        {"x": 87.5, "y": 272},
                        {"x": 115, "y": 318.79999999999995},
                        {"x": 90, "y": 318.79999999999995},
                        {"x": 115, "y": 365.6},
                        {"x": 90, "y": 365.6},
                    ],
                    "states": [
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                        {"state": {"visible": True}},
                    ],
                }
            }
        },
    }


@pytest.fixture
def sample_tag_result():
    return {
        "classes_id": [
            "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
            "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
            "df8aa5dc-ae20-417d-a522-555b981dcc77",
        ],
        "class": ["bb", "pp", "kk"],
        "classes_count": [
            {
                "id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "name": "bb",
                "count": 2,
            },
            {
                "id": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                "name": "pp",
                "count": 1,
            },
            {
                "id": "df8aa5dc-ae20-417d-a522-555b981dcc77",
                "name": "kk",
                "count": 1,
            },
        ],
    }


@pytest.fixture
def sample_info_result():
    return {
        "meta": {
            "editInfo": {
                "objects": [
                    {
                        "color": "#FF625A",
                        "id": "e0d133c5-7089-465a-8f05-ec5fecccd8ba",
                        "selected": False,
                        "visible": True,
                    },
                    {
                        "color": "#FF625A",
                        "id": "47353aca-6f12-4de8-b54b-5985c3fe7faa",
                        "selected": False,
                        "visible": True,
                    },
                    {
                        "color": "#FE9573",
                        "id": "ddd914fe-0b9b-4ee7-8397-555412ac9687",
                        "selected": False,
                        "visible": True,
                    },
                    {
                        "color": "#FFAF5A",
                        "id": "9473cf55-67b8-4333-abe9-a41f4b4408cd",
                        "selected": False,
                        "visible": True,
                    },
                ]
            },
            "imageInfo": {},
        },
        "result": {
            "categories": {
                "properties": [
                    {
                        "optionIds": [
                            "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                            "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a",
                        ],
                        "optionNames": ["b", "c"],
                        "propertyId": "root",
                        "propertyName": "Root",
                    }
                ]
            },
            "objects": [
                {
                    "annotation": {
                        "coord": {
                            "height": 161,
                            "width": 188,
                            "x": 173,
                            "y": 92,
                        },
                        "meta": {"zIndex": 1},
                    },
                    "annotationType": "box",
                    "classId": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "className": "bb",
                    "id": "e0d133c5-7089-465a-8f05-ec5fecccd8ba",
                    "properties": [
                        {
                            "optionId": "2",
                            "optionName": "2",
                            "propertyId": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                            "propertyName": "pc",
                        },
                        {
                            "optionIds": ["3"],
                            "optionNames": ["1"],
                            "propertyId": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "propertyName": "ps",
                        },
                    ],
                },
                {
                    "annotation": {
                        "coord": {"height": 77, "width": 78, "x": 99, "y": 74},
                        "meta": {"zIndex": 1},
                    },
                    "annotationType": "box",
                    "classId": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "className": "bb",
                    "id": "47353aca-6f12-4de8-b54b-5985c3fe7faa",
                    "properties": [
                        {
                            "optionId": "1",
                            "optionName": "1",
                            "propertyId": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                            "propertyName": "pc",
                        },
                        {
                            "optionIds": ["4", "3"],
                            "optionNames": ["2", "1"],
                            "propertyId": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "propertyName": "ps",
                        },
                    ],
                },
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                {"x": 441, "y": 158},
                                {"x": 483, "y": 301},
                                {"x": 547, "y": 293},
                                {"x": 557, "y": 174},
                            ]
                        },
                        "meta": {"zIndex": 1},
                    },
                    "annotationType": "polygon",
                    "classId": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                    "className": "pp",
                    "id": "ddd914fe-0b9b-4ee7-8397-555412ac9687",
                    "properties": [],
                },
                {
                    "annotation": {
                        "coord": {
                            "graph": {
                                "nodes": [
                                    {"x": 102.5, "y": 178.4},
                                    {"x": 108.75, "y": 166.7},
                                    {"x": 96.25, "y": 166.7},
                                    {"x": 115, "y": 172.55},
                                    {"x": 90, "y": 172.55},
                                    {"x": 121.25, "y": 201.8},
                                    {"x": 83.75, "y": 201.8},
                                    {"x": 146.25, "y": 225.2},
                                    {"x": 58.75, "y": 225.2},
                                    {"x": 133.75, "y": 260.3},
                                    {"x": 71.25, "y": 260.3},
                                    {"x": 117.5, "y": 272},
                                    {"x": 87.5, "y": 272},
                                    {"x": 115, "y": 318.79999999999995},
                                    {"x": 90, "y": 318.79999999999995},
                                    {"x": 115, "y": 365.6},
                                    {"x": 90, "y": 365.6},
                                ],
                                "states": [
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                    {"state": {"visible": True}},
                                ],
                            }
                        },
                        "meta": {"zIndex": 1},
                    },
                    "annotationType": "keypoints",
                    "classId": "df8aa5dc-ae20-417d-a522-555b981dcc77",
                    "className": "kk",
                    "id": "9473cf55-67b8-4333-abe9-a41f4b4408cd",
                    "properties": [],
                },
            ],
        },
        "tags": {
            "class": ["bb", "pp", "kk"],
            "classes_count": [
                {
                    "count": 2,
                    "id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "name": "bb",
                },
                {
                    "count": 1,
                    "id": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                    "name": "pp",
                },
                {
                    "count": 1,
                    "id": "df8aa5dc-ae20-417d-a522-555b981dcc77",
                    "name": "kk",
                },
            ],
            "classes_id": [
                "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                "df8aa5dc-ae20-417d-a522-555b981dcc77",
            ],
        },
        "version": "0.3.1-py",
    }


@pytest.fixture
def sample_build_result():
    return {
        "objects": [
            {
                "id": "e0d133c5-7089-465a-8f05-ec5fecccd8ba",
                "classId": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "className": "bb",
                "annotationType": "box",
                "annotation": {
                    "coord": {"x": 173, "y": 92, "width": 188, "height": 161},
                    "meta": {"zIndex": 1},
                },
                "properties": [
                    {
                        "propertyId": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                        "propertyName": "pc",
                        "optionId": "2",
                        "optionName": "2",
                    },
                    {
                        "propertyId": "f7eebc07-155b-48f3-847d-5501668044ad",
                        "propertyName": "ps",
                        "optionIds": ["3"],
                        "optionNames": ["1"],
                    },
                ],
            },
            {
                "id": "47353aca-6f12-4de8-b54b-5985c3fe7faa",
                "classId": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "className": "bb",
                "annotationType": "box",
                "annotation": {
                    "coord": {"x": 99, "y": 74, "width": 78, "height": 77},
                    "meta": {"zIndex": 1},
                },
                "properties": [
                    {
                        "propertyId": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                        "propertyName": "pc",
                        "optionId": "1",
                        "optionName": "1",
                    },
                    {
                        "propertyId": "f7eebc07-155b-48f3-847d-5501668044ad",
                        "propertyName": "ps",
                        "optionIds": ["4", "3"],
                        "optionNames": ["2", "1"],
                    },
                ],
            },
            {
                "id": "ddd914fe-0b9b-4ee7-8397-555412ac9687",
                "classId": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                "className": "pp",
                "annotationType": "polygon",
                "annotation": {
                    "coord": {
                        "points": [
                            {"x": 441, "y": 158},
                            {"x": 483, "y": 301},
                            {"x": 547, "y": 293},
                            {"x": 557, "y": 174},
                        ]
                    },
                    "meta": {"zIndex": 1},
                },
                "properties": [],
            },
            {
                "id": "9473cf55-67b8-4333-abe9-a41f4b4408cd",
                "classId": "df8aa5dc-ae20-417d-a522-555b981dcc77",
                "className": "kk",
                "annotationType": "keypoints",
                "annotation": {
                    "coord": {
                        "graph": {
                            "nodes": [
                                {"x": 102.5, "y": 178.4},
                                {"x": 108.75, "y": 166.7},
                                {"x": 96.25, "y": 166.7},
                                {"x": 115, "y": 172.55},
                                {"x": 90, "y": 172.55},
                                {"x": 121.25, "y": 201.8},
                                {"x": 83.75, "y": 201.8},
                                {"x": 146.25, "y": 225.2},
                                {"x": 58.75, "y": 225.2},
                                {"x": 133.75, "y": 260.3},
                                {"x": 71.25, "y": 260.3},
                                {"x": 117.5, "y": 272},
                                {"x": 87.5, "y": 272},
                                {"x": 115, "y": 318.79999999999995},
                                {"x": 90, "y": 318.79999999999995},
                                {"x": 115, "y": 365.6},
                                {"x": 90, "y": 365.6},
                            ],
                            "states": [
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                                {"state": {"visible": True}},
                            ],
                        }
                    },
                    "meta": {"zIndex": 1},
                },
                "properties": [],
            },
        ],
        "categories": {
            "properties": [
                {
                    "propertyId": "root",
                    "propertyName": "Root",
                    "optionIds": [
                        "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                        "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a",
                    ],
                    "optionNames": ["b", "c"],
                }
            ]
        },
    }


@pytest.fixture
def label_interface_sample_v4():
    return {
        "type": "image-siesta",
        "version": "0.6.4",
        "data_type": "image",
        "categorization": {
            "properties": [
                {
                    "id": "root",
                    "name": "Root",
                    "type": "checkbox",
                    "options": [
                        {
                            "id": "f2c19b26-37fa-4b74-baaf-1105a4b51841",
                            "name": "alphabet",
                            "children": [
                                {
                                    "id": "b2ad46b3-ab05-41e1-be71-6b454daadf8c",
                                    "name": "a",
                                },
                                {
                                    "id": "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                                    "name": "b",
                                },
                                {
                                    "id": "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a",
                                    "name": "c",
                                },
                            ],
                        },
                        {
                            "id": "4964136d-8ebf-4692-98ee-8f81b0fb1234",
                            "name": "number",
                            "children": [
                                {
                                    "id": "a1200bca-41c2-43e5-85d9-4d51554d552b",
                                    "name": "1",
                                },
                                {
                                    "id": "d6711d55-aae5-4dbe-a92e-55d87c1c02ef",
                                    "name": "2",
                                },
                                {
                                    "id": "87c0bf6a-6dfb-46d8-99b4-5112340529c9",
                                    "name": "3",
                                },
                            ],
                        },
                    ],
                    "required": True,
                    "description": "",
                    "render_value": False,
                    "default_value": [],
                }
            ]
        },
        "object_detection": {
            "keypoints": [],
            "object_groups": [],
            "object_classes": [
                {
                    "id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "name": "bb",
                    "color": "#FF625A",
                    "properties": [
                        {
                            "id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                            "name": "pc",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "1"},
                                {"id": "2", "name": "2"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "name": "ps",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "1"},
                                {"id": "4", "name": "2"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "box",
                }
            ],
            "annotation_types": ["box", "image category"],
        },
    }


@pytest.fixture
def set_category_1():
    return {"properties": [{"name": "Root", "value": ["1", "a", "b"]}]}


@pytest.fixture
def sample_tag_result_v4():
    return {
        "classes_id": ["6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9"],
        "class": [
            "bb",
            "a1200bca-41c2-43e5-85d9-4d51554d552b",
            "b2ad46b3-ab05-41e1-be71-6b454daadf8c",
            "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
        ],
        "classes_count": [
            {
                "id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "name": "bb",
                "count": 2,
            }
        ],
        "classes_properties_count": [
            {
                "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "property_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                "property_name": "pc",
                "option_id": "2",
                "option_name": "2",
                "property_option_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2#2",
                "count": 1,
            },
            {
                "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "property_id": "f7eebc07-155b-48f3-847d-5501668044ad",
                "property_name": "ps",
                "option_id": "3",
                "option_name": "1",
                "property_option_id": "f7eebc07-155b-48f3-847d-5501668044ad#3",
                "count": 2,
            },
            {
                "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "property_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                "property_name": "pc",
                "option_id": "1",
                "option_name": "1",
                "property_option_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2#1",
                "count": 1,
            },
            {
                "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "property_id": "f7eebc07-155b-48f3-847d-5501668044ad",
                "property_name": "ps",
                "option_id": "4",
                "option_name": "2",
                "property_option_id": "f7eebc07-155b-48f3-847d-5501668044ad#4",
                "count": 1,
            },
        ],
        "categories_id": [
            "a1200bca-41c2-43e5-85d9-4d51554d552b",
            "b2ad46b3-ab05-41e1-be71-6b454daadf8c",
            "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
        ],
    }


@pytest.fixture
def sample_info_result_v4():
    return {
        "version": "0.4.7",
        "meta": {
            "image_info": {},
            "edit_info": {
                "objects": [
                    {
                        "id": "31cc65f9-1228-4b38-afd9-59151238f00f",
                        "color": "#FF625A",
                        "visible": True,
                        "selected": False,
                    },
                    {
                        "id": "a44bd6fe-c8ca-4df5-8618-65413e2f2e89",
                        "color": "#FF625A",
                        "visible": True,
                        "selected": False,
                    },
                ]
            },
        },
        "result": {
            "objects": [
                {
                    "id": "31cc65f9-1228-4b38-afd9-59151238f00f",
                    "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "class_name": "bb",
                    "annotation_type": "box",
                    "annotation": {
                        "multiple": False,
                        "coord": {
                            "x": 173,
                            "y": 92,
                            "width": 188,
                            "height": 161,
                        },
                        "meta": {},
                    },
                    "properties": [
                        {
                            "type": "radio",
                            "property_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                            "property_name": "pc",
                            "option_id": "2",
                            "option_name": "2",
                        },
                        {
                            "type": "checkbox",
                            "property_id": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "property_name": "ps",
                            "option_ids": ["3"],
                            "option_names": ["1"],
                        },
                    ],
                },
                {
                    "id": "a44bd6fe-c8ca-4df5-8618-65413e2f2e89",
                    "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "class_name": "bb",
                    "annotation_type": "box",
                    "annotation": {
                        "multiple": False,
                        "coord": {"x": 99, "y": 74, "width": 78, "height": 77},
                        "meta": {},
                    },
                    "properties": [
                        {
                            "type": "radio",
                            "property_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                            "property_name": "pc",
                            "option_id": "1",
                            "option_name": "1",
                        },
                        {
                            "type": "checkbox",
                            "property_id": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "property_name": "ps",
                            "option_ids": ["4", "3"],
                            "option_names": ["2", "1"],
                        },
                    ],
                },
            ],
            "categories": {
                "properties": [
                    {
                        "type": "checkbox",
                        "property_id": "root",
                        "property_name": "Root",
                        "option_ids": [
                            "a1200bca-41c2-43e5-85d9-4d51554d552b",
                            "b2ad46b3-ab05-41e1-be71-6b454daadf8c",
                            "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                        ],
                        "option_names": ["1", "a", "b"],
                    }
                ]
            },
        },
        "tags": {
            "classes_id": ["6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9"],
            "class": [
                "bb",
                "a1200bca-41c2-43e5-85d9-4d51554d552b",
                "b2ad46b3-ab05-41e1-be71-6b454daadf8c",
                "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
            ],
            "classes_count": [
                {
                    "id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "name": "bb",
                    "count": 2,
                }
            ],
            "classes_properties_count": [
                {
                    "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "property_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                    "property_name": "pc",
                    "option_id": "2",
                    "option_name": "2",
                    "property_option_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2#2",
                    "count": 1,
                },
                {
                    "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "property_id": "f7eebc07-155b-48f3-847d-5501668044ad",
                    "property_name": "ps",
                    "option_id": "3",
                    "option_name": "1",
                    "property_option_id": "f7eebc07-155b-48f3-847d-5501668044ad#3",
                    "count": 2,
                },
                {
                    "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "property_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                    "property_name": "pc",
                    "option_id": "1",
                    "option_name": "1",
                    "property_option_id": "5b65d4ae-2737-4de8-a460-70a5aab4eba2#1",
                    "count": 1,
                },
                {
                    "class_id": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                    "property_id": "f7eebc07-155b-48f3-847d-5501668044ad",
                    "property_name": "ps",
                    "option_id": "4",
                    "option_name": "2",
                    "property_option_id": "f7eebc07-155b-48f3-847d-5501668044ad#4",
                    "count": 1,
                },
            ],
            "categories_id": [
                "a1200bca-41c2-43e5-85d9-4d51554d552b",
                "b2ad46b3-ab05-41e1-be71-6b454daadf8c",
                "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
            ],
        },
    }


@pytest.fixture
def label_interface_sample_v6():
    return {
        "type": "image-siesta",
        "version": "0.6.4",
        "data_type": "image",
        "categorization": {
            "properties": [
                {
                    "id": "bb0e4235-9d17-40ed-9852-26fc66941d05",
                    "name": "ms_cate",
                    "type": "checkbox",
                    "options": [
                        {
                            "id": "13cb5be0-33cc-4dda-84c3-ec6afb50680c",
                            "name": "ms_g",
                            "children": [
                                {
                                    "id": "14d9bb96-17cf-44d0-9929-4a9144d85797",
                                    "name": "ms_1",
                                },
                                {
                                    "id": "eba4b04b-b23f-4e65-a020-88e6731300f4",
                                    "name": "ms_2",
                                },
                            ],
                        }
                    ],
                    "required": False,
                    "description": "",
                    "render_value": False,
                    "default_value": [],
                },
                {
                    "id": "0da7b178-df30-47da-bf9b-2daadfbc99d7",
                    "name": "mc_cate",
                    "type": "radio",
                    "options": [
                        {
                            "id": "0bd3a095-2e61-4cf3-b7aa-cb58d4ef1912",
                            "name": "mc_g",
                            "children": [
                                {
                                    "id": "8831d4a4-5bee-4252-b651-c254b4593490",
                                    "name": "mc_1",
                                },
                                {
                                    "id": "08e881d0-c072-443b-9887-d4042c09a998",
                                    "name": "mc_2",
                                },
                            ],
                        }
                    ],
                    "required": False,
                    "description": "",
                    "render_value": False,
                    "default_value": "",
                },
                {
                    "id": "69f0963a-0400-4d9a-81fe-b7ef3ded55db",
                    "name": "fr_cate",
                    "type": "free response",
                    "blank": True,
                    "constraints": {
                        "digit": True,
                        "space": True,
                        "special": True,
                        "alphabet": True,
                    },
                    "description": "",
                    "render_value": False,
                    "default_value": "",
                },
            ]
        },
        "object_detection": {
            "keypoints": [
                {
                    "id": "facial-landmark-15",
                    "name": "face",
                    "edges": [
                        {"u": 1, "v": 0, "color": "#64b5f6"},
                        {"u": 2, "v": 0, "color": "#64b5f6"},
                        {"u": 4, "v": 3, "color": "#ff8a65"},
                        {"u": 5, "v": 3, "color": "#ff8a65"},
                        {"u": 7, "v": 6, "color": "#64b5f6"},
                        {"u": 9, "v": 8, "color": "#ff8a65"},
                        {"u": 13, "v": 11, "color": "#64b5f6"},
                        {"u": 14, "v": 11, "color": "#64b5f6"},
                        {"u": 13, "v": 12, "color": "#ff8a65"},
                        {"u": 14, "v": 12, "color": "#ff8a65"},
                    ],
                    "points": [
                        {
                            "name": "left eye center",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.75,
                                "y": 0.25,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 3,
                        },
                        {
                            "name": "left eye inner corner",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.625,
                                "y": 0.25,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 4,
                        },
                        {
                            "name": "left eye outer corner",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.875,
                                "y": 0.25,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 5,
                        },
                        {
                            "name": "right eye center",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.25,
                                "y": 0.25,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 0,
                        },
                        {
                            "name": "right eye inner corner",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.375,
                                "y": 0.25,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 1,
                        },
                        {
                            "name": "right eye outer corner",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.125,
                                "y": 0.25,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 2,
                        },
                        {
                            "name": "left eyebrow inner end",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.625,
                                "y": 0,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 8,
                        },
                        {
                            "name": "left eyebrow outer end",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 1,
                                "y": 0,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 9,
                        },
                        {
                            "name": "right eyebrow inner end",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.375,
                                "y": 0,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 6,
                        },
                        {
                            "name": "right eyebrow outer end",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0,
                                "y": 0,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 7,
                        },
                        {
                            "name": "nose tip",
                            "color": "#d50000",
                            "default_value": {
                                "x": 0.5,
                                "y": 0.5,
                                "state": {"visible": True},
                            },
                        },
                        {
                            "name": "mouth left corner",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.75,
                                "y": 0.875,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 12,
                        },
                        {
                            "name": "mouth right corner",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.25,
                                "y": 0.875,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 11,
                        },
                        {
                            "name": "mouth center top lip",
                            "color": "#d50000",
                            "default_value": {
                                "x": 0.5,
                                "y": 0.75,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 13,
                        },
                        {
                            "name": "mouth center bottom lip",
                            "color": "#d50000",
                            "default_value": {
                                "x": 0.5,
                                "y": 1,
                                "state": {"visible": True},
                            },
                            "symmetric_idx": 14,
                        },
                    ],
                    "allow_valid_invisibles": False,
                }
            ],
            "object_groups": [],
            "object_classes": [
                {
                    "id": "346c2e59-0d4d-4818-8cd0-538b157fa06c",
                    "name": "box",
                    "color": "#FF625A",
                    "properties": [
                        {
                            "id": "c126812b-c013-4f78-b709-7a1764c7c7f3",
                            "name": "box Property",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "3b09f755-e34f-4d5b-9950-0467d08b5c6b",
                            "name": "box Property (1)",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                        {
                            "id": "da2e15ff-98bc-4ef4-a1c9-1830f0e32908",
                            "name": "box Property (2)",
                            "type": "free response",
                            "blank": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True,
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": "",
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "box",
                },
                {
                    "id": "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                    "name": "rbox",
                    "color": "#FE9573",
                    "properties": [
                        {
                            "id": "e8405ff2-a091-4fb3-9ee3-33921491be6b",
                            "name": "rbox Property",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "3e75a099-875a-4576-9548-2e2f171e6ad5",
                            "name": "rbox Property (1)",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                        {
                            "id": "29243fd2-92c4-4f11-baa0-0e615901039f",
                            "name": "rbox Property (2)",
                            "type": "free response",
                            "blank": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True,
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": "",
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "rbox",
                },
                {
                    "id": "7c6ab4db-5b0c-4143-b992-6dc732f28870",
                    "name": "poly",
                    "color": "#FFAF5A",
                    "properties": [
                        {
                            "id": "d1516ef1-a64d-45c4-9bd0-d26a38658839",
                            "name": "poly Property",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "7ac2d2d6-bbcf-422e-8b88-0b20335626a0",
                            "name": "poly Property (1)",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                        {
                            "id": "a2bae19d-b700-4633-81b3-880b6fcc9fc0",
                            "name": "poly Property (2)",
                            "type": "free response",
                            "blank": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True,
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": "",
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "polyline",
                },
                {
                    "id": "5a122ca5-b827-4896-9476-ab01d5164853",
                    "name": "poly_seg",
                    "color": "#FFCC00",
                    "properties": [
                        {
                            "id": "00f9510e-c574-4667-8f76-17c51618e272",
                            "name": "poly_seg Property",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "1007f627-a13f-4678-a411-871482dfd166",
                            "name": "poly_seg Property (1)",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                        {
                            "id": "2fccbadc-271f-4124-a3e2-71a759db27c0",
                            "name": "poly_seg Property (2)",
                            "type": "free response",
                            "blank": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True,
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": "",
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "polygon",
                },
                {
                    "id": "96007e8f-3c76-4359-88d3-27cc3b2e986f",
                    "name": "face_kp",
                    "color": "#FFF73E",
                    "properties": [
                        {
                            "id": "8f826174-6b13-4144-80a9-df236d986c38",
                            "name": "face_kp Property",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "743e543b-c51c-4eac-a29b-f8fa20dd2474",
                            "name": "face_kp Property (1)",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                        {
                            "id": "931e64e5-30b2-4da0-a435-b32f40cad7cb",
                            "name": "face_kp Property (2)",
                            "type": "free response",
                            "blank": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True,
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": "",
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "keypoint",
                    "keypoint_interface_id": "facial-landmark-15",
                },
                {
                    "id": "e970ec55-2dd7-4a94-8a93-ec2b34ed5005",
                    "name": "2d_cuboid",
                    "color": "#DEF00F",
                    "properties": [
                        {
                            "id": "cd1ce733-f0f9-45f2-b2d3-d95016807656",
                            "name": "2d_cuboid Property",
                            "type": "radio",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None,
                        },
                        {
                            "id": "faf00cd0-99d6-409e-a9ad-75c8830c021a",
                            "name": "2d_cuboid Property (1)",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                        {
                            "id": "b75b8e1f-0e18-405f-bcde-f808fc3595dc",
                            "name": "2d_cuboid Property (2)",
                            "type": "free response",
                            "blank": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True,
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": "",
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "cuboid2d",
                },
                {
                    "id": "414d1b1d-fe14-4e16-af4e-908a5a8147c1",
                    "name": "박스",
                    "color": "#A3EB57",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "box",
                },
            ],
            "annotation_types": [
                "box",
                "rbox",
                "polyline",
                "polygon",
                "keypoint",
                "cuboid2d",
                "image category",
            ],
        },
    }


@pytest.fixture
def label_info_sample_v6():
    return {
        "version": "0.6.4",
        "meta": {
            "image_info": {},
            "edit_info": {
                "objects": [
                    {
                        "id": "12590dbe-72f1-4278-b1fe-b4a0642d55b6",
                        "color": "#FF625A",
                        "visible": True,
                        "selected": False,
                    },
                    {
                        "id": "6f4e5ef6-e3ea-4a2d-b0a1-3ebd00b965b3",
                        "color": "#FE9573",
                        "visible": True,
                        "selected": False,
                    },
                    {
                        "id": "9b20fabd-9b33-422b-bbb5-870cfaad31b2",
                        "color": "#FFAF5A",
                        "visible": True,
                        "selected": False,
                    },
                    {
                        "id": "92e28cc4-7eee-4a72-9dc4-383ffd4ecf70",
                        "color": "#FFCC00",
                        "visible": True,
                        "selected": False,
                    },
                    {
                        "id": "9ed93108-2c3a-4eba-8613-0633003a239f",
                        "color": "#FFF73E",
                        "visible": True,
                        "selected": False,
                    },
                    {
                        "id": "10a57f9d-3d04-4ce6-aa8f-516300cd8f75",
                        "color": "#DEF00F",
                        "visible": True,
                        "selected": False,
                    },
                ]
            },
        },
        "result": {
            "objects": [
                {
                    "id": "12590dbe-72f1-4278-b1fe-b4a0642d55b6",
                    "class_name": "box",
                    "class_id": "346c2e59-0d4d-4818-8cd0-538b157fa06c",
                    "annotation_type": "box",
                    "annotation": {
                        "coord": {
                            "x": 26.3,
                            "y": 24.1,
                            "width": 36.3,
                            "height": 25.2,
                        },
                        "meta": {
                            "z_index": 1,
                            "visible": True,
                            "alpha": 1,
                            "color": "#FF625A",
                        },
                    },
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "6f4e5ef6-e3ea-4a2d-b0a1-3ebd00b965b3",
                    "class_name": "rbox",
                    "class_id": "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                    "annotation_type": "rbox",
                    "annotation": {
                        "coord": {
                            "cx": 55.6,
                            "cy": 84.0,
                            "width": 27.8,
                            "height": 22.4,
                            "angle": 24.3,
                        },
                        "meta": {
                            "z_index": 1,
                            "visible": True,
                            "alpha": 1,
                            "color": "#FE9573",
                        },
                    },
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "9b20fabd-9b33-422b-bbb5-870cfaad31b2",
                    "class_name": "poly",
                    "class_id": "7c6ab4db-5b0c-4143-b992-6dc732f28870",
                    "annotation_type": "polyline",
                    "annotation": {
                        "multiple": True,
                        "coord": {
                            "points": [
                                [
                                    {"x": 20.5, "y": 144.8},
                                    {"x": 40.9, "y": 117.3},
                                    {"x": 40.8, "y": 145.8},
                                ]
                            ]
                        },
                        "meta": {
                            "z_index": 1,
                            "visible": True,
                            "alpha": 1,
                            "color": "#FFAF5A",
                        },
                    },
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "92e28cc4-7eee-4a72-9dc4-383ffd4ecf70",
                    "class_name": "poly_seg",
                    "class_id": "5a122ca5-b827-4896-9476-ab01d5164853",
                    "annotation_type": "polygon",
                    "annotation": {
                        "multiple": True,
                        "coord": {
                            "points": [
                                [
                                    [
                                        {"x": 21.5, "y": 191.2},
                                        {"x": 24.2, "y": 167.7},
                                        {"x": 28.1, "y": 158.1},
                                        {"x": 41.2, "y": 161.9},
                                        {"x": 21.5, "y": 191.2},
                                    ]
                                ]
                            ]
                        },
                        "meta": {
                            "z_index": 1,
                            "visible": True,
                            "alpha": 1,
                            "color": "#FFCC00",
                        },
                    },
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "9ed93108-2c3a-4eba-8613-0633003a239f",
                    "class_name": "face_kp",
                    "class_id": "96007e8f-3c76-4359-88d3-27cc3b2e986f",
                    "annotation_type": "keypoint",
                    "annotation": {
                        "coord": {
                            "points": [
                                {
                                    "name": "left eye center",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "left eye inner corner",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "left eye outer corner",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "right eye center",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "right eye inner corner",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "right eye outer corner",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "left eyebrow inner end",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "left eyebrow outer end",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "right eyebrow inner end",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "right eyebrow outer end",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "nose tip",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "mouth left corner",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "mouth right corner",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "mouth center top lip",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                                {
                                    "name": "mouth center bottom lip",
                                    "x": 0.0,
                                    "y": 0.0,
                                    "state": {"visible": True, "valid": True},
                                },
                            ]
                        },
                        "meta": {
                            "z_index": 1,
                            "visible": True,
                            "alpha": 1,
                            "color": "#FFF73E",
                        },
                    },
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "10a57f9d-3d04-4ce6-aa8f-516300cd8f75",
                    "class_name": "2d_cuboid",
                    "class_id": "e970ec55-2dd7-4a94-8a93-ec2b34ed5005",
                    "annotation_type": "cuboid2d",
                    "annotation": {
                        "coord": {
                            "near": {
                                "x": 15.1,
                                "y": 225.7,
                                "width": 44.9,
                                "height": 37.6,
                            },
                            "far": {
                                "x": 83.2,
                                "y": 239.3,
                                "width": 5.4,
                                "height": 16.5,
                            },
                        },
                        "meta": {
                            "z_index": 1,
                            "visible": True,
                            "alpha": 1,
                            "color": "#DEF00F",
                        },
                    },
                    "properties": [],
                    "tracking_id": None,
                },
            ],
            "categories": {"properties": []},
        },
        "tags": {
            "classes_id": [
                "346c2e59-0d4d-4818-8cd0-538b157fa06c",
                "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                "7c6ab4db-5b0c-4143-b992-6dc732f28870",
                "5a122ca5-b827-4896-9476-ab01d5164853",
                "96007e8f-3c76-4359-88d3-27cc3b2e986f",
                "e970ec55-2dd7-4a94-8a93-ec2b34ed5005",
            ],
            "class": [
                "box",
                "rbox",
                "poly",
                "poly_seg",
                "face_kp",
                "2d_cuboid",
            ],
            "classes_count": [
                {
                    "id": "346c2e59-0d4d-4818-8cd0-538b157fa06c",
                    "name": "box",
                    "count": 1,
                },
                {
                    "id": "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                    "name": "rbox",
                    "count": 1,
                },
                {
                    "id": "7c6ab4db-5b0c-4143-b992-6dc732f28870",
                    "name": "poly",
                    "count": 1,
                },
                {
                    "id": "5a122ca5-b827-4896-9476-ab01d5164853",
                    "name": "poly_seg",
                    "count": 1,
                },
                {
                    "id": "96007e8f-3c76-4359-88d3-27cc3b2e986f",
                    "name": "face_kp",
                    "count": 1,
                },
                {
                    "id": "e970ec55-2dd7-4a94-8a93-ec2b34ed5005",
                    "name": "2d_cuboid",
                    "count": 1,
                },
            ],
            "classes_properties_count": [],
            "categories_id": [],
        },
    }
