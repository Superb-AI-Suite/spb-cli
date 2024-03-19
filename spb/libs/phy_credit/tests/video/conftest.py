import pytest


@pytest.fixture
def label_interface_sample():
    return {
        "version": "0.1.0",
        "data_type": "image sequence",
        "categorization": {"properties": []},
        "object_tracking": {
            "keypoints": [],
            "object_groups": [],
            "object_classes": [
                {
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                    "color": "#FF625A",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [
                        {"class_ids": ["1"], "engine_id": "co_20200526"}
                    ],
                    "annotation_type": "box",
                },
                {
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
                    "color": "#FE9573",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [{"class_ids": [], "engine_id": ""}],
                    "annotation_type": "polygon",
                },
            ],
            "annotation_types": ["box", "polygon"],
        },
    }


@pytest.fixture
def add_object_1():
    return {
        "tracking_id": 1,
        "class_name": "Person",
        "annotations": [
            {
                "frame_num": 0,
                "coord": {
                    "x": 1245.1356238698008,
                    "y": 355.4430379746835,
                    "width": 232.40506329113896,
                    "height": 482.386980108499,
                },
            },
            {
                "frame_num": 1,
                "coord": {
                    "x": 1032.2603978300176,
                    "y": 421.8444846292944,
                    "width": 199.20433996383372,
                    "height": 410.1265822784811,
                },
            },
        ],
    }


@pytest.fixture
def add_object_2():
    return {
        "tracking_id": 1,
        "class_name": "Person",
        "annotations": [
            {
                "frame_num": 0,
                "coord": {
                    "x": 1245.1356238698008,
                    "y": 355.4430379746835,
                    "width": 232.40506329113896,
                    "height": 482.386980108499,
                },
            },
            {
                "frame_num": 1,
                "coord": {
                    "x": 1032.2603978300176,
                    "y": 421.8444846292944,
                    "width": 199.20433996383372,
                    "height": 410.1265822784811,
                },
            },
        ],
    }


@pytest.fixture
def sample_tag_result_scratch():
    return {
        "class": ["Person"],
        "classes_annotation_count": [
            {
                "count": 4,
                "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "name": "Person",
            }
        ],
        "classes_count": [
            {
                "count": 2,
                "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "name": "Person",
            }
        ],
        "classes_id": ["f9c75f80-1f2d-45ef-875e-bbe5f49e56ff"],
    }


@pytest.fixture
def sample_info_result_scratch():
    return {
        "meta": {
            "editInfo": {
                "objects": [
                    {
                        "color": "#FF625A",
                        "id": "46a8b7c7-b94c-4118-afdf-5411feb0dcc4",
                        "selected": False,
                        "trackingId": 1,
                        "visible": True,
                    },
                    {
                        "color": "#FF625A",
                        "id": "acbc877b-b555-4336-8197-d87eb9cbab52",
                        "selected": False,
                        "trackingId": 1,
                        "visible": True,
                    },
                ]
            },
            "imageInfo": {},
        },
        "result": {
            "categories": {"frames": [], "properties": []},
            "objects": [
                {
                    "annotationType": "box",
                    "classId": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "className": "Person",
                    "frames": [
                        {
                            "annotation": {
                                "coord": {
                                    "height": 482.386980108499,
                                    "width": 232.40506329113896,
                                    "x": 1245.1356238698008,
                                    "y": 355.4430379746835,
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 0,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "height": 410.1265822784811,
                                    "width": 199.20433996383372,
                                    "x": 1032.2603978300176,
                                    "y": 421.8444846292944,
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 1,
                            "properties": [],
                        },
                    ],
                    "id": "46a8b7c7-b94c-4118-afdf-5411feb0dcc4",
                    "properties": [],
                    "trackingId": 1,
                },
                {
                    "annotationType": "box",
                    "classId": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "className": "Person",
                    "frames": [
                        {
                            "annotation": {
                                "coord": {
                                    "height": 482.386980108499,
                                    "width": 232.40506329113896,
                                    "x": 1245.1356238698008,
                                    "y": 355.4430379746835,
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 0,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "height": 410.1265822784811,
                                    "width": 199.20433996383372,
                                    "x": 1032.2603978300176,
                                    "y": 421.8444846292944,
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 1,
                            "properties": [],
                        },
                    ],
                    "id": "acbc877b-b555-4336-8197-d87eb9cbab52",
                    "properties": [],
                    "trackingId": 1,
                },
            ],
        },
        "tags": {
            "class": ["Person"],
            "classes_annotation_count": [
                {
                    "count": 4,
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                }
            ],
            "classes_count": [
                {
                    "count": 2,
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                }
            ],
            "classes_id": ["f9c75f80-1f2d-45ef-875e-bbe5f49e56ff"],
        },
        "version": "0.3.1-py",
    }


@pytest.fixture
def sample_tag_result():
    return {
        "class": ["Person", "Chair"],
        "classes_annotation_count": [
            {
                "count": 3,
                "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "name": "Person",
            },
            {
                "count": 2,
                "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                "name": "Chair",
            },
        ],
        "classes_count": [
            {
                "count": 1,
                "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "name": "Person",
            },
            {
                "count": 2,
                "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                "name": "Chair",
            },
        ],
        "classes_id": [
            "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
            "1c4c4891-9382-496d-8895-a004d488b38e",
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
                        "id": "13ff1526-370e-4db6-8fae-aa387cb34c3c",
                        "selected": False,
                        "trackingId": 1,
                        "visible": True,
                    },
                    {
                        "color": "#FE9573",
                        "id": "86698a96-3dcb-422b-b73b-435e72b068d4",
                        "selected": False,
                        "trackingId": 2,
                        "visible": True,
                    },
                    {
                        "color": "#FE9573",
                        "id": "3f0d4d21-43fe-45d8-82fe-4ee3b83744a7",
                        "selected": False,
                        "trackingId": 3,
                        "visible": True,
                    },
                ]
            },
            "imageInfo": {},
        },
        "result": {
            "categories": {"frames": [], "properties": []},
            "objects": [
                {
                    "annotationType": "box",
                    "classId": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "className": "Person",
                    "frames": [
                        {
                            "annotation": {
                                "coord": {
                                    "height": 472.62206148282087,
                                    "width": 218.7341772151899,
                                    "x": 1260.7594936708856,
                                    "y": 369.1139240506328,
                                },
                                "meta": {},
                            },
                            "num": 0,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "height": 423.7974683544303,
                                    "width": 195.2983725135623,
                                    "x": 1036.166365280289,
                                    "y": 415.9855334538878,
                                },
                                "meta": {},
                            },
                            "num": 1,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "height": 423.7974683544303,
                                    "width": 195.2983725135623,
                                    "x": 1036.166365280289,
                                    "y": 415.9855334538878,
                                },
                                "meta": {},
                            },
                            "num": 3,
                            "properties": [],
                        },
                    ],
                    "id": "13ff1526-370e-4db6-8fae-aa387cb34c3c",
                    "properties": [],
                    "trackingId": 1,
                },
                {
                    "annotationType": "polygon",
                    "classId": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "className": "Chair",
                    "frames": [
                        {
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "x": 727.5949367088607,
                                            "y": 199.2043399638336,
                                        },
                                        {
                                            "x": 725.641952983725,
                                            "y": 302.71247739602165,
                                        },
                                        {
                                            "x": 704.1591320072331,
                                            "y": 308.5714285714285,
                                        },
                                        {
                                            "x": 764.7016274864374,
                                            "y": 337.86618444846283,
                                        },
                                        {
                                            "x": 760.7956600361662,
                                            "y": 363.254972875226,
                                        },
                                        {
                                            "x": 942.4231464737792,
                                            "y": 345.6781193490053,
                                        },
                                        {
                                            "x": 874.0687160940323,
                                            "y": 304.66546112115725,
                                        },
                                        {
                                            "x": 930.7052441229654,
                                            "y": 253.88788426763105,
                                        },
                                        {
                                            "x": 827.1971066907773,
                                            "y": 199.2043399638336,
                                        },
                                    ]
                                },
                                "meta": {},
                            },
                            "num": 0,
                            "properties": [],
                        }
                    ],
                    "id": "86698a96-3dcb-422b-b73b-435e72b068d4",
                    "properties": [],
                    "trackingId": 2,
                },
                {
                    "annotationType": "polygon",
                    "classId": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "className": "Chair",
                    "frames": [
                        {
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "x": 744.4354838709677,
                                            "y": 479.0322580645161,
                                        },
                                        {
                                            "x": 594.1935483870967,
                                            "y": 670.6451612903226,
                                        },
                                        {
                                            "x": 936.0483870967743,
                                            "y": 757.7419354838709,
                                        },
                                        {
                                            "x": 942.5806451612904,
                                            "y": 733.7903225806451,
                                        },
                                        {"x": 1007.9032258064516, "y": 540},
                                    ]
                                },
                                "meta": {},
                            },
                            "num": 7,
                            "properties": [],
                        }
                    ],
                    "id": "3f0d4d21-43fe-45d8-82fe-4ee3b83744a7",
                    "properties": [],
                    "trackingId": 3,
                },
            ],
        },
        "tags": {
            "class": ["Person", "Chair"],
            "classes_annotation_count": [
                {
                    "count": 3,
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                },
                {
                    "count": 2,
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
                },
            ],
            "classes_count": [
                {
                    "count": 1,
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                },
                {
                    "count": 2,
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
                },
            ],
            "classes_id": [
                "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "1c4c4891-9382-496d-8895-a004d488b38e",
            ],
        },
        "version": "0.3.1-py",
    }


@pytest.fixture
def sample_build_result():
    return {
        "objects": [
            {
                "id": "13ff1526-370e-4db6-8fae-aa387cb34c3c",
                "trackingId": 1,
                "classId": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "className": "Person",
                "annotationType": "box",
                "properties": [],
                "frames": [
                    {
                        "num": 0,
                        "annotation": {
                            "coord": {
                                "x": 1260.7594936708856,
                                "y": 369.1139240506328,
                                "width": 218.7341772151899,
                                "height": 472.62206148282087,
                            },
                            "meta": {},
                        },
                        "properties": [],
                    },
                    {
                        "num": 1,
                        "annotation": {
                            "coord": {
                                "x": 1036.166365280289,
                                "y": 415.9855334538878,
                                "width": 195.2983725135623,
                                "height": 423.7974683544303,
                            },
                            "meta": {},
                        },
                        "properties": [],
                    },
                    {
                        "num": 3,
                        "annotation": {
                            "coord": {
                                "x": 1036.166365280289,
                                "y": 415.9855334538878,
                                "width": 195.2983725135623,
                                "height": 423.7974683544303,
                            },
                            "meta": {},
                        },
                        "properties": [],
                    },
                ],
            },
            {
                "id": "86698a96-3dcb-422b-b73b-435e72b068d4",
                "trackingId": 2,
                "classId": "1c4c4891-9382-496d-8895-a004d488b38e",
                "className": "Chair",
                "annotationType": "polygon",
                "properties": [],
                "frames": [
                    {
                        "num": 0,
                        "annotation": {
                            "coord": {
                                "points": [
                                    {
                                        "x": 727.5949367088607,
                                        "y": 199.2043399638336,
                                    },
                                    {
                                        "x": 725.641952983725,
                                        "y": 302.71247739602165,
                                    },
                                    {
                                        "x": 704.1591320072331,
                                        "y": 308.5714285714285,
                                    },
                                    {
                                        "x": 764.7016274864374,
                                        "y": 337.86618444846283,
                                    },
                                    {
                                        "x": 760.7956600361662,
                                        "y": 363.254972875226,
                                    },
                                    {
                                        "x": 942.4231464737792,
                                        "y": 345.6781193490053,
                                    },
                                    {
                                        "x": 874.0687160940323,
                                        "y": 304.66546112115725,
                                    },
                                    {
                                        "x": 930.7052441229654,
                                        "y": 253.88788426763105,
                                    },
                                    {
                                        "x": 827.1971066907773,
                                        "y": 199.2043399638336,
                                    },
                                ]
                            },
                            "meta": {},
                        },
                        "properties": [],
                    }
                ],
            },
            {
                "id": "3f0d4d21-43fe-45d8-82fe-4ee3b83744a7",
                "trackingId": 3,
                "classId": "1c4c4891-9382-496d-8895-a004d488b38e",
                "className": "Chair",
                "annotationType": "polygon",
                "properties": [],
                "frames": [
                    {
                        "num": 7,
                        "annotation": {
                            "coord": {
                                "points": [
                                    {
                                        "x": 744.4354838709677,
                                        "y": 479.0322580645161,
                                    },
                                    {
                                        "x": 594.1935483870967,
                                        "y": 670.6451612903226,
                                    },
                                    {
                                        "x": 936.0483870967743,
                                        "y": 757.7419354838709,
                                    },
                                    {
                                        "x": 942.5806451612904,
                                        "y": 733.7903225806451,
                                    },
                                    {"x": 1007.9032258064516, "y": 540},
                                ]
                            },
                            "meta": {},
                        },
                        "properties": [],
                    }
                ],
            },
        ],
        "categories": {"properties": [], "frames": []},
    }


@pytest.fixture
def label_interface_sample_w_properties():
    return {
        "version": "0.4.6",
        "data_type": "image sequence",
        "categorization": {"properties": []},
        "object_tracking": {
            "keypoints": [],
            "object_groups": [],
            "object_classes": [
                {
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                    "color": "#FF625A",
                    "properties": [
                        {
                            "id": "63fe0ee1-2a21-40b8-a0cd-4ac06e9093a4",
                            "name": "identifiable",
                            "type": "radio",
                            "options": [
                                {"id": "2", "name": "True"},
                                {
                                    "id": "d482ea4c-1424-42e7-9c02-277a1a20b75f",
                                    "name": "False",
                                },
                            ],
                            "required": True,
                            "per_frame": False,
                            "description": "",
                            "render_value": False,
                            "default_value": "2",
                        },
                        {
                            "id": "9784c05a-00b6-4527-9b39-0b5e4e506176",
                            "name": "accessories",
                            "type": "checkbox",
                            "options": [
                                {"id": "3", "name": "hat"},
                                {"id": "4", "name": "bag"},
                            ],
                            "required": False,
                            "per_frame": False,
                            "description": "",
                            "render_value": False,
                            "default_value": [],
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [
                        {"class_ids": ["1"], "engine_id": "co_20200526"}
                    ],
                    "annotation_type": "box",
                },
                {
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
                    "color": "#FE9573",
                    "properties": [
                        {
                            "id": "f10903ce-2112-423f-adaf-c5042dc0f17e",
                            "name": "color",
                            "type": "free response",
                            "blank": False,
                            "per_frame": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True,
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": "",
                        }
                    ],
                    "constraints": {},
                    "ai_class_map": [{"class_ids": [], "engine_id": ""}],
                    "annotation_type": "polygon",
                },
            ],
            "annotation_types": ["box", "polygon"],
        },
    }


@pytest.fixture
def add_object_w_properties_1():
    return {
        "tracking_id": 1,
        "class_name": "Person",
        "annotations": [
            {
                "frame_num": 0,
                "coord": {
                    "x": 1245.1356238698008,
                    "y": 355.4430379746835,
                    "width": 232.40506329113896,
                    "height": 482.386980108499,
                },
            },
            {
                "frame_num": 1,
                "coord": {
                    "x": 1032.2603978300176,
                    "y": 421.8444846292944,
                    "width": 199.20433996383372,
                    "height": 410.1265822784811,
                },
            },
        ],
        "properties": [
            {"name": "identifiable", "value": "True"},
            {"name": "accessories", "value": ["hat", "bag"]},
        ],
    }


@pytest.fixture
def add_object_w_properties_2():
    return {
        "tracking_id": 2,
        "class_name": "Chair",
        "annotations": [
            {
                "frame_num": 0,
                "coord": {
                    "points": [
                        {"x": 723.6889692585893, "y": 207.0162748643761},
                        {"x": 737.3598553345388, "y": 312.47739602169975},
                        {"x": 706.1121157323688, "y": 310.52441229656415},
                        {"x": 739.3128390596743, "y": 341.7721518987341},
                        {"x": 737.3598553345388, "y": 363.254972875226},
                        {"x": 883.8336347197104, "y": 357.3960216998191},
                        {"x": 876.021699819168, "y": 322.2423146473779},
                        {"x": 911.1754068716092, "y": 273.41772151898726},
                        {"x": 838.9150090415911, "y": 298.8065099457504},
                        {"x": 807.6672694394211, "y": 191.3924050632911},
                    ]
                },
            },
            {
                "frame_num": 1,
                "coord": {
                    "points": [
                        {"x": 723.6889692585893, "y": 207.0162748643761},
                        {"x": 737.3598553345388, "y": 312.47739602169975},
                        {"x": 706.1121157323688, "y": 310.52441229656415},
                        {"x": 739.3128390596743, "y": 341.7721518987341},
                        {"x": 737.3598553345388, "y": 363.254972875226},
                        {"x": 883.8336347197104, "y": 357.3960216998191},
                        {"x": 876.021699819168, "y": 322.2423146473779},
                        {"x": 911.1754068716092, "y": 273.41772151898726},
                        {"x": 838.9150090415911, "y": 298.8065099457504},
                        {"x": 807.6672694394211, "y": 191.3924050632911},
                    ]
                },
            },
            {
                "frame_num": 7,
                "coord": {
                    "points": [
                        {"x": 723.6889692585893, "y": 207.0162748643761},
                        {"x": 737.3598553345388, "y": 312.47739602169975},
                        {"x": 706.1121157323688, "y": 310.52441229656415},
                        {"x": 739.3128390596743, "y": 341.7721518987341},
                        {"x": 737.3598553345388, "y": 363.254972875226},
                        {"x": 883.8336347197104, "y": 357.3960216998191},
                        {"x": 876.021699819168, "y": 322.2423146473779},
                        {"x": 911.1754068716092, "y": 273.41772151898726},
                        {"x": 838.9150090415911, "y": 298.8065099457504},
                        {"x": 807.6672694394211, "y": 191.3924050632911},
                    ]
                },
            },
            {
                "frame_num": 9,
                "coord": {
                    "points": [
                        {"x": 723.6889692585893, "y": 207.0162748643761},
                        {"x": 737.3598553345388, "y": 312.47739602169975},
                        {"x": 706.1121157323688, "y": 310.52441229656415},
                        {"x": 739.3128390596743, "y": 341.7721518987341},
                        {"x": 737.3598553345388, "y": 363.254972875226},
                        {"x": 883.8336347197104, "y": 357.3960216998191},
                        {"x": 876.021699819168, "y": 322.2423146473779},
                        {"x": 911.1754068716092, "y": 273.41772151898726},
                        {"x": 838.9150090415911, "y": 298.8065099457504},
                        {"x": 807.6672694394211, "y": 191.3924050632911},
                    ]
                },
            },
            {
                "frame_num": 10,
                "coord": {
                    "points": [
                        {"x": 723.6889692585893, "y": 207.0162748643761},
                        {"x": 737.3598553345388, "y": 312.47739602169975},
                        {"x": 706.1121157323688, "y": 310.52441229656415},
                        {"x": 739.3128390596743, "y": 341.7721518987341},
                        {"x": 737.3598553345388, "y": 363.254972875226},
                        {"x": 883.8336347197104, "y": 357.3960216998191},
                        {"x": 876.021699819168, "y": 322.2423146473779},
                        {"x": 911.1754068716092, "y": 273.41772151898726},
                        {"x": 838.9150090415911, "y": 298.8065099457504},
                        {"x": 807.6672694394211, "y": 191.3924050632911},
                    ]
                },
            },
        ],
        "properties": [{"name": "color", "value": "beige", "type": "radio"}],
    }


@pytest.fixture
def sample_tag_result_w_properties():
    return {
        "annotated_frame_count": 5,
        "categories_id": [],
        "class": ["Person", "Chair"],
        "classes_annotation_count": [
            {
                "count": 2,
                "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "name": "Person",
            },
            {
                "count": 5,
                "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                "name": "Chair",
            },
        ],
        "classes_count": [
            {
                "count": 1,
                "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "name": "Person",
            },
            {
                "count": 1,
                "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                "name": "Chair",
            },
        ],
        "classes_id": [
            "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
            "1c4c4891-9382-496d-8895-a004d488b38e",
        ],
        "classes_properties_count": [
            {
                "class_id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "count": 1,
                "option_id": "2",
                "option_name": "True",
                "property_id": "63fe0ee1-2a21-40b8-a0cd-4ac06e9093a4",
                "property_name": "identifiable",
                "property_option_id": "63fe0ee1-2a21-40b8-a0cd-4ac06e9093a4#2",
            },
            {
                "class_id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "count": 1,
                "option_id": "3",
                "option_name": "hat",
                "property_id": "9784c05a-00b6-4527-9b39-0b5e4e506176",
                "property_name": "accessories",
                "property_option_id": "9784c05a-00b6-4527-9b39-0b5e4e506176#3",
            },
            {
                "class_id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "count": 1,
                "option_id": "4",
                "option_name": "bag",
                "property_id": "9784c05a-00b6-4527-9b39-0b5e4e506176",
                "property_name": "accessories",
                "property_option_id": "9784c05a-00b6-4527-9b39-0b5e4e506176#4",
            },
        ],
    }


@pytest.fixture
def sample_info_result_w_properties():
    return {
        "meta": {
            "edit_info": {
                "objects": [
                    {
                        "color": "#FF625A",
                        "id": "745e4138-2cdb-46f2-a299-36ad799be2f0",
                        "selected": False,
                        "tracking_id": 1,
                        "visible": True,
                    },
                    {
                        "color": "#FE9573",
                        "id": "18bd41c0-f9c6-4c5a-b430-10ce55615044",
                        "selected": False,
                        "tracking_id": 2,
                        "visible": True,
                    },
                ]
            },
            "image_info": {},
        },
        "result": {
            "categories": {"frames": [], "properties": []},
            "objects": [
                {
                    "annotation_type": "box",
                    "class_id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "class_name": "Person",
                    "frames": [
                        {
                            "annotation": {
                                "coord": {
                                    "height": 482.386980108499,
                                    "width": 232.40506329113896,
                                    "x": 1245.1356238698008,
                                    "y": 355.4430379746835,
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 0,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "height": 410.1265822784811,
                                    "width": 199.20433996383372,
                                    "x": 1032.2603978300176,
                                    "y": 421.8444846292944,
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 1,
                            "properties": [],
                        },
                    ],
                    "id": "745e4138-2cdb-46f2-a299-36ad799be2f0",
                    "properties": [
                        {
                            "option_id": "2",
                            "option_name": "True",
                            "property_id": "63fe0ee1-2a21-40b8-a0cd-4ac06e9093a4",
                            "property_name": "identifiable",
                            "type": "radio",
                        },
                        {
                            "option_ids": ["3", "4"],
                            "option_names": ["hat", "bag"],
                            "property_id": "9784c05a-00b6-4527-9b39-0b5e4e506176",
                            "property_name": "accessories",
                            "type": "checkbox",
                        },
                    ],
                    "tracking_id": 1,
                },
                {
                    "annotation_type": "polygon",
                    "class_id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "class_name": "Chair",
                    "frames": [
                        {
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "x": 723.6889692585893,
                                            "y": 207.0162748643761,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 312.47739602169975,
                                        },
                                        {
                                            "x": 706.1121157323688,
                                            "y": 310.52441229656415,
                                        },
                                        {
                                            "x": 739.3128390596743,
                                            "y": 341.7721518987341,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 363.254972875226,
                                        },
                                        {
                                            "x": 883.8336347197104,
                                            "y": 357.3960216998191,
                                        },
                                        {
                                            "x": 876.021699819168,
                                            "y": 322.2423146473779,
                                        },
                                        {
                                            "x": 911.1754068716092,
                                            "y": 273.41772151898726,
                                        },
                                        {
                                            "x": 838.9150090415911,
                                            "y": 298.8065099457504,
                                        },
                                        {
                                            "x": 807.6672694394211,
                                            "y": 191.3924050632911,
                                        },
                                    ]
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 0,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "x": 723.6889692585893,
                                            "y": 207.0162748643761,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 312.47739602169975,
                                        },
                                        {
                                            "x": 706.1121157323688,
                                            "y": 310.52441229656415,
                                        },
                                        {
                                            "x": 739.3128390596743,
                                            "y": 341.7721518987341,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 363.254972875226,
                                        },
                                        {
                                            "x": 883.8336347197104,
                                            "y": 357.3960216998191,
                                        },
                                        {
                                            "x": 876.021699819168,
                                            "y": 322.2423146473779,
                                        },
                                        {
                                            "x": 911.1754068716092,
                                            "y": 273.41772151898726,
                                        },
                                        {
                                            "x": 838.9150090415911,
                                            "y": 298.8065099457504,
                                        },
                                        {
                                            "x": 807.6672694394211,
                                            "y": 191.3924050632911,
                                        },
                                    ]
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 1,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "x": 723.6889692585893,
                                            "y": 207.0162748643761,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 312.47739602169975,
                                        },
                                        {
                                            "x": 706.1121157323688,
                                            "y": 310.52441229656415,
                                        },
                                        {
                                            "x": 739.3128390596743,
                                            "y": 341.7721518987341,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 363.254972875226,
                                        },
                                        {
                                            "x": 883.8336347197104,
                                            "y": 357.3960216998191,
                                        },
                                        {
                                            "x": 876.021699819168,
                                            "y": 322.2423146473779,
                                        },
                                        {
                                            "x": 911.1754068716092,
                                            "y": 273.41772151898726,
                                        },
                                        {
                                            "x": 838.9150090415911,
                                            "y": 298.8065099457504,
                                        },
                                        {
                                            "x": 807.6672694394211,
                                            "y": 191.3924050632911,
                                        },
                                    ]
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 7,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "x": 723.6889692585893,
                                            "y": 207.0162748643761,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 312.47739602169975,
                                        },
                                        {
                                            "x": 706.1121157323688,
                                            "y": 310.52441229656415,
                                        },
                                        {
                                            "x": 739.3128390596743,
                                            "y": 341.7721518987341,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 363.254972875226,
                                        },
                                        {
                                            "x": 883.8336347197104,
                                            "y": 357.3960216998191,
                                        },
                                        {
                                            "x": 876.021699819168,
                                            "y": 322.2423146473779,
                                        },
                                        {
                                            "x": 911.1754068716092,
                                            "y": 273.41772151898726,
                                        },
                                        {
                                            "x": 838.9150090415911,
                                            "y": 298.8065099457504,
                                        },
                                        {
                                            "x": 807.6672694394211,
                                            "y": 191.3924050632911,
                                        },
                                    ]
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 9,
                            "properties": [],
                        },
                        {
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "x": 723.6889692585893,
                                            "y": 207.0162748643761,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 312.47739602169975,
                                        },
                                        {
                                            "x": 706.1121157323688,
                                            "y": 310.52441229656415,
                                        },
                                        {
                                            "x": 739.3128390596743,
                                            "y": 341.7721518987341,
                                        },
                                        {
                                            "x": 737.3598553345388,
                                            "y": 363.254972875226,
                                        },
                                        {
                                            "x": 883.8336347197104,
                                            "y": 357.3960216998191,
                                        },
                                        {
                                            "x": 876.021699819168,
                                            "y": 322.2423146473779,
                                        },
                                        {
                                            "x": 911.1754068716092,
                                            "y": 273.41772151898726,
                                        },
                                        {
                                            "x": 838.9150090415911,
                                            "y": 298.8065099457504,
                                        },
                                        {
                                            "x": 807.6672694394211,
                                            "y": 191.3924050632911,
                                        },
                                    ]
                                },
                                "meta": {},
                                "multiple": False,
                            },
                            "num": 10,
                            "properties": [],
                        },
                    ],
                    "id": "18bd41c0-f9c6-4c5a-b430-10ce55615044",
                    "properties": [
                        {
                            "property_id": "f10903ce-2112-423f-adaf-c5042dc0f17e",
                            "property_name": "color",
                            "type": "free response",
                            "value": "beige",
                        }
                    ],
                    "tracking_id": 2,
                },
            ],
        },
        "tags": {
            "annotated_frame_count": 5,
            "categories_id": [],
            "class": ["Person", "Chair"],
            "classes_annotation_count": [
                {
                    "count": 2,
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                },
                {
                    "count": 5,
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
                },
            ],
            "classes_count": [
                {
                    "count": 1,
                    "id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "name": "Person",
                },
                {
                    "count": 1,
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
                },
            ],
            "classes_id": [
                "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                "1c4c4891-9382-496d-8895-a004d488b38e",
            ],
            "classes_properties_count": [
                {
                    "class_id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "count": 1,
                    "option_id": "2",
                    "option_name": "True",
                    "property_id": "63fe0ee1-2a21-40b8-a0cd-4ac06e9093a4",
                    "property_name": "identifiable",
                    "property_option_id": "63fe0ee1-2a21-40b8-a0cd-4ac06e9093a4#2",
                },
                {
                    "class_id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "count": 1,
                    "option_id": "3",
                    "option_name": "hat",
                    "property_id": "9784c05a-00b6-4527-9b39-0b5e4e506176",
                    "property_name": "accessories",
                    "property_option_id": "9784c05a-00b6-4527-9b39-0b5e4e506176#3",
                },
                {
                    "class_id": "f9c75f80-1f2d-45ef-875e-bbe5f49e56ff",
                    "count": 1,
                    "option_id": "4",
                    "option_name": "bag",
                    "property_id": "9784c05a-00b6-4527-9b39-0b5e4e506176",
                    "property_name": "accessories",
                    "property_option_id": "9784c05a-00b6-4527-9b39-0b5e4e506176#4",
                },
            ],
        },
        "version": "0.4.7",
    }


@pytest.fixture
def label_interface_sample_v6():
    return {
        "type": "video-siesta",
        "version": "0.6.5",
        "data_type": "image sequence",
        "categorization": {
            "properties": [
                {
                    "id": "bb0e4235-9d17-40ed-9852-26fc66941d05",
                    "name": "ms_cate",
                    "default_value": [],
                    "description": "",
                    "options": [
                        {
                            "name": "ms_g",
                            "id": "13cb5be0-33cc-4dda-84c3-ec6afb50680c",
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
                    "render_value": False,
                    "required": False,
                    "per_frame": False,
                    "type": "checkbox",
                },
                {
                    "id": "0da7b178-df30-47da-bf9b-2daadfbc99d7",
                    "name": "mc_cate",
                    "default_value": "",
                    "description": "",
                    "options": [
                        {
                            "name": "mc_g",
                            "id": "0bd3a095-2e61-4cf3-b7aa-cb58d4ef1912",
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
                    "render_value": False,
                    "required": False,
                    "per_frame": False,
                    "type": "radio",
                },
                {
                    "id": "69f0963a-0400-4d9a-81fe-b7ef3ded55db",
                    "name": "fr_cate",
                    "default_value": "",
                    "description": "",
                    "constraints": {
                        "digit": True,
                        "space": True,
                        "special": True,
                        "alphabet": True,
                    },
                    "render_value": False,
                    "blank": True,
                    "per_frame": False,
                    "type": "free response",
                },
            ]
        },
        "object_tracking": {
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
                    "name": "person",
                    "color": "#FF625A",
                    "properties": [
                        {
                            "id": "c126812b-c013-4f78-b709-7a1764c7c7f3",
                            "name": "box Property",
                            "default_value": None,
                            "description": "",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "radio",
                        },
                        {
                            "id": "3b09f755-e34f-4d5b-9950-0467d08b5c6b",
                            "name": "box Property (1)",
                            "default_value": [],
                            "description": "",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "checkbox",
                        },
                        {
                            "id": "da2e15ff-98bc-4ef4-a1c9-1830f0e32908",
                            "name": "box Property (2)",
                            "default_value": "",
                            "description": "",
                            "constraints": {
                                "alphabet": True,
                                "digit": True,
                                "space": True,
                                "special": True,
                            },
                            "render_value": False,
                            "blank": False,
                            "per_frame": False,
                            "type": "free response",
                        },
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "box",
                },
                {
                    "id": "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                    "name": "person",
                    "color": "#FE9573",
                    "properties": [
                        {
                            "id": "e8405ff2-a091-4fb3-9ee3-33921491be6b",
                            "name": "rbox Property",
                            "default_value": None,
                            "description": "",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "radio",
                        },
                        {
                            "id": "3e75a099-875a-4576-9548-2e2f171e6ad5",
                            "name": "rbox Property (1)",
                            "default_value": [],
                            "description": "",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "checkbox",
                        },
                        {
                            "id": "29243fd2-92c4-4f11-baa0-0e615901039f",
                            "name": "rbox Property (2)",
                            "default_value": "",
                            "description": "",
                            "constraints": {
                                "alphabet": True,
                                "digit": True,
                                "space": True,
                                "special": True,
                            },
                            "render_value": False,
                            "blank": False,
                            "per_frame": False,
                            "type": "free response",
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
                            "default_value": None,
                            "description": "",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "radio",
                        },
                        {
                            "id": "7ac2d2d6-bbcf-422e-8b88-0b20335626a0",
                            "name": "poly Property (1)",
                            "default_value": [],
                            "description": "",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "checkbox",
                        },
                        {
                            "id": "a2bae19d-b700-4633-81b3-880b6fcc9fc0",
                            "name": "poly Property (2)",
                            "default_value": "",
                            "description": "",
                            "constraints": {
                                "alphabet": True,
                                "digit": True,
                                "space": True,
                                "special": True,
                            },
                            "render_value": False,
                            "blank": False,
                            "per_frame": False,
                            "type": "free response",
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
                            "default_value": None,
                            "description": "",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "radio",
                        },
                        {
                            "id": "1007f627-a13f-4678-a411-871482dfd166",
                            "name": "poly_seg Property (1)",
                            "default_value": [],
                            "description": "",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "checkbox",
                        },
                        {
                            "id": "2fccbadc-271f-4124-a3e2-71a759db27c0",
                            "name": "poly_seg Property (2)",
                            "default_value": "",
                            "description": "",
                            "constraints": {
                                "alphabet": True,
                                "digit": True,
                                "space": True,
                                "special": True,
                            },
                            "render_value": False,
                            "blank": False,
                            "per_frame": False,
                            "type": "free response",
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
                            "default_value": None,
                            "description": "",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "radio",
                        },
                        {
                            "id": "743e543b-c51c-4eac-a29b-f8fa20dd2474",
                            "name": "face_kp Property (1)",
                            "default_value": [],
                            "description": "",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "checkbox",
                        },
                        {
                            "id": "931e64e5-30b2-4da0-a435-b32f40cad7cb",
                            "name": "face_kp Property (2)",
                            "default_value": "",
                            "description": "",
                            "constraints": {
                                "alphabet": True,
                                "digit": True,
                                "space": True,
                                "special": True,
                            },
                            "render_value": False,
                            "blank": False,
                            "per_frame": False,
                            "type": "free response",
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
                            "default_value": None,
                            "description": "",
                            "options": [
                                {"id": "1", "name": "Untitled Option"},
                                {"id": "2", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "radio",
                        },
                        {
                            "id": "faf00cd0-99d6-409e-a9ad-75c8830c021a",
                            "name": "2d_cuboid Property (1)",
                            "default_value": [],
                            "description": "",
                            "options": [
                                {"id": "3", "name": "Untitled Option"},
                                {"id": "4", "name": "Untitled Option (1)"},
                            ],
                            "render_value": False,
                            "required": True,
                            "per_frame": False,
                            "type": "checkbox",
                        },
                        {
                            "id": "b75b8e1f-0e18-405f-bcde-f808fc3595dc",
                            "name": "2d_cuboid Property (2)",
                            "default_value": "",
                            "description": "",
                            "constraints": {
                                "alphabet": True,
                                "digit": True,
                                "space": True,
                                "special": True,
                            },
                            "render_value": False,
                            "blank": False,
                            "per_frame": False,
                            "type": "free response",
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
        "version": "0.6.5",
        "meta": {
            "image_info": {},
            "edit_info": {
                "objects": [
                    {
                        "id": "12590dbe-72f1-4278-b1fe-b4a0642d55b6",
                        "color": "#FF625A",
                        "visible": True,
                        "selected": False,
                        "tracking_id": None,
                    },
                    {
                        "id": "6f4e5ef6-e3ea-4a2d-b0a1-3ebd00b965b3",
                        "color": "#FE9573",
                        "visible": True,
                        "selected": False,
                        "tracking_id": None,
                    },
                    {
                        "id": "9b20fabd-9b33-422b-bbb5-870cfaad31b2",
                        "color": "#FFAF5A",
                        "visible": True,
                        "selected": False,
                        "tracking_id": None,
                    },
                    {
                        "id": "92e28cc4-7eee-4a72-9dc4-383ffd4ecf70",
                        "color": "#FFCC00",
                        "visible": True,
                        "selected": False,
                        "tracking_id": None,
                    },
                    {
                        "id": "9ed93108-2c3a-4eba-8613-0633003a239f",
                        "color": "#FFF73E",
                        "visible": True,
                        "selected": False,
                        "tracking_id": None,
                    },
                    {
                        "id": "10a57f9d-3d04-4ce6-aa8f-516300cd8f75",
                        "color": "#DEF00F",
                        "visible": True,
                        "selected": False,
                        "tracking_id": None,
                    },
                ]
            },
        },
        "result": {
            "objects": [
                {
                    "id": "12590dbe-72f1-4278-b1fe-b4a0642d55b6",
                    "class_name": "person",
                    "class_id": "346c2e59-0d4d-4818-8cd0-538b157fa06c",
                    "annotation_type": "box",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
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
                        }
                    ],
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "6f4e5ef6-e3ea-4a2d-b0a1-3ebd00b965b3",
                    "class_name": "person",
                    "class_id": "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                    "annotation_type": "rbox",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
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
                        }
                    ],
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "9b20fabd-9b33-422b-bbb5-870cfaad31b2",
                    "class_name": "poly",
                    "class_id": "7c6ab4db-5b0c-4143-b992-6dc732f28870",
                    "annotation_type": "polyline",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
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
                        }
                    ],
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "92e28cc4-7eee-4a72-9dc4-383ffd4ecf70",
                    "class_name": "poly_seg",
                    "class_id": "5a122ca5-b827-4896-9476-ab01d5164853",
                    "annotation_type": "polygon",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
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
                        }
                    ],
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "9ed93108-2c3a-4eba-8613-0633003a239f",
                    "class_name": "face_kp",
                    "class_id": "96007e8f-3c76-4359-88d3-27cc3b2e986f",
                    "annotation_type": "keypoint",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
                            "annotation": {
                                "coord": {
                                    "points": [
                                        {
                                            "name": "left eye center",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "left eye inner corner",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "left eye outer corner",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "right eye center",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "right eye inner corner",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "right eye outer corner",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "left eyebrow inner end",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "left eyebrow outer end",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "right eyebrow inner end",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "right eyebrow outer end",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "nose tip",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "mouth left corner",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "mouth right corner",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "mouth center top lip",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
                                        },
                                        {
                                            "name": "mouth center bottom lip",
                                            "x": 0.0,
                                            "y": 0.0,
                                            "state": {
                                                "visible": True,
                                                "valid": True,
                                            },
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
                        }
                    ],
                    "properties": [],
                    "tracking_id": None,
                },
                {
                    "id": "10a57f9d-3d04-4ce6-aa8f-516300cd8f75",
                    "class_name": "2d_cuboid",
                    "class_id": "e970ec55-2dd7-4a94-8a93-ec2b34ed5005",
                    "annotation_type": "cuboid2d",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
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
                        }
                    ],
                    "properties": [],
                    "tracking_id": None,
                },
            ],
            "categories": {"frames": [], "properties": []},
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
                "person",
                "person",
                "poly",
                "poly_seg",
                "face_kp",
                "2d_cuboid",
            ],
            "classes_count": [
                {
                    "id": "346c2e59-0d4d-4818-8cd0-538b157fa06c",
                    "name": "person",
                    "count": 1,
                },
                {
                    "id": "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                    "name": "person",
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
            "classes_annotation_count": [
                {
                    "id": "346c2e59-0d4d-4818-8cd0-538b157fa06c",
                    "name": "person",
                    "count": 1,
                },
                {
                    "id": "e15fae76-1702-44e9-97d8-25bf420e4dbe",
                    "name": "person",
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
            "categories_id": [],
            "annotated_frame_count": 1,
        },
    }
