# import numpy as np
# import cv2
# import math

# from spb.utils.color_utils import hex_to_rgb, rgb_to_hex


# def mask_from_label(
#     label_interface: dict,
#     meta_info: dict,
#     label_info: dict,
#     skip_box:bool=False,
#     skip_rbox:bool=False,
#     skip_polygon:bool=False,
#     skip_polyline:bool=False,
#     skip_keypoint:bool=False,
#     background_color:tuple=(0,0,0),
# ):
#     image_width = meta_info["image_info"]["width"]
#     image_height = meta_info["image_info"]["height"]

#     # mask
#     mask = np.zeros((image_height, image_width, 3), dtype=np.uint8)
#     mask[:] = background_color

#     # keypoints
#     edge_info = dict()
#     node_info = dict()
#     if label_interface["object_detection"]["keypoints"]:
#         keypoint_infos = label_interface["object_detection"]["keypoints"]
#         for keypoint_info in keypoint_infos:
#             edges = keypoint_info["edges"]
#             for edge in edges:
#                 edge_info[edge["u"], edge["v"]] = edge["color"]
#             points = keypoint_info["points"]
#             for point in points:
#                 node_info[point["name"]] = point["color"]
    
#     # object detection
#     objects = label_info["objects"]
#     layered_objects = sorted(objects, key=lambda obj: obj["annotation"]["meta"]["z_index"])

#     for obj in layered_objects:
#         annotation_type = obj["annotation_type"]
#         if annotation_type == "box":
#             if not skip_box:
#                 coord = obj["annotation"]["coord"]
#                 points_to_mask = np.array(
#                     [
#                         [coord["x"], coord["y"]],
#                         [coord["x"], coord["y"] + coord["height"]],
#                         [coord["x"] + coord["width"], coord["y"] + coord["height"]],
#                         [coord["x"] + coord["width"], coord["y"]],
#                     ]
#                 )
#                 cv2.fillPoly(
#                     mask,
#                     np.int32([points_to_mask]),
#                     hex_to_rgb(obj["annotation"]["meta"]["color"]),
#                 )

#         elif annotation_type == "rbox":
#             if not skip_rbox:
#                 coord = obj["annotation"]["coord"]
#                 polygon_points = rotate_points(coord, coord["angle"])
#                 points_to_mask = np.array(
#                     [[points["x"], points["y"]] for points in polygon_points]
#                 )
#                 cv2.fillPoly(
#                     mask,
#                     np.int32([points_to_mask]),
#                     hex_to_rgb(obj["annotation"]["meta"]["color"]),
#                 )

#         elif annotation_type == "polygon":
#             if not skip_polygon:
#                 points = obj["annotation"]["coord"]["points"]
#                 for segment_contour in points:
#                     points_to_mask = []
#                     for index, contour_obj in enumerate(segment_contour):
#                         inner_points = np.array(
#                             [[pt["x"], pt["y"]] for pt in contour_obj]
#                         )
#                         points_to_mask.append(np.int32(inner_points))
#                     cv2.fillPoly(
#                         mask,
#                         points_to_mask,
#                         hex_to_rgb(obj["annotation"]["meta"]["color"]),
#                     )

#         elif annotation_type == "polyline":
#             if not skip_polyline:
#                 points = obj["annotation"]["coord"]["points"]
#                 for polyline in points:
#                     points_to_mask = np.array([[pt["x"], pt["y"]] for pt in polyline])
#                     is_closed = False
#                     cv2.polylines(
#                         mask,
#                         np.int32([points_to_mask]),
#                         is_closed,
#                         hex_to_rgb(obj["annotation"]["meta"]["color"]),
#                         thickness=1,
#                     )

#         elif annotation_type == "keypoint":
#             if not skip_keypoint:
#                 # mask points
#                 points = obj["annotation"]["coord"]["points"]
#                 for pt in points:
#                     if pt["state"]["visible"]:
#                         cv2.circle(
#                             mask,
#                             (int(pt["x"]), int(pt["y"])),
#                             radius=1,
#                             color=hex_to_rgb(node_info[pt["name"]]),
#                             thickness=4,
#                         )
#                 # mask edges
#                 for (u, v), edge_color in edge_info.items():
#                     if points[u]["state"]["visible"] and points[v]["state"]["visible"]:
#                         cv2.line(
#                             mask,
#                             (int(points[u]["x"]), int(points[u]["y"])),
#                             (int(points[v]["x"]), int(points[v]["y"])),
#                             hex_to_rgb(edge_color),
#                             thickness=1,
#                         )
#         else: # TODO raise error message
#             print(f"not implemented for type: {annotation_type}")

#     return mask


# def rotate_points(coord, angle):
#     width = coord["width"]
#     height = coord["height"]
#     center_point = [coord["cx"], coord["cy"]]
#     origin_left_top_point = [-width / 2, -height / 2]
#     origin_right_top_point = [width / 2, -height / 2]
#     origin_right_bottom_point = [width / 2, height / 2]
#     origin_left_bottom_point = [-width / 2, height / 2]
#     origin_points = [
#         origin_left_top_point,
#         origin_right_top_point,
#         origin_right_bottom_point,
#         origin_left_bottom_point,
#         origin_left_top_point,
#     ]

#     rotated_points = []
#     for pts in origin_points:
#         rotated_points.append(
#             [
#                 (pts[0] * (math.cos(-(90 + angle))))
#                 - (pts[1] * (math.sin(-(90 + angle))))
#                 + center_point[0],
#                 (pts[0] * (math.sin(-(90 + angle))))
#                 + (pts[1] * (math.cos(-(90 + angle))))
#                 + center_point[1],
#             ]
#         )

#     polygon_points = []
#     for obj in rotated_points:
#         polygon_points.append({"x": obj[0], "y": obj[1]})

#     return polygon_points
