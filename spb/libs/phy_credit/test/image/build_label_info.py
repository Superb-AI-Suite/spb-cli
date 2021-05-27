from phy_credit.imageV2 import build_label_info
import json


def test_build_label_info_from_scratch():
    label_interface_sample = {
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
                                    "name": "a"
                                },
                                {
                                    "id": "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                                    "name": "b"
                                },
                                {
                                    "id": "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a",
                                    "name": "c"
                                }
                            ]
                        },
                        {
                            "id": "4964136d-8ebf-4692-98ee-8f81b0fb1234",
                            "name": "number",
                            "children": [
                                {
                                    "id": "a1200bca-41c2-43e5-85d9-4d51554d552b",
                                    "name": "1"
                                },
                                {
                                    "id": "d6711d55-aae5-4dbe-a92e-55d87c1c02ef",
                                    "name": "2"
                                },
                                {
                                    "id": "87c0bf6a-6dfb-46d8-99b4-5112340529c9",
                                    "name": "3"
                                }
                            ]
                        }
                    ],
                    "required": True,
                    "description": "",
                    "render_value": False,
                    "default_value": []
                }
            ]
        },
        "object_detection": {
            "keypoints": [
                {
                    "id": "keypoint-id",
                    "name": "human",
                    "edges": [
                        {
                            "u": 2,
                            "v": 4,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 0,
                            "v": 2,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 8,
                            "v": 6,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 10,
                            "v": 8,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 12,
                            "v": 6,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 14,
                            "v": 12,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 16,
                            "v": 14,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 1,
                            "v": 2,
                            "color": "#4db6ac"
                        },
                        {
                            "u": 5,
                            "v": 6,
                            "color": "#4db6ac"
                        },
                        {
                            "u": 11,
                            "v": 12,
                            "color": "#4db6ac"
                        },
                        {
                            "u": 1,
                            "v": 0,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 3,
                            "v": 1,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 7,
                            "v": 5,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 9,
                            "v": 7,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 11,
                            "v": 5,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 13,
                            "v": 11,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 15,
                            "v": 13,
                            "color": "#64b5f6"
                        }
                    ],
                    "points": [
                        {
                            "name": "nose",
                            "color": "#d50000",
                            "default_value": {
                                "x": 0.5,
                                "y": 0.1,
                                "state": {
                                    "visible": True
                                }
                            }
                        },
                        {
                            "name": "left eye",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.55,
                                "y": 0.05,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 2
                        },
                        {
                            "name": "right eye",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.45,
                                "y": 0.05,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 1
                        },
                        {
                            "name": "left ear",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.075,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 4
                        },
                        {
                            "name": "right ear",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.075,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 3
                        },
                        {
                            "name": "left shoulder",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.65,
                                "y": 0.2,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 6
                        },
                        {
                            "name": "right shoulder",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.35,
                                "y": 0.2,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 5
                        },
                        {
                            "name": "left elbow",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.85,
                                "y": 0.3,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 8
                        },
                        {
                            "name": "right elbow",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.15,
                                "y": 0.3,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 7
                        },
                        {
                            "name": "left wrist",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.75,
                                "y": 0.45,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 10
                        },
                        {
                            "name": "right wrist",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.25,
                                "y": 0.45,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 9
                        },
                        {
                            "name": "left hip",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.62,
                                "y": 0.5,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 12
                        },
                        {
                            "name": "right hip",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.38,
                                "y": 0.5,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 11
                        },
                        {
                            "name": "left knee",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.7,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 14
                        },
                        {
                            "name": "right_knee",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.7,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 13
                        },
                        {
                            "name": "left ankle",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.9,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 16
                        },
                        {
                            "name": "right ankle",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.9,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 15
                        }
                    ],
                    "allow_valid_invisibles": False
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
                                {
                                    "id": "1",
                                    "name": "1"
                                },
                                {
                                    "id": "2",
                                    "name": "2"
                                }
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None
                        },
                        {
                            "id": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "name": "ps",
                            "type": "checkbox",
                            "options": [
                                {
                                    "id": "3",
                                    "name": "1"
                                },
                                {
                                    "id": "4",
                                    "name": "2"
                                }
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": []
                        }
                    ],
                    "constraints": {},
                    "ai_class_map": [
                        {
                            "class_ids": [],
                            "engine_id": ""
                        }
                    ],
                    "annotation_type": "box"
                },
                {
                    "id": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                    "name": "pp",
                    "color": "#FE9573",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [
                        {
                            "class_ids": [],
                            "engine_id": ""
                        }
                    ],
                    "annotation_type": "polygon"
                },
                {
                    "id": "df8aa5dc-ae20-417d-a522-555b981dcc77",
                    "name": "kk",
                    "color": "#FFAF5A",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "keypoint",
                    "keypoint_interface_id": "keypoint-id"
                }
            ],
            "annotation_types": [
                "box",
                "polygon",
                "keypoint",
                "image category"
            ]
        }
    }
    labelInfo = build_label_info(label_interface_sample)
    labelInfo.add_object(class_name='bb', annotation={
            "coord": {
                "x": 173,
                "y": 92,
                "width": 188,
                "height": 161
            }
        },
        properties= [
            {
                "name": "pc",
                "value": "2"
            },
            {
                "name": "ps",
                "value": [
                    "1"
                ]
            }
        ]
    )
    labelInfo.add_object(class_name='bb', annotation={
            "coord": {
                "x": 99,
                "y": 74,
                "width": 78,
                "height": 77
            }
        },
        properties=[
            {
                "name": "pc",
                "value": "1"
            },
            {
                "name": "ps",
                "value": [
                    "2",
                    "1"
                ]
            }
        ]
    )
    labelInfo.add_object(class_name='pp', annotation={
            "coord": {
                "points": [
                    {
                        "x": 441,
                        "y": 158
                    },
                    {
                        "x": 483,
                        "y": 301
                    },
                    {
                        "x": 547,
                        "y": 293
                    },
                    {
                        "x": 557,
                        "y": 174
                    }
                ]
            }
        }
    )
    labelInfo.add_object(class_name='kk', annotation={
            "coord": {
                "graph": {
                    "nodes": [
                        {
                            "x": 102.5,
                            "y": 178.4
                        },
                        {
                            "x": 108.75,
                            "y": 166.7
                        },
                        {
                            "x": 96.25,
                            "y": 166.7
                        },
                        {
                            "x": 115,
                            "y": 172.55
                        },
                        {
                            "x": 90,
                            "y": 172.55
                        },
                        {
                            "x": 121.25,
                            "y": 201.8
                        },
                        {
                            "x": 83.75,
                            "y": 201.8
                        },
                        {
                            "x": 146.25,
                            "y": 225.2
                        },
                        {
                            "x": 58.75,
                            "y": 225.2
                        },
                        {
                            "x": 133.75,
                            "y": 260.3
                        },
                        {
                            "x": 71.25,
                            "y": 260.3
                        },
                        {
                            "x": 117.5,
                            "y": 272
                        },
                        {
                            "x": 87.5,
                            "y": 272
                        },
                        {
                            "x": 115,
                            "y": 318.79999999999995
                        },
                        {
                            "x": 90,
                            "y": 318.79999999999995
                        },
                        {
                            "x": 115,
                            "y": 365.6
                        },
                        {
                            "x": 90,
                            "y": 365.6
                        }
                    ],
                    "states": [
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        },
                        {
                            "state": {
                                "visible": True
                            }
                        }
                    ]
                }
            }
        }
    )

    print(json.dumps(labelInfo.build_tags()))
    print(json.dumps(labelInfo.build_info()))


def test_build_label_info_from_result():
    label_interface_sample = {
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
                                    "name": "a"
                                },
                                {
                                    "id": "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                                    "name": "b"
                                },
                                {
                                    "id": "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a",
                                    "name": "c"
                                }
                            ]
                        },
                        {
                            "id": "4964136d-8ebf-4692-98ee-8f81b0fb1234",
                            "name": "number",
                            "children": [
                                {
                                    "id": "a1200bca-41c2-43e5-85d9-4d51554d552b",
                                    "name": "1"
                                },
                                {
                                    "id": "d6711d55-aae5-4dbe-a92e-55d87c1c02ef",
                                    "name": "2"
                                },
                                {
                                    "id": "87c0bf6a-6dfb-46d8-99b4-5112340529c9",
                                    "name": "3"
                                }
                            ]
                        }
                    ],
                    "required": True,
                    "description": "",
                    "render_value": False,
                    "default_value": []
                }
            ]
        },
        "object_detection": {
            "keypoints": [
                {
                    "id": "keypoint-id",
                    "name": "human",
                    "edges": [
                        {
                            "u": 2,
                            "v": 4,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 0,
                            "v": 2,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 8,
                            "v": 6,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 10,
                            "v": 8,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 12,
                            "v": 6,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 14,
                            "v": 12,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 16,
                            "v": 14,
                            "color": "#ff8a65"
                        },
                        {
                            "u": 1,
                            "v": 2,
                            "color": "#4db6ac"
                        },
                        {
                            "u": 5,
                            "v": 6,
                            "color": "#4db6ac"
                        },
                        {
                            "u": 11,
                            "v": 12,
                            "color": "#4db6ac"
                        },
                        {
                            "u": 1,
                            "v": 0,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 3,
                            "v": 1,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 7,
                            "v": 5,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 9,
                            "v": 7,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 11,
                            "v": 5,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 13,
                            "v": 11,
                            "color": "#64b5f6"
                        },
                        {
                            "u": 15,
                            "v": 13,
                            "color": "#64b5f6"
                        }
                    ],
                    "points": [
                        {
                            "name": "nose",
                            "color": "#d50000",
                            "default_value": {
                                "x": 0.5,
                                "y": 0.1,
                                "state": {
                                    "visible": True
                                }
                            }
                        },
                        {
                            "name": "left eye",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.55,
                                "y": 0.05,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 2
                        },
                        {
                            "name": "right eye",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.45,
                                "y": 0.05,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 1
                        },
                        {
                            "name": "left ear",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.075,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 4
                        },
                        {
                            "name": "right ear",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.075,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 3
                        },
                        {
                            "name": "left shoulder",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.65,
                                "y": 0.2,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 6
                        },
                        {
                            "name": "right shoulder",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.35,
                                "y": 0.2,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 5
                        },
                        {
                            "name": "left elbow",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.85,
                                "y": 0.3,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 8
                        },
                        {
                            "name": "right elbow",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.15,
                                "y": 0.3,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 7
                        },
                        {
                            "name": "left wrist",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.75,
                                "y": 0.45,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 10
                        },
                        {
                            "name": "right wrist",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.25,
                                "y": 0.45,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 9
                        },
                        {
                            "name": "left hip",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.62,
                                "y": 0.5,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 12
                        },
                        {
                            "name": "right hip",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.38,
                                "y": 0.5,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 11
                        },
                        {
                            "name": "left knee",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.7,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 14
                        },
                        {
                            "name": "right_knee",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.7,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 13
                        },
                        {
                            "name": "left ankle",
                            "color": "#64b5f6",
                            "default_value": {
                                "x": 0.6,
                                "y": 0.9,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 16
                        },
                        {
                            "name": "right ankle",
                            "color": "#ff8a65",
                            "default_value": {
                                "x": 0.4,
                                "y": 0.9,
                                "state": {
                                    "visible": True
                                }
                            },
                            "symmetric_idx": 15
                        }
                    ],
                    "allow_valid_invisibles": False
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
                                {
                                    "id": "1",
                                    "name": "1"
                                },
                                {
                                    "id": "2",
                                    "name": "2"
                                }
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None
                        },
                        {
                            "id": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "name": "ps",
                            "type": "checkbox",
                            "options": [
                                {
                                    "id": "3",
                                    "name": "1"
                                },
                                {
                                    "id": "4",
                                    "name": "2"
                                }
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": []
                        }
                    ],
                    "constraints": {},
                    "ai_class_map": [
                        {
                            "class_ids": [],
                            "engine_id": ""
                        }
                    ],
                    "annotation_type": "box"
                },
                {
                    "id": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                    "name": "pp",
                    "color": "#FE9573",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [
                        {
                            "class_ids": [],
                            "engine_id": ""
                        }
                    ],
                    "annotation_type": "polygon"
                },
                {
                    "id": "df8aa5dc-ae20-417d-a522-555b981dcc77",
                    "name": "kk",
                    "color": "#FFAF5A",
                    "properties": [],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "keypoint",
                    "keypoint_interface_id": "keypoint-id"
                }
            ],
            "annotation_types": [
                "box",
                "polygon",
                "keypoint",
                "image category"
            ]
        }
    }
    labelInfo = build_label_info(label_interface_sample, result={
        "objects": [
            {
                "id": "e0d133c5-7089-465a-8f05-ec5fecccd8ba",
                "classId": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "className": "bb",
                "annotationType": "box",
                "annotation": {
                    "coord": {
                        "x": 173,
                        "y": 92,
                        "width": 188,
                        "height": 161
                    },
                    "meta": {
                        "zIndex": 1
                    }
                },
                "properties": [
                    {
                        "propertyId": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                        "propertyName": "pc",
                        "optionId": "2",
                        "optionName": "2"
                    },
                    {
                        "propertyId": "f7eebc07-155b-48f3-847d-5501668044ad",
                        "propertyName": "ps",
                        "optionIds": [
                            "3"
                        ],
                        "optionNames": [
                            "1"
                        ]
                    }
                ]
            },
            {
                "id": "47353aca-6f12-4de8-b54b-5985c3fe7faa",
                "classId": "6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
                "className": "bb",
                "annotationType": "box",
                "annotation": {
                    "coord": {
                        "x": 99,
                        "y": 74,
                        "width": 78,
                        "height": 77
                    },
                    "meta": {
                        "zIndex": 1
                    }
                },
                "properties": [
                    {
                        "propertyId": "5b65d4ae-2737-4de8-a460-70a5aab4eba2",
                        "propertyName": "pc",
                        "optionId": "1",
                        "optionName": "1"
                    },
                    {
                        "propertyId": "f7eebc07-155b-48f3-847d-5501668044ad",
                        "propertyName": "ps",
                        "optionIds": [
                            "4",
                            "3"
                        ],
                        "optionNames": [
                            "2",
                            "1"
                        ]
                    }
                ]
            },
            {
                "id": "ddd914fe-0b9b-4ee7-8397-555412ac9687",
                "classId": "3f6439b3-7d58-42c9-9093-bb5e3d2fa6a4",
                "className": "pp",
                "annotationType": "polygon",
                "annotation": {
                    "coord": {
                        "points": [
                            {
                                "x": 441,
                                "y": 158
                            },
                            {
                                "x": 483,
                                "y": 301
                            },
                            {
                                "x": 547,
                                "y": 293
                            },
                            {
                                "x": 557,
                                "y": 174
                            }
                        ]
                    },
                    "meta": {
                        "zIndex": 1
                    }
                },
                "properties": []
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
                                {
                                    "x": 102.5,
                                    "y": 178.4
                                },
                                {
                                    "x": 108.75,
                                    "y": 166.7
                                },
                                {
                                    "x": 96.25,
                                    "y": 166.7
                                },
                                {
                                    "x": 115,
                                    "y": 172.55
                                },
                                {
                                    "x": 90,
                                    "y": 172.55
                                },
                                {
                                    "x": 121.25,
                                    "y": 201.8
                                },
                                {
                                    "x": 83.75,
                                    "y": 201.8
                                },
                                {
                                    "x": 146.25,
                                    "y": 225.2
                                },
                                {
                                    "x": 58.75,
                                    "y": 225.2
                                },
                                {
                                    "x": 133.75,
                                    "y": 260.3
                                },
                                {
                                    "x": 71.25,
                                    "y": 260.3
                                },
                                {
                                    "x": 117.5,
                                    "y": 272
                                },
                                {
                                    "x": 87.5,
                                    "y": 272
                                },
                                {
                                    "x": 115,
                                    "y": 318.79999999999995
                                },
                                {
                                    "x": 90,
                                    "y": 318.79999999999995
                                },
                                {
                                    "x": 115,
                                    "y": 365.6
                                },
                                {
                                    "x": 90,
                                    "y": 365.6
                                }
                            ],
                            "states": [
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                },
                                {
                                    "state": {
                                        "visible": True
                                    }
                                }
                            ]
                        }
                    },
                    "meta": {
                        "zIndex": 1
                    }
                },
                "properties": []
            }
        ],
        "categories": {
            "properties": [
                {
                    "propertyId": "root",
                    "propertyName": "Root",
                    "optionIds": [
                        "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                        "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a"
                    ],
                    "optionNames": [
                        "b",
                        "c"
                    ]
                }
            ]
        }
    })

    print(json.dumps(labelInfo.build_tags()))
    print(json.dumps(labelInfo.build_info()))


def test_build_label_info_from_scratch_v4():
    label_interface_sample = {
        "type": "image-siesta",
        "version": "0.4.0",
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
                                    "name": "a"
                                },
                                {
                                    "id": "cd0df355-75f3-48c0-977a-8f2b7cd8197b",
                                    "name": "b"
                                },
                                {
                                    "id": "de5f7920-e9bc-441f-b4c0-3ebd8fe7013a",
                                    "name": "c"
                                }
                            ]
                        },
                        {
                            "id": "4964136d-8ebf-4692-98ee-8f81b0fb1234",
                            "name": "number",
                            "children": [
                                {
                                    "id": "a1200bca-41c2-43e5-85d9-4d51554d552b",
                                    "name": "1"
                                },
                                {
                                    "id": "d6711d55-aae5-4dbe-a92e-55d87c1c02ef",
                                    "name": "2"
                                },
                                {
                                    "id": "87c0bf6a-6dfb-46d8-99b4-5112340529c9",
                                    "name": "3"
                                }
                            ]
                        }
                    ],
                    "required": True,
                    "description": "",
                    "render_value": False,
                    "default_value": []
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
                                {
                                    "id": "1",
                                    "name": "1"
                                },
                                {
                                    "id": "2",
                                    "name": "2"
                                }
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None
                        },
                        {
                            "id": "f7eebc07-155b-48f3-847d-5501668044ad",
                            "name": "ps",
                            "type": "checkbox",
                            "options": [
                                {
                                    "id": "3",
                                    "name": "1"
                                },
                                {
                                    "id": "4",
                                    "name": "2"
                                }
                            ],
                            "required": True,
                            "description": "",
                            "render_value": False,
                            "default_value": []
                        }
                    ],
                    "constraints": {},
                    "ai_class_map": [
                        {
                            "class_ids": [],
                            "engine_id": ""
                        }
                    ],
                    "annotation_type": "box"
                }
            ],
            "annotation_types": [
                "box",
                "image category"
            ]
        }
    }
    labelInfo = build_label_info(label_interface_sample)
    labelInfo.add_object(class_name='bb', annotation={
            "coord": {
                "x": 173,
                "y": 92,
                "width": 188,
                "height": 161
            }
        },
        properties= [
            {
                "name": "pc",
                "value": "2"
            },
            {
                "name": "ps",
                "value": [
                    "1"
                ]
            }
        ]
    )
    labelInfo.add_object(class_name='bb', annotation={
            "coord": {
                "x": 99,
                "y": 74,
                "width": 78,
                "height": 77
            }
        },
        properties=[
            {
                "name": "pc",
                "value": "1"
            },
            {
                "name": "ps",
                "value": [
                    "2",
                    "1"
                ]
            }
        ]
    )
    labelInfo.set_categories(
        properties=[
            {
                'name': 'Root',
                'value': ['1', 'a', 'b']
            }
        ]
    )

    print(json.dumps(labelInfo.build_tags()))
    print(json.dumps(labelInfo.build_info()))


if __name__ == '__main__':
    # in a rush...
    test_build_label_info_from_scratch()
    test_build_label_info_from_result()
    test_build_label_info_from_scratch_v4()
