from phy_credit.video import LabelInfo

def test_build_label_info_from_scratch():
    label_interface_sample = {
        "version": "0.1.0",
        "data_type": "image sequence",
        "categorization": {
            "properties": []
        },
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
                        {
                            "class_ids": [
                                "1"
                            ],
                            "engine_id": "co_20200526"
                        }
                    ],
                    "annotation_type": "box"
                },
                {
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
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
                }
            ],
            "annotation_types": [
                "box",
                "polygon"
            ]
        }
    }
    labelInfo = LabelInfo(label_interface_sample)
    labelInfo.add_object(tracking_id=1, class_name='Person', annotations=[
        {
            'frame_num': 0,
            'coord': {
                "x": 1245.1356238698008,
                "y": 355.4430379746835,
                "width": 232.40506329113896,
                "height": 482.386980108499
            }
        },
        {
            'frame_num': 1,
            'coord': {
                "x": 1032.2603978300176,
                "y": 421.8444846292944,
                "width": 199.20433996383372,
                "height": 410.1265822784811
            }
        },
    ])
    labelInfo.add_object(tracking_id=2, class_name='Chair', annotations=[
        {
            'frame_num': 0,
            'coord': {
                "points": [
                    {
                        "x": 723.6889692585893,
                        "y": 207.0162748643761
                    },
                    {
                        "x": 737.3598553345388,
                        "y": 312.47739602169975
                    },
                    {
                        "x": 706.1121157323688,
                        "y": 310.52441229656415
                    },
                    {
                        "x": 739.3128390596743,
                        "y": 341.7721518987341
                    },
                    {
                        "x": 737.3598553345388,
                        "y": 363.254972875226
                    },
                    {
                        "x": 883.8336347197104,
                        "y": 357.3960216998191
                    },
                    {
                        "x": 876.021699819168,
                        "y": 322.2423146473779
                    },
                    {
                        "x": 911.1754068716092,
                        "y": 273.41772151898726
                    },
                    {
                        "x": 838.9150090415911,
                        "y": 298.8065099457504
                    },
                    {
                        "x": 807.6672694394211,
                        "y": 191.3924050632911
                    }
                ]
            }
        },
    ])

    import pprint
    pprint.pprint(labelInfo.build_tags())
    pprint.pprint(labelInfo.build_info())

def test_build_label_info_with_result():
    label_interface_sample = {
        "version": "0.1.0",
        "data_type": "image sequence",
        "categorization": {
            "properties": []
        },
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
                        {
                            "class_ids": [
                                "1"
                            ],
                            "engine_id": "co_20200526"
                        }
                    ],
                    "annotation_type": "box"
                },
                {
                    "id": "1c4c4891-9382-496d-8895-a004d488b38e",
                    "name": "Chair",
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
                }
            ],
            "annotation_types": [
                "box",
                "polygon"
            ]
        }
    }
    labelInfo = LabelInfo(
        label_interface_sample,
        result={
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
                                    "height": 472.62206148282087
                                },
                                "meta": {}
                            },
                            "properties": []
                        },
                        {
                            "num": 1,
                            "annotation": {
                                "coord": {
                                    "x": 1036.166365280289,
                                    "y": 415.9855334538878,
                                    "width": 195.2983725135623,
                                    "height": 423.7974683544303
                                },
                                "meta": {}
                            },
                            "properties": []
                        },
                        {
                            "num": 3,
                            "annotation": {
                                "coord": {
                                    "x": 1036.166365280289,
                                    "y": 415.9855334538878,
                                    "width": 195.2983725135623,
                                    "height": 423.7974683544303
                                },
                                "meta": {}
                            },
                            "properties": []
                        }
                    ]
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
                                            "y": 199.2043399638336
                                        },
                                        {
                                            "x": 725.641952983725,
                                            "y": 302.71247739602165
                                        },
                                        {
                                            "x": 704.1591320072331,
                                            "y": 308.5714285714285
                                        },
                                        {
                                            "x": 764.7016274864374,
                                            "y": 337.86618444846283
                                        },
                                        {
                                            "x": 760.7956600361662,
                                            "y": 363.254972875226
                                        },
                                        {
                                            "x": 942.4231464737792,
                                            "y": 345.6781193490053
                                        },
                                        {
                                            "x": 874.0687160940323,
                                            "y": 304.66546112115725
                                        },
                                        {
                                            "x": 930.7052441229654,
                                            "y": 253.88788426763105
                                        },
                                        {
                                            "x": 827.1971066907773,
                                            "y": 199.2043399638336
                                        }
                                    ]
                                },
                                "meta": {}
                            },
                            "properties": []
                        }
                    ]
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
                                            "y": 479.0322580645161
                                        },
                                        {
                                            "x": 594.1935483870967,
                                            "y": 670.6451612903226
                                        },
                                        {
                                            "x": 936.0483870967743,
                                            "y": 757.7419354838709
                                        },
                                        {
                                            "x": 942.5806451612904,
                                            "y": 733.7903225806451
                                        },
                                        {
                                            "x": 1007.9032258064516,
                                            "y": 540
                                        }
                                    ]
                                },
                                "meta": {}
                            },
                            "properties": []
                        }
                    ]
                }
            ],
            "categories": {
                "properties": [],
                "frames": []
            }
        }
    )

    import pprint
    pprint.pprint(labelInfo.build_tags())
    pprint.pprint(labelInfo.build_info())

if __name__ == '__main__':
    # in a rush...
    test_build_label_info_from_scratch()
    test_build_label_info_with_result()
