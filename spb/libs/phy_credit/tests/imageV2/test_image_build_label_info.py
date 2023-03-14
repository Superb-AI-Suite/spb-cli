import json

from phy_credit.imageV2 import (
    CategorizationDef,
    LabelInterface,
    build_label_info,
)


def test_build_label_info_from_scratch(
    label_interface_sample,
    add_object_1,
    add_object_2,
    add_object_3,
    add_object_4,
    sample_tag_result,
    sample_info_result,
):
    label_interface = LabelInterface.from_dict(label_interface_sample)
    labelInfo = build_label_info(label_interface)
    labelInfo.add_object(**add_object_1)
    labelInfo.add_object(**add_object_2)
    labelInfo.add_object(**add_object_3)
    labelInfo.add_object(**add_object_4)

    tags = labelInfo.build_tags()
    assert json.dumps(tags, sort_keys=True) == json.dumps(
        sample_tag_result, sort_keys=True
    )
    # TODO: Comparison is a bit complex because of IDs
    # info = labelInfo.build_info()
    # assert json.dumps(info, sort_keys=True) == json.dumps(
    #     sample_info_result, sort_keys=True)


def test_build_label_info_from_result(
    label_interface_sample,
    sample_build_result,
    sample_tag_result,
    sample_info_result,
):
    label_interface = LabelInterface.from_dict(label_interface_sample)
    labelInfo = build_label_info(
        label_interface=label_interface,
        result=sample_build_result,
    )

    tags = labelInfo.build_tags()
    assert json.dumps(tags, sort_keys=True) == json.dumps(
        sample_tag_result, sort_keys=True
    )
    info = labelInfo.build_info()
    assert json.dumps(info, sort_keys=True) == json.dumps(
        sample_info_result, sort_keys=True
    )


def test_build_label_info_from_scratch_v4(
    label_interface_sample_v4,
    add_object_1,
    add_object_2,
    set_category_1,
    sample_tag_result_v4,
    sample_info_result_v4,
):

    label_interface = LabelInterface.from_dict(label_interface_sample_v4)
    label_info = build_label_info(label_interface)
    # box_creator = label_info.get_box_creator()
    label_info.add_object(**add_object_1)
    label_info.add_object(**add_object_2)
    # label_info.add_object(box_creator.from_dict(add_object_1))
    # label_info.add_object(box_creator.from_dict(add_object_2))
    categorization = CategorizationDef.from_dict(set_category_1)
    label_info.set_categories(categorization)

    tags = label_info.build_tags()
    assert json.dumps(tags, sort_keys=True) == json.dumps(
        sample_tag_result_v4, sort_keys=True
    )
    assert len(tags["classes_properties_count"]) == 4
    # # TODO: Comparison is a bit complex because of IDs
    # info = label_info.build_info()
    # assert json.dumps(info, sort_keys=True) == json.dumps(
    #     sample_info_result_v4, sort_keys=True
    # )


# # using creators
# def test_build_label_info_from_scratch_v6(
#     label_interface_sample_v6, label_info_sample_v6
# ):
#     label_interface = LabelInterface.from_dict(label_interface_sample_v6)
#     label_info = build_label_info(label_interface)
#     box_creator = label_info.get_box_creator()
#
#     box = box_creator.create(
#         id="12590dbe-72f1-4278-b1fe-b4a0642d55b6",
#         class_name="box",
#         coord={"x": 26.3, "y": 24.1, "width": 36.3, "height": 25.2},
#     )
#
#     label_info.add_object(box)
#
#     rbox_creator = label_info.get_rotated_box_creator()
#
#     rbox = rbox_creator.create(
#         id="6f4e5ef6-e3ea-4a2d-b0a1-3ebd00b965b3",
#         class_name="rbox",
#         coord={
#             "cx": 55.6,
#             "cy": 84.0,
#             "width": 27.8,
#             "height": 22.4,
#             "angle": 24.3,
#         },
#     )
#
#     label_info.add_object(rbox)
#
#     polyline_creator = label_info.get_polyline_creator()
#
#     polyline = polyline_creator.create(
#         id="9b20fabd-9b33-422b-bbb5-870cfaad31b2",
#         class_name="poly",
#         coord={
#             "points": [
#                 [
#                     {"x": 20.5, "y": 144.8},
#                     {"x": 40.9, "y": 117.3},
#                     {"x": 40.8, "y": 145.8},
#                 ]
#             ]
#         },
#     )
#
#     label_info.add_object(polyline)
#
#     polygon_creator = label_info.get_polygon_creator()
#
#     polygon = polygon_creator.create(
#         id="92e28cc4-7eee-4a72-9dc4-383ffd4ecf70",
#         class_name="poly_seg",
#         coord={
#             "points": [
#                 [
#                     [
#                         {"x": 21.5, "y": 191.2},
#                         {"x": 24.2, "y": 167.7},
#                         {"x": 28.1, "y": 158.1},
#                         {"x": 41.2, "y": 161.9},
#                         {"x": 21.5, "y": 191.2},
#                     ],
#                 ]
#             ]
#         },
#     )
#
#     label_info.add_object(polygon)
#
#     keypoint_cretor = label_info.get_keypoint_creator()
#     default_kp_coord = keypoint_cretor.get_default_keypoint_coord(
#         keypoint_interface_id="facial-landmark-15"
#     )
#     keypoint = keypoint_cretor.create(
#         id="9ed93108-2c3a-4eba-8613-0633003a239f",
#         class_name="face_kp",
#         coord=default_kp_coord,
#     )
#
#     label_info.add_object(keypoint)
#
#     cuboid2d_creator = label_info.get_2D_cubid_creator()
#
#     cuboid_2d = cuboid2d_creator.create(
#         id="10a57f9d-3d04-4ce6-aa8f-516300cd8f75",
#         class_name="2d_cuboid",
#         coord={
#             "near": {"x": 15.1, "y": 225.7, "width": 44.9, "height": 37.6},
#             "far": {"x": 83.2, "y": 239.3, "width": 5.4, "height": 16.5},
#         },
#     )
#
#     label_info.add_object(cuboid_2d)
#
#     label_info.build_info()
#
#     assert json.dumps(label_info.build_info(), sort_keys=True) == json.dumps(
#         label_info_sample_v6, sort_keys=True
#     )
#     # assert json.dumps(tags, sort_keys=True) == json.dumps(
#     #     sample_tag_result_v4, sort_keys=True
