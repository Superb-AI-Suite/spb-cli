import pytest


@pytest.fixture
def label_interface_sample_v6():
    return {
        "type": "pointclouds-siesta",
        "version": "0.6.5",
        "data_type": "pointclouds",
        "categorization": {
            "properties": []
        },
        "object_tracking": {
            "object_groups": [
                {
                    "id": "92851114-f8ab-46f0-b472-9b81032afb02",
                    "name": "Organism",
                    "object_class_ids": [
                        "68499718-1fcc-4435-b97d-92bdbac702fb",
                        "c8174711-3d1a-476f-9d94-94f9c08b426c"
                    ]
                },
                {
                    "id": "4ab741f2-1522-417e-8989-ae7629a25606",
                    "name": "Vehicles",
                    "object_class_ids": [
                        "2adca68d-9251-4932-85f6-17f1a2312c77"
                    ]
                }
            ],
            "object_classes": [
                {
                    "id": "2adca68d-9251-4932-85f6-17f1a2312c77",
                    "name": "Car",
                    "color": "#FF625A",
                    "properties": [
                        {
                            "id": "d331a975-b041-457c-be8c-aa2c48a77e31",
                            "name": "Car Property",
                            "type": "radio",
                            "options": [
                                {
                                    "id": "5fdca54d-6b30-43a6-b5bf-1ce17190ba59",
                                    "name": "Choice 1"
                                },
                                {
                                    "id": "517ed303-17b6-4595-8bb5-a29e3ad1072e",
                                    "name": "Choice 2"
                                }
                            ],
                            "required": True,
                            "per_frame": True,
                            "description": "",
                            "render_value": False,
                            "default_value": None
                        }
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "cuboid"
                },
                {
                    "id": "68499718-1fcc-4435-b97d-92bdbac702fb",
                    "name": "Person",
                    "color": "#FE9573",
                    "properties": [
                        {
                            "id": "fe8518f4-48aa-4d2c-9462-05a24ec0f9cd",
                            "name": "Person Property",
                            "type": "checkbox",
                            "options": [
                                {
                                    "id": "43f204d9-334e-4b74-a5cc-24c21e50ffa7",
                                    "name": "Select 1"
                                },
                                {
                                    "id": "f4c11c64-b18a-4479-81d5-e325b7b4f865",
                                    "name": "Select 2"
                                }
                            ],
                            "required": True,
                            "per_frame": False,
                            "description": "",
                            "render_value": False,
                            "default_value": []
                        }
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "cuboid"
                },
                {
                    "id": "c8174711-3d1a-476f-9d94-94f9c08b426c",
                    "name": "Dog",
                    "color": "#FFAF5A",
                    "properties": [
                        {
                            "id": "3d83e668-78b3-452f-9b57-55164a85fe52",
                            "name": "Dog Property",
                            "type": "free response",
                            "blank": True,
                            "per_frame": False,
                            "constraints": {
                                "digit": True,
                                "space": True,
                                "special": True,
                                "alphabet": True
                            },
                            "description": "",
                            "render_value": False,
                            "default_value": ""
                        }
                    ],
                    "constraints": {},
                    "ai_class_map": [],
                    "annotation_type": "cuboid"
                }
            ],
            "annotation_types": [
                "cuboid"
            ]
        }
    }


@pytest.fixture
def label_info_sample_v6():
    return {
        "version": "0.6.5",
        "meta": {
            "image_info": {},
            "edit_info": {
                "brightness": 0,
                "contrast": 0,
                "elapsed_time": 259,
                "objects": [],
                "canvas_scale": 1,
                "timeline_scale": 1,
                "keyframe_info": {
                    "keyframes": []
                }
            }
        },
        "result": {
            "objects": [
                {
                    "id": "07dbb9e7-1f87-4316-b9a1-2fc187f9e27a",
                    "class_id": "68499718-1fcc-4435-b97d-92bdbac702fb",
                    "tracking_id": 1,
                    "class_name": "Person",
                    "annotation_type": "cuboid",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
                            "annotation": {
                                "coord": {
                                    "position": {
                                        "x": -0.41185502876955127,
                                        "y": -1.6218309550756003,
                                        "z": 0
                                    },
                                    "rotation_quaternion": {
                                        "x": 0,
                                        "y": 0,
                                        "z": 0,
                                        "w": 1
                                    },
                                    "size": {
                                        "x": 10,
                                        "y": 20,
                                        "z": 30
                                    }
                                },
                                "meta": {
                                    "visible": True,
                                    "alpha": 1,
                                    "color": "#FE9573"
                                }
                            }
                        }
                    ],
                    "properties": [
                        {
                            "type": "checkbox",
                            "property_id": "fe8518f4-48aa-4d2c-9462-05a24ec0f9cd",
                            "property_name": "Person Property",
                            "option_ids": [
                                "f4c11c64-b18a-4479-81d5-e325b7b4f865",
                                "43f204d9-334e-4b74-a5cc-24c21e50ffa7"
                            ],
                            "option_names": [
                                "Select 2",
                                "Select 1"
                            ]
                        }
                    ]
                },
                {
                    "id": "0d59c97f-f795-40c4-ad50-c6c5f0ea1452",
                    "class_id": "c8174711-3d1a-476f-9d94-94f9c08b426c",
                    "tracking_id": 2,
                    "class_name": "Dog",
                    "annotation_type": "cuboid",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [],
                            "annotation": {
                                "coord": {
                                    "position": {
                                        "x": -6.6229948630614786,
                                        "y": -31.77720972359645,
                                        "z": 0
                                    },
                                    "rotation_quaternion": {
                                        "x": 0,
                                        "y": 0,
                                        "z": 0,
                                        "w": 1
                                    },
                                    "size": {
                                        "x": 10,
                                        "y": 20,
                                        "z": 30
                                    }
                                },
                                "meta": {
                                    "visible": True,
                                    "alpha": 1,
                                    "color": "#FFAF5A"
                                }
                            }
                        }
                    ],
                    "properties": [
                        {
                            "type": "free response",
                            "property_id": "3d83e668-78b3-452f-9b57-55164a85fe52",
                            "property_name": "Dog Property",
                            "value": "Free response"
                        }
                    ]
                },
                {
                    "id": "35c0c1dd-188e-4498-9f1d-1a3bf2b8b239",
                    "class_id": "2adca68d-9251-4932-85f6-17f1a2312c77",
                    "tracking_id": 3,
                    "class_name": "Car",
                    "annotation_type": "cuboid",
                    "frames": [
                        {
                            "num": 0,
                            "properties": [
                                {
                                    "type": "radio",
                                    "property_id": "d331a975-b041-457c-be8c-aa2c48a77e31",
                                    "property_name": "Car Property",
                                    "option_id": "5fdca54d-6b30-43a6-b5bf-1ce17190ba59",
                                    "option_name": "Choice 1"
                                }
                            ],
                            "annotation": {
                                "coord": {
                                    "position": {
                                        "x": 41.892474849090405,
                                        "y": 36.967404216399615,
                                        "z": 0
                                    },
                                    "rotation_quaternion": {
                                        "x": 0,
                                        "y": 0,
                                        "z": 0,
                                        "w": 1
                                    },
                                    "size": {
                                        "x": 10,
                                        "y": 10,
                                        "z": 10
                                    }
                                },
                                "meta": {
                                    "visible": True,
                                    "alpha": 1,
                                    "color": "#FF625A"
                                }
                            }
                        }
                    ],
                    "properties": []
                }
            ],
            "categories": {
                "properties": [],
                "frames": []
            }
        },
        "tags": {
            "classes_id": [
                "68499718-1fcc-4435-b97d-92bdbac702fb",
                "c8174711-3d1a-476f-9d94-94f9c08b426c",
                "2adca68d-9251-4932-85f6-17f1a2312c77"
            ],
            "categories_id": [],
            "class": [
                "Person",
                "Dog",
                "Car"
            ],
            "classes_count": [
                {
                    "id": "68499718-1fcc-4435-b97d-92bdbac702fb",
                    "name": "Person",
                    "count": 1
                },
                {
                    "id": "c8174711-3d1a-476f-9d94-94f9c08b426c",
                    "name": "Dog",
                    "count": 1
                },
                {
                    "id": "2adca68d-9251-4932-85f6-17f1a2312c77",
                    "name": "Car",
                    "count": 1
                }
            ],
            "classes_annotation_count": [
                {
                    "id": "68499718-1fcc-4435-b97d-92bdbac702fb",
                    "name": "Person",
                    "count": 1
                },
                {
                    "id": "c8174711-3d1a-476f-9d94-94f9c08b426c",
                    "name": "Dog",
                    "count": 1
                },
                {
                    "id": "2adca68d-9251-4932-85f6-17f1a2312c77",
                    "name": "Car",
                    "count": 1
                }
            ],
            "time_spent": 259
        }
    }
