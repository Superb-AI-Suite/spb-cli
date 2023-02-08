import json

from phy_credit.imageV2 import (
    CategorizationDef,
    LabelInterface,
    ObjectDetectionDef,
    PropertyDef,
    PropertyOptionsDef,
    PropertyOptionsItemDef,
)


def test_build_label_interface_v6_from_scratch(label_interface_sample_v6):
    categorization = CategorizationDef.get_default()
    ms_1 = PropertyOptionsItemDef(
        name="ms_1", id="14d9bb96-17cf-44d0-9929-4a9144d85797"
    )
    ms_2 = PropertyOptionsItemDef(
        name="ms_2", id="eba4b04b-b23f-4e65-a020-88e6731300f4"
    )
    ms_g = PropertyOptionsDef(
        name="ms_g",
        id="13cb5be0-33cc-4dda-84c3-ec6afb50680c",
        children=[ms_1, ms_2],
    )
    categorization.add_multiple_selection_category(
        name="ms_cate",
        id="bb0e4235-9d17-40ed-9852-26fc66941d05",
        options=[ms_g],
        is_required=False,
        description="",
        render_value=False,
        default_value=[],
    )
    mc_1 = PropertyOptionsItemDef(
        name="mc_1", id="8831d4a4-5bee-4252-b651-c254b4593490"
    )
    mc_2 = PropertyOptionsItemDef(
        name="mc_2", id="08e881d0-c072-443b-9887-d4042c09a998"
    )
    mc_g = PropertyOptionsDef(
        name="mc_g",
        id="0bd3a095-2e61-4cf3-b7aa-cb58d4ef1912",
        children=[mc_1, mc_2],
    )
    categorization.add_multiple_choice_category(
        name="mc_cate",
        id="0da7b178-df30-47da-bf9b-2daadfbc99d7",
        options=[mc_g],
        is_required=False,
        description="",
        render_value=False,
        default_value="",
    )
    categorization.add_free_response_category(
        name="fr_cate",
        id="69f0963a-0400-4d9a-81fe-b7ef3ded55db",
        blank=True,
        description="",
        render_value=False,
        default_value="",
    )
    assert json.dumps(categorization.to_dict(), sort_keys=True) == json.dumps(
        label_interface_sample_v6["categorization"], sort_keys=True
    )
    object_detection = ObjectDetectionDef.get_default()
    opt_1 = PropertyOptionsItemDef(name="Untitled Option", id="1")
    opt_2 = PropertyOptionsItemDef(name="Untitled Option (1)", id="2")
    box_prop = PropertyDef.multiple_choice_property(
        name="box Property",
        options=[opt_1, opt_2],
        id="c126812b-c013-4f78-b709-7a1764c7c7f3",
        default_value=None,
        is_required=True,
    )
    opt_3 = PropertyOptionsItemDef(name="Untitled Option", id="3")
    opt_4 = PropertyOptionsItemDef(name="Untitled Option (1)", id="4")
    box_prop_1 = PropertyDef.multiple_selection_property(
        name="box Property (1)",
        options=[opt_3, opt_4],
        id="3b09f755-e34f-4d5b-9950-0467d08b5c6b",
        default_value=[],
        is_required=True,
    )
    box_prop_2 = PropertyDef.free_response_property(
        name="box Property (2)",
        id="da2e15ff-98bc-4ef4-a1c9-1830f0e32908",
        blank=False,
        description="",
        render_value=False,
        default_value="",
        constraints={
            "alphabet": True,
            "digit": True,
            "space": True,
            "special": True,
        },
    )
    object_detection.add_box(
        name="box",
        id="346c2e59-0d4d-4818-8cd0-538b157fa06c",
        color="#FF625A",
        properties=[box_prop, box_prop_1, box_prop_2],
    )
    assert json.dumps(
        object_detection.to_dict()["object_classes"][0], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["object_classes"][0],
        sort_keys=True,
    )
    rbox_prop = PropertyDef.multiple_choice_property(
        name="rbox Property",
        options=[opt_1, opt_2],
        id="e8405ff2-a091-4fb3-9ee3-33921491be6b",
        is_required=True,
    )
    rbox_prop_1 = PropertyDef.multiple_selection_property(
        name="rbox Property (1)",
        options=[opt_3, opt_4],
        id="3e75a099-875a-4576-9548-2e2f171e6ad5",
        is_required=True,
    )
    rbox_prop_2 = PropertyDef.free_response_property(
        name="rbox Property (2)",
        id="29243fd2-92c4-4f11-baa0-0e615901039f",
        blank=False,
        description="",
        render_value=False,
        default_value="",
        constraints={
            "alphabet": True,
            "digit": True,
            "space": True,
            "special": True,
        },
    )
    object_detection.add_rbox(
        name="rbox",
        id="e15fae76-1702-44e9-97d8-25bf420e4dbe",
        color="#FE9573",
        properties=[rbox_prop, rbox_prop_1, rbox_prop_2],
    )
    assert json.dumps(
        object_detection.to_dict()["object_classes"][1], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["object_classes"][1],
        sort_keys=True,
    )
    poly_prop = PropertyDef.multiple_choice_property(
        name="poly Property",
        options=[opt_1, opt_2],
        id="d1516ef1-a64d-45c4-9bd0-d26a38658839",
        is_required=True,
    )
    poly_prop_1 = PropertyDef.multiple_selection_property(
        name="poly Property (1)",
        options=[opt_3, opt_4],
        id="7ac2d2d6-bbcf-422e-8b88-0b20335626a0",
        is_required=True,
    )
    poly_prop_2 = PropertyDef.free_response_property(
        name="poly Property (2)",
        id="a2bae19d-b700-4633-81b3-880b6fcc9fc0",
        blank=False,
        description="",
        render_value=False,
        default_value="",
        constraints={
            "alphabet": True,
            "digit": True,
            "space": True,
            "special": True,
        },
    )
    object_detection.add_polyline(
        name="poly",
        id="7c6ab4db-5b0c-4143-b992-6dc732f28870",
        color="#FFAF5A",
        properties=[poly_prop, poly_prop_1, poly_prop_2],
    )
    assert json.dumps(
        object_detection.to_dict()["object_classes"][2], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["object_classes"][2],
        sort_keys=True,
    )
    poly_seg_prop = PropertyDef.multiple_choice_property(
        name="poly_seg Property",
        options=[opt_1, opt_2],
        id="00f9510e-c574-4667-8f76-17c51618e272",
        is_required=True,
    )
    poly_seg_prop_1 = PropertyDef.multiple_selection_property(
        name="poly_seg Property (1)",
        options=[opt_3, opt_4],
        id="1007f627-a13f-4678-a411-871482dfd166",
        is_required=True,
    )
    poly_seg_prop_2 = PropertyDef.free_response_property(
        name="poly_seg Property (2)",
        id="2fccbadc-271f-4124-a3e2-71a759db27c0",
        blank=False,
        description="",
        render_value=False,
        default_value="",
        constraints={
            "alphabet": True,
            "digit": True,
            "space": True,
            "special": True,
        },
    )
    object_detection.add_polygon(
        name="poly_seg",
        id="5a122ca5-b827-4896-9476-ab01d5164853",
        color="#FFCC00",
        properties=[poly_seg_prop, poly_seg_prop_1, poly_seg_prop_2],
    )
    assert json.dumps(
        object_detection.to_dict()["object_classes"][3], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["object_classes"][3],
        sort_keys=True,
    )

    # key point interface can be built on suite project settings.
    face_kp_interface = {
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
    face_kp_prop = PropertyDef.multiple_choice_property(
        name="face_kp Property",
        options=[opt_1, opt_2],
        id="8f826174-6b13-4144-80a9-df236d986c38",
        is_required=True,
    )
    face_kp_prop_1 = PropertyDef.multiple_selection_property(
        name="face_kp Property (1)",
        options=[opt_3, opt_4],
        id="743e543b-c51c-4eac-a29b-f8fa20dd2474",
        is_required=True,
    )
    face_kp_prop_2 = PropertyDef.free_response_property(
        name="face_kp Property (2)",
        id="931e64e5-30b2-4da0-a435-b32f40cad7cb",
        blank=False,
        description="",
        render_value=False,
        default_value="",
        constraints={
            "alphabet": True,
            "digit": True,
            "space": True,
            "special": True,
        },
    )
    object_detection.add_keypoint(
        name="face_kp",
        id="96007e8f-3c76-4359-88d3-27cc3b2e986f",
        keypoint_id="facial-landmark-15",
        color="#FFF73E",
        properties=[face_kp_prop, face_kp_prop_1, face_kp_prop_2],
        keypoint_template=face_kp_interface,
    )
    assert json.dumps(
        object_detection.to_dict()["keypoints"], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["keypoints"],
        sort_keys=True,
    )
    assert json.dumps(
        object_detection.to_dict()["object_classes"][4], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["object_classes"][4],
        sort_keys=True,
    )
    cuboid_2d_prop = PropertyDef.multiple_choice_property(
        name="2d_cuboid Property",
        options=[opt_1, opt_2],
        id="cd1ce733-f0f9-45f2-b2d3-d95016807656",
        is_required=True,
    )
    cuboid_2d_prop_1 = PropertyDef.multiple_selection_property(
        name="2d_cuboid Property (1)",
        options=[opt_3, opt_4],
        id="faf00cd0-99d6-409e-a9ad-75c8830c021a",
        is_required=True,
    )
    cuboid_2d_prop_2 = PropertyDef.free_response_property(
        name="2d_cuboid Property (2)",
        id="b75b8e1f-0e18-405f-bcde-f808fc3595dc",
        blank=False,
        description="",
        render_value=False,
        default_value="",
        constraints={
            "alphabet": True,
            "digit": True,
            "space": True,
            "special": True,
        },
    )
    object_detection.add_2dcuboid(
        name="2d_cuboid",
        id="e970ec55-2dd7-4a94-8a93-ec2b34ed5005",
        color="#DEF00F",
        properties=[cuboid_2d_prop, cuboid_2d_prop_1, cuboid_2d_prop_2],
    )
    assert json.dumps(
        object_detection.to_dict()["object_classes"][5], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["object_classes"][5],
        sort_keys=True,
    )
    object_detection.add_box(
        name="박스", id="414d1b1d-fe14-4e16-af4e-908a5a8147c1", color="#A3EB57"
    )
    assert json.dumps(
        object_detection.to_dict()["object_classes"][6], sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"]["object_classes"][6],
        sort_keys=True,
    )

    label_interface = LabelInterface.get_default()
    label_interface.set_categorization(categorization=categorization)
    label_interface.set_object_detection(object_detection=object_detection)

    assert json.dumps(
        label_interface.object_detection.to_dict(), sort_keys=True
    ) == json.dumps(
        label_interface_sample_v6["object_detection"], sort_keys=True
    )


def test_build_label_interface_v4_from_scratch(label_interface_sample_v4):
    option_a = PropertyOptionsItemDef(
        name="a", id="b2ad46b3-ab05-41e1-be71-6b454daadf8c"
    )
    option_b = PropertyOptionsItemDef(
        name="b", id="cd0df355-75f3-48c0-977a-8f2b7cd8197b"
    )
    option_c = PropertyOptionsItemDef(
        name="c", id="de5f7920-e9bc-441f-b4c0-3ebd8fe7013a"
    )
    option_alphabet = PropertyOptionsDef(
        name="alphabet",
        id="f2c19b26-37fa-4b74-baaf-1105a4b51841",
        children=[option_a, option_b, option_c],
    )

    option_1 = PropertyOptionsItemDef(
        name="1", id="a1200bca-41c2-43e5-85d9-4d51554d552b"
    )
    option_2 = PropertyOptionsItemDef(
        name="2", id="d6711d55-aae5-4dbe-a92e-55d87c1c02ef"
    )
    option_3 = PropertyOptionsItemDef(
        name="3", id="87c0bf6a-6dfb-46d8-99b4-5112340529c9"
    )
    option_number = PropertyOptionsDef(
        name="number",
        id="4964136d-8ebf-4692-98ee-8f81b0fb1234",
        children=[option_1, option_2, option_3],
    )

    categorization = CategorizationDef.get_default()
    categorization.add_multiple_selection_category(
        name="Root",
        id="root",
        options=[option_alphabet, option_number],
        is_required=True,
    )

    # print(categorization.to_dict())
    object_detection = ObjectDetectionDef.get_default()
    pc_option_1 = PropertyOptionsItemDef(name="1", id="1")
    pc_option_2 = PropertyOptionsItemDef(name="2", id="2")
    pc_properties = PropertyDef.multiple_choice_property(
        name="pc",
        id="5b65d4ae-2737-4de8-a460-70a5aab4eba2",
        options=[pc_option_1, pc_option_2],
        is_required=True,
    )
    ps_option_1 = PropertyOptionsItemDef(name="1", id="3")
    ps_option_2 = PropertyOptionsItemDef(name="2", id="4")
    ps_properties = PropertyDef.multiple_selection_property(
        name="ps",
        id="f7eebc07-155b-48f3-847d-5501668044ad",
        options=[ps_option_1, ps_option_2],
        is_required=True,
    )

    object_detection.add_box(
        name="bb",
        id="6b5ec356-cf5d-4e73-9cfb-1f7a3393f4a9",
        color="#FF625A",
        properties=[pc_properties, ps_properties],
    )

    label_interface = LabelInterface.get_default()

    label_interface.set_categorization(categorization=categorization)
    label_interface.set_object_detection(object_detection=object_detection)

    assert label_interface_sample_v4 == label_interface.to_dict()
    # print(json.dumps(label_interface.to_dict(), indent=4))
    # # This will print the result below


"""
{
    "type": "image-siesta",
    "version": "0.4.7",
    "data_type": "image",
    "categorization": {
        "properties": [
            {
                "id": "root",
                "name": "Root",
                "default_value": [],
                "description": "",
                "options": [
                    {
                        "name": "alphabet",
                        "id": "f2c19b26-37fa-4b74-baaf-1105a4b51841",
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
                        "name": "number",
                        "id": "4964136d-8ebf-4692-98ee-8f81b0fb1234",
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
                "render_value": false,
                "required": true,
                "type": "checkbox"
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
                        "default_value": null,
                        "description": "",
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
                        "render_value": false,
                        "required": true,
                        "type": "radio"
                    },
                    {
                        "id": "f7eebc07-155b-48f3-847d-5501668044ad",
                        "name": "ps",
                        "default_value": [],
                        "description": "",
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
                        "render_value": false,
                        "required": true,
                        "type": "checkbox"
                    }
                ],
                "constraints": {},
                "ai_class_map": [],
                "annotation_type": "box"
            }
        ],
        "annotation_types": [
            "box",
            "image category"
        ]
    }
}
"""
