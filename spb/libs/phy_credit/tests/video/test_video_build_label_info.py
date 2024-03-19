import json

from phy_credit.video import LabelInterface, build_label_info


def test_build_label_info_from_scratch(
    label_interface_sample,
    add_object_1,
    add_object_2,
    sample_tag_result_scratch,
    sample_info_result_scratch,
):
    label_interface = LabelInterface.from_dict(label_interface_sample)
    labelInfo = build_label_info(label_interface)
    labelInfo.add_object(**add_object_1)
    labelInfo.add_object(**add_object_2)

    tags = labelInfo.build_tags()
    assert json.dumps(tags, sort_keys=True) == json.dumps(
        sample_tag_result_scratch, sort_keys=True
    )
    # TODO: Comparison is a bit complex because of IDs
    # info = labelInfo.build_info()
    # assert json.dumps(info, sort_keys=True) == json.dumps(
    #     sample_info_result_scratch, sort_keys=True)


def test_build_label_info_with_result(
    label_interface_sample,
    sample_build_result,
    sample_tag_result,
    sample_info_result,
):
    label_interface = LabelInterface.from_dict(label_interface_sample)
    labelInfo = build_label_info(label_interface, result=sample_build_result)

    tags = labelInfo.build_tags()
    assert json.dumps(tags, sort_keys=True) == json.dumps(
        sample_tag_result, sort_keys=True
    )
    info = labelInfo.build_info()
    assert json.dumps(info, sort_keys=True) == json.dumps(
        sample_info_result, sort_keys=True
    )


def test_build_label_info_from_scratch_v6(
    label_interface_sample_v6, label_info_sample_v6
):
    label_interface = LabelInterface.from_dict(label_interface_sample_v6)

    label_info = build_label_info(label_interface)

    label_info.add_object(
        id="12590dbe-72f1-4278-b1fe-b4a0642d55b6",
        class_name="person",
        annotations=[
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
        properties=[],
        tracking_id=None,
    )

    label_info.add_object(
        id="6f4e5ef6-e3ea-4a2d-b0a1-3ebd00b965b3",
        class_name="person",
        annotations=[
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
        properties=[],
        tracking_id=None,
    )

    label_info.add_object(
        id="9b20fabd-9b33-422b-bbb5-870cfaad31b2",
        class_name="poly",
        annotations=[
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
        properties=[],
        tracking_id=None,
    )

    label_info.add_object(
        id="92e28cc4-7eee-4a72-9dc4-383ffd4ecf70",
        class_name="poly_seg",
        annotations=[
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
        properties=[],
        tracking_id=None,
    )

    label_info.add_object(
        id="9ed93108-2c3a-4eba-8613-0633003a239f",
        class_name="face_kp",
        annotations=[
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
        properties=[],
        tracking_id=None,
    )

    label_info.add_object(
        id="10a57f9d-3d04-4ce6-aa8f-516300cd8f75",
        class_name="2d_cuboid",
        annotations=[
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
        properties=[],
        tracking_id=None,
    )

    print(json.dumps(label_info_sample_v6, sort_keys=True, indent=4))
    assert json.dumps(label_info.build_info(), sort_keys=True) == json.dumps(
        label_info_sample_v6, sort_keys=True
    )
