from phy_credit.common.image_utils import (
    calculate_imageV2_properties_count,
    count_properties,
)


def test_count_properties(mock_preprocessed_properties, mock_count_properties_result):
    input = mock_preprocessed_properties
    expected = mock_count_properties_result
    assert all([a == b for a, b in zip(count_properties(input), expected)])


def test_calculate_image_properties_count(mock_image_objects_with_properties, mock_image_classes_properties_count):
    objects = mock_image_objects_with_properties
    expected = mock_image_classes_properties_count
    result = calculate_imageV2_properties_count(objects)
    assert all([a == b for a, b in zip(result, expected)])
