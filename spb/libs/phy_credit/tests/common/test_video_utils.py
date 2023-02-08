from phy_credit.common.utils import (
    expand_options,
    remove_free_response,
)
from phy_credit.common.video_utils import (
    calculate_video_properties_count,
    flatten_video_obj_properties,
    preprocess_video_obj_properties,
)


# preprocessing: step 1
def test_flatten_video_object_properties(mock_video_objects, num_properties_flattened):
    assert len(flatten_video_obj_properties([])) == 0
    assert (
        len(flatten_video_obj_properties(mock_video_objects))
        == num_properties_flattened
    )


# preprocessing: step 2
def test_remove_free_response(mock_video_objects, num_properties_removed_free_response):
    input = flatten_video_obj_properties(mock_video_objects)
    assert len(remove_free_response(input)
               ) == num_properties_removed_free_response


# preprocessing: step 3
def test_expand_options(mock_video_objects, num_properties_expanded_options):
    input = remove_free_response(
        flatten_video_obj_properties(mock_video_objects))
    assert len(expand_options(input)) == num_properties_expanded_options


# preprocessing: combined steps
def test_preprocess_video_objects(mock_video_objects, num_properties_preprocessed):
    result = preprocess_video_obj_properties(mock_video_objects)
    assert len(result) == num_properties_preprocessed


# counting: combined steps
def test_calculate_video_properties_count(mock_video_classes_properties_count, mock_video_objects):
    assert calculate_video_properties_count([]) == []
    expected = mock_video_classes_properties_count
    for (result, expected) in zip(
        calculate_video_properties_count(mock_video_objects), expected
    ):
        assert result == expected
