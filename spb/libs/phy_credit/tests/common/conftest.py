import pytest


@pytest.fixture
def mock_image_objects_with_properties():
    return [
        {
            "id": "aaa",
            "class_id": "car-id",
            "class_name": "Car",
            "annotation_type": "box",
            "annotation": {},
            "properties": [
                {
                    "property_id": "Car-color-id",
                    "property_name": "Color",
                    "option_id": "Silver-id",
                    "option_name": "Silver",
                    "type": "radio",
                },
                {
                    "property_id": "Car-color-id",
                    "property_name": "Color",
                    "option_id": "Silver-id",
                    "option_name": "Silver",
                    "type": "radio",
                },
                {
                    "property_id": "Car-color-id",
                    "property_name": "Color",
                    "option_id": "Navy-id",
                    "option_name": "Navy",
                    "type": "radio",
                },
                {
                    "property_id": "Car-color-id",
                    "property_name": "Color",
                    "option_id": "White-id",
                    "option_name": "White",
                    "type": "radio",
                },
                {
                    "property_id": "Car-description-id",
                    "property_name": "Car Description",
                    "value": "This is a sports car",
                    "type": "free response",
                },
            ],
        },
        {
            "id": "bbb",
            "class_id": "car-id",
            "class_name": "Car",
            "annotation_type": "box",
            "annotation": {},
            "properties": [
                {
                    "property_id": "Car-color-id",
                    "property_name": "Color",
                    "option_id": "Silver-id",
                    "option_name": "Silver",
                    "type": "radio",
                },
                {
                    "property_id": "Car-color-id",
                    "property_name": "Color",
                    "option_id": "White-id",
                    "option_name": "White",
                    "type": "radio",
                },
                {
                    "property_id": "Car-description-id",
                    "property_name": "Car Description",
                    "value": "This is a sports car",
                    "type": "free response",
                },
            ],
        },
    ]


@pytest.fixture
def mock_image_classes_properties_count():
    return [
        {
            "class_id": "car-id",
            "property_id": "Car-color-id",
            "property_name": "Color",
            "option_id": "Silver-id",
            "option_name": "Silver",
            "property_option_id": "Car-color-id#Silver-id",
            "count": 3,
        },
        {
            "class_id": "car-id",
            "property_id": "Car-color-id",
            "property_name": "Color",
            "option_id": "Navy-id",
            "option_name": "Navy",
            "property_option_id": "Car-color-id#Navy-id",
            "count": 1,
        },
        {
            "class_id": "car-id",
            "property_id": "Car-color-id",
            "property_name": "Color",
            "option_id": "White-id",
            "option_name": "White",
            "property_option_id": "Car-color-id#White-id",
            "count": 2,
        },
    ]


@pytest.fixture
def mock_preprocessed_properties():
    return [
        {
            "class_id": "person-id",
            "option_id": "female-id",
            "option_name": "Female",
            "property_id": "gender-id",
            "property_name": "Gender",
            "property_option_id": "gender-id#female-id",
        },
        {
            "class_id": "person-id",
            "option_id": "female-id",
            "option_name": "Female",
            "property_id": "gender-id",
            "property_name": "Gender",
            "property_option_id": "gender-id#female-id",
        },
        {
            "class_id": "person-id",
            "option_id": "male-id",
            "option_name": "Male",
            "property_id": "gender-id",
            "property_name": "Gender",
            "property_option_id": "gender-id#male-id",
        },
        {
            "class_id": "person-id",
            "option_id": "true-id",
            "option_name": "True",
            "property_id": "occluded-id",
            "property_name": "Occluded",
            "property_option_id": "occluded-id#true-id",
        },
        {
            "class_id": "person-id",
            "option_id": "false-id",
            "option_name": "False",
            "property_id": "occluded-id",
            "property_name": "Occluded",
            "property_option_id": "occluded-id#false-id",
        },
        {
            "class_id": "person-id",
            "option_id": "false-id",
            "option_name": "False",
            "property_id": "occluded-id",
            "property_name": "Occluded",
            "property_option_id": "occluded-id#false-id",
        },
        {
            "class_id": "person-id",
            "option_id": "false-id",
            "option_name": "False",
            "property_id": "occluded-id",
            "property_name": "Occluded",
            "property_option_id": "occluded-id#false-id",
        },
    ]


@pytest.fixture
def mock_count_properties_result():
    return [
        {
            "class_id": "person-id",
            "option_id": "female-id",
            "option_name": "Female",
            "property_id": "gender-id",
            "property_name": "Gender",
            "property_option_id": "gender-id#female-id",
            "count": 2,
        },
        {
            "class_id": "person-id",
            "option_id": "male-id",
            "option_name": "Male",
            "property_id": "gender-id",
            "property_name": "Gender",
            "property_option_id": "gender-id#male-id",
            "count": 1,
        },
        {
            "class_id": "person-id",
            "option_id": "true-id",
            "option_name": "True",
            "property_id": "occluded-id",
            "property_name": "Occluded",
            "property_option_id": "occluded-id#true-id",
            "count": 1,
        },
        {
            "class_id": "person-id",
            "option_id": "false-id",
            "option_name": "False",
            "property_id": "occluded-id",
            "property_name": "Occluded",
            "property_option_id": "occluded-id#false-id",
            "count": 3,
        },
    ]


@pytest.fixture
def num_properties_flattened():
    return 18


@pytest.fixture
def num_properties_removed_free_response():
    return 10


@pytest.fixture
def num_properties_expanded_options():
    return 14


@pytest.fixture
def num_properties_preprocessed():
    return 14


@pytest.fixture
def mock_video_classes_properties_count():
    return [
        {
            "class_id": "f1e62c91-7241-4d42-8e6c-5a4f79f09b3f",
            "property_id": "ad7647bd-f2a9-4ab4-9ca1-5b7600acfd78",
            "property_name": "Person Subclass",
            "option_id": "627f7de4-5a11-4a98-8618-6ea3439020f3",
            "option_name": "Unknown",
            "property_option_id": "ad7647bd-f2a9-4ab4-9ca1-5b7600acfd78#627f7de4-5a11-4a98-8618-6ea3439020f3",
            "count": 1,
        },
        {
            "class_id": "f1e62c91-7241-4d42-8e6c-5a4f79f09b3f",
            "property_id": "ad7647bd-f2a9-4ab4-9ca1-5b7600acfd78",
            "property_name": "Person Subclass",
            "option_id": "cfd5be2e-695f-468d-8e98-182769728920",
            "option_name": "Client",
            "property_option_id": "ad7647bd-f2a9-4ab4-9ca1-5b7600acfd78#cfd5be2e-695f-468d-8e98-182769728920",
            "count": 1,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a",
            "property_name": "Mood(PF)",
            "option_id": "1",
            "option_name": "Sad",
            "property_option_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a#1",
            "count": 3,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a",
            "property_name": "Mood(PF)",
            "option_id": "2",
            "option_name": "Happy",
            "property_option_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a#2",
            "count": 2,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a",
            "property_name": "Mood(PF)",
            "option_id": "3",
            "option_name": "Thoughtful",
            "property_option_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a#3",
            "count": 2,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "fc5cb926-8b6a-443f-8d67-426478f4056f",
            "property_name": "Truncated(PF)",
            "option_id": "1",
            "option_name": "T",
            "property_option_id": "fc5cb926-8b6a-443f-8d67-426478f4056f#1",
            "count": 1,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "57d8115c-7a44-45ae-98c6-eb4b2fb9b710",
            "property_name": "Mood",
            "option_id": "3",
            "option_name": "Sad",
            "property_option_id": "57d8115c-7a44-45ae-98c6-eb4b2fb9b710#3",
            "count": 1,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "38a1be62-42c2-4c55-b793-136b8c147615",
            "property_name": "Truncated",
            "option_id": "1",
            "option_name": "Yes",
            "property_option_id": "38a1be62-42c2-4c55-b793-136b8c147615#1",
            "count": 1,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "df27390a-4f0c-40c7-9f0f-bacf999cdaee",
            "property_name": "Size",
            "option_id": "3",
            "option_name": "S",
            "property_option_id": "df27390a-4f0c-40c7-9f0f-bacf999cdaee#3",
            "count": 1,
        },
        {
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "property_id": "c58fe3d6-1693-4995-8e8f-7929b484da1b",
            "property_name": "Occluded",
            "option_id": "1",
            "option_name": "True",
            "property_option_id": "c58fe3d6-1693-4995-8e8f-7929b484da1b#1",
            "count": 1,
        },
    ]


@pytest.fixture
def mock_video_objects():
    return [
        {
            "annotation_type": "keypoint",
            "class_id": "f1e62c91-7241-4d42-8e6c-5a4f79f09b3f",
            "class_name": "Person",
            "frames": [
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                {
                                    "name": "left eye inner corner",
                                    "state": {"valid": True, "visible": True},
                                    "x": 325.8487177544785,
                                    "y": 129.9350831305714,
                                },
                            ]
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#6648FF",
                            "visible": True,
                            "z_index": 1,
                        },
                    },
                    "num": 0,
                    "properties": [],
                },
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                {
                                    "name": "left eye center",
                                    "state": {"valid": True, "visible": True},
                                    "x": 319.4920928160841,
                                    "y": 126.31307461866575,
                                },
                                {
                                    "name": "left eye inner corner",
                                    "state": {"valid": True, "visible": True},
                                    "x": 325.8487177544785,
                                    "y": 129.9350831305714,
                                },
                                {
                                    "name": "left eye outer corner",
                                    "state": {"valid": True, "visible": True},
                                    "x": 319.15317630532724,
                                    "y": 134.61523555774093,
                                },
                                {
                                    "name": "right eye center",
                                    "state": {"valid": True, "visible": True},
                                    "x": 317.62934558138977,
                                    "y": 155.76259096939575,
                                },
                            ]
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#6648FF",
                            "visible": True,
                            "z_index": 1,
                        },
                    },
                    "num": 1,
                    "properties": [],
                },
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                {
                                    "name": "nose tip",
                                    "state": {"valid": True, "visible": True},
                                    "x": 328.9325992874725,
                                    "y": 227.90782622868213,
                                },
                            ]
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#6648FF",
                            "visible": True,
                            "z_index": 1,
                        },
                    },
                    "num": 2,
                    "properties": [],
                },
            ],
            "id": "fee81b6a-8ad2-46c7-819c-89781c730519",
            "properties": [
                {
                    "option_id": "627f7de4-5a11-4a98-8618-6ea3439020f3",
                    "option_name": "Unknown",
                    "property_id": "ad7647bd-f2a9-4ab4-9ca1-5b7600acfd78",
                    "property_name": "Person Subclass",
                    "type": "radio",
                }
            ],
            "tracking_id": 1,
        },
        {
            "annotation_type": "polygon",
            "class_id": "8c0dea92-bbdc-418f-bfa8-86ca249c0b73",
            "class_name": "Grocery Bag",
            "frames": [
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                [
                                    [
                                        {"x": 547.7251977470074,
                                            "y": 16.268694580160915},
                                        {"x": 576.028607118613,
                                            "y": 45.32496429245545},
                                        {"x": 547.7251977470074,
                                            "y": 16.268694580160915},
                                    ]
                                ]
                            ]
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#FE9573",
                            "visible": True,
                            "z_index": 2,
                        },
                        "multiple": True,
                    },
                    "num": 0,
                    "properties": [],
                },
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                [
                                    [
                                        {"x": 547.7251977470074,
                                            "y": 16.268694580160915},
                                        {"x": 546.3928160444136,
                                            "y": 17.958102836071195},
                                        {"x": 547.7251977470074,
                                            "y": 16.268694580160915},
                                    ]
                                ]
                            ]
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#FE9573",
                            "visible": True,
                            "z_index": 2,
                        },
                        "multiple": True,
                    },
                    "num": 2,
                    "properties": [],
                },
            ],
            "id": "1af98de3-d356-410a-86c8-3a7b71411575",
            "properties": [],
            "tracking_id": 2,
        },
        {
            "annotation_type": "keypoint",
            "class_id": "f1e62c91-7241-4d42-8e6c-5a4f79f09b3f",
            "class_name": "Person",
            "frames": [
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                {
                                    "name": "nose tip",
                                    "state": {"valid": False, "visible": False},
                                    "x": None,
                                    "y": None,
                                },
                                {
                                    "name": "mouth left corner",
                                    "state": {"valid": False, "visible": False},
                                    "x": None,
                                    "y": None,
                                },
                            ]
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#6648FF",
                            "visible": True,
                            "z_index": 3,
                        },
                    },
                    "num": 0,
                    "properties": [],
                },
                {
                    "annotation": {
                        "coord": {
                            "points": [
                                {
                                    "name": "nose tip",
                                    "state": {"valid": False, "visible": False},
                                    "x": None,
                                    "y": None,
                                },
                                {
                                    "name": "mouth left corner",
                                    "state": {"valid": False, "visible": False},
                                    "x": None,
                                    "y": None,
                                },
                            ]
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#6648FF",
                            "visible": True,
                            "z_index": 3,
                        },
                    },
                    "num": 2,
                    "properties": [],
                },
            ],
            "id": "a452943e-bb5e-4c40-8d34-0e322d7f4bf6",
            "properties": [
                {
                    "option_id": "cfd5be2e-695f-468d-8e98-182769728920",
                    "option_name": "Client",
                    "property_id": "ad7647bd-f2a9-4ab4-9ca1-5b7600acfd78",
                    "property_name": "Person Subclass",
                    "type": "radio",
                }
            ],
            "tracking_id": 3,
        },
        {
            "annotation_type": "box",
            "class_id": "88164746-1f8b-4730-8aec-ebd089cbe9d6",
            "class_name": "Penguin",
            "frames": [
                {
                    "annotation": {
                        "coord": {
                            "height": 52.03273942246172,
                            "width": 32.07547252186159,
                            "x": 39.730742505428886,
                            "y": 52.91824642277193,
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#39F8F8",
                            "visible": True,
                            "z_index": 4,
                        },
                    },
                    "num": 0,
                    "properties": [
                        {
                            "option_ids": ["1", "2", "3"],
                            "option_names": ["Sad", "Happy", "Thoughtful"],
                            "property_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a",
                            "property_name": "Mood(PF)",
                            "type": "checkbox",
                        },
                        {
                            "property_id": "82f0f333-5247-4d3f-bd42-d03b8e914f10",
                            "property_name": "Is area crowded",
                            "type": "free response",
                            "value": "",
                        },
                        {
                            "property_id": "93c6434d-af9c-42b4-999c-911c43b72bb6",
                            "property_name": "Is area cluttered",
                            "type": "free response",
                            "value": "",
                        },
                    ],
                },
                {
                    "annotation": {
                        "coord": {
                            "height": 52.03273942246172,
                            "width": 32.07547252186159,
                            "x": 39.730742505428886,
                            "y": 52.91824642277193,
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#39F8F8",
                            "visible": True,
                            "z_index": 4,
                        },
                    },
                    "num": 1,
                    "properties": [
                        {
                            "option_ids": ["1"],
                            "option_names": ["Sad"],
                            "property_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a",
                            "property_name": "Mood(PF)",
                            "type": "checkbox",
                        },
                        {
                            "property_id": "82f0f333-5247-4d3f-bd42-d03b8e914f10",
                            "property_name": "Is area crowded",
                            "type": "free response",
                            "value": "",
                        },
                        {
                            "property_id": "93c6434d-af9c-42b4-999c-911c43b72bb6",
                            "property_name": "Is area cluttered",
                            "type": "free response",
                            "value": "",
                        },
                    ],
                },
                {
                    "annotation": {
                        "coord": {
                            "height": 52.03273942246172,
                            "width": 32.07547252186159,
                            "x": 39.730742505428886,
                            "y": 52.91824642277193,
                        },
                        "meta": {
                            "alpha": 1,
                            "color": "#39F8F8",
                            "visible": True,
                            "z_index": 4,
                        },
                    },
                    "num": 2,
                    "properties": [
                        {
                            "option_ids": ["1", "2", "3"],
                            "option_names": ["Sad", "Happy", "Thoughtful"],
                            "property_id": "ac3bc093-810a-4491-9fc9-3592213aaf3a",
                            "property_name": "Mood(PF)",
                            "type": "checkbox",
                        },
                        {
                            "property_id": "82f0f333-5247-4d3f-bd42-d03b8e914f10",
                            "property_name": "Is area crowded",
                            "type": "free response",
                            "value": "yes",
                        },
                        {
                            "property_id": "93c6434d-af9c-42b4-999c-911c43b72bb6",
                            "property_name": "Is area cluttered",
                            "type": "free response",
                            "value": "0",
                        },
                        {
                            "option_id": "1",
                            "option_name": "T",
                            "property_id": "fc5cb926-8b6a-443f-8d67-426478f4056f",
                            "property_name": "Truncated(PF)",
                            "type": "radio",
                        },
                    ],
                },
            ],
            "id": "a518d610-cd99-4975-ae17-6c1a081aeeb1",
            "properties": [
                {
                    "option_ids": ["3"],
                    "option_names": ["Sad"],
                    "property_id": "57d8115c-7a44-45ae-98c6-eb4b2fb9b710",
                    "property_name": "Mood",
                    "type": "checkbox",
                },
                {
                    "property_id": "d099a83f-12e0-423c-a9be-4f1dbd221690",
                    "property_name": "Describe mood",
                    "type": "free response",
                    "value": "",
                },
                {
                    "option_id": "1",
                    "option_name": "Yes",
                    "property_id": "38a1be62-42c2-4c55-b793-136b8c147615",
                    "property_name": "Truncated",
                    "type": "radio",
                },
                {
                    "option_ids": ["3"],
                    "option_names": ["S"],
                    "property_id": "df27390a-4f0c-40c7-9f0f-bacf999cdaee",
                    "property_name": "Size",
                    "type": "checkbox",
                },
                {
                    "property_id": "06bb4da1-d8fd-475b-ad2f-4d4b8b94fb8d",
                    "property_name": "Describe colors",
                    "type": "free response",
                    "value": "1",
                },
                {
                    "option_id": "1",
                    "option_name": "True",
                    "property_id": "c58fe3d6-1693-4995-8e8f-7929b484da1b",
                    "property_name": "Occluded",
                    "type": "radio",
                },
            ],
            "tracking_id": 4,
        },
    ]
