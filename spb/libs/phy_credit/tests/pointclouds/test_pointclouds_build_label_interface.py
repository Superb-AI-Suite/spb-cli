import json

from phy_credit.pointclouds import (
    LabelInterface,
    ObjectTrackingDef,
    PropertyDef,
    PropertyOptionsDef,
    PropertyOptionsItemDef,
)
from phy_credit.common import (
    ClassType,
)


def test_build_label_interface_v6(label_interface_sample_v6):
    object_tracking = ObjectTrackingDef().get_default()
    opt_1 = PropertyOptionsItemDef(
        name="Choice 1", id="5fdca54d-6b30-43a6-b5bf-1ce17190ba59")
    opt_2 = PropertyOptionsItemDef(
        name="Choice 2", id="517ed303-17b6-4595-8bb5-a29e3ad1072e")
    car_prop = PropertyDef.multiple_choice_property(
        name="Car Property",
        id="d331a975-b041-457c-be8c-aa2c48a77e31",
        options=[opt_1, opt_2],
        default_value=None,
        is_required=True,
        is_per_frame=True
    )
    object_tracking.add_cuboid(
        id="2adca68d-9251-4932-85f6-17f1a2312c77",
        name="Car",
        color="#FF625A",
        properties=[car_prop]
    )

    opt_3 = PropertyOptionsItemDef(
        name="Select 1", id="43f204d9-334e-4b74-a5cc-24c21e50ffa7")
    opt_4 = PropertyOptionsItemDef(
        name="Select 2", id="f4c11c64-b18a-4479-81d5-e325b7b4f865")
    person_prop = PropertyDef.multiple_selection_property(
        name="Person Property",
        id="fe8518f4-48aa-4d2c-9462-05a24ec0f9cd",
        options=[opt_3, opt_4],
        default_value=[],
        is_required=True,
        is_per_frame=False
    )
    object_tracking.add_cuboid(
        id="68499718-1fcc-4435-b97d-92bdbac702fb",
        name="Person",
        color="#FE9573",
        properties=[person_prop]
    )

    dog_prop = PropertyDef.free_response_property(
        name="Dog Property",
        id="3d83e668-78b3-452f-9b57-55164a85fe52",
        blank=True,
        is_per_frame=False,
        default_value=""
    )
    object_tracking.add_cuboid(
        id="c8174711-3d1a-476f-9d94-94f9c08b426c",
        name="Dog",
        color="#FFAF5A",
        properties=[dog_prop]
    )

    object_tracking.add_object_group(
        name="Organism",
        id="92851114-f8ab-46f0-b472-9b81032afb02",
        groups=["Person", "Dog"]
    )

    object_tracking.add_object_group(
        name="Vehicles",
        id="4ab741f2-1522-417e-8989-ae7629a25606",
        groups=["Car"]
    )

    label_interface = LabelInterface.get_default()
    label_interface.set_object_tracking(object_tracking)

    car_object = label_interface.object_tracking.get_object_class(
        name="Car", annotation_type=ClassType.CUBOID)
    person_object = label_interface.object_tracking.get_object_class(
        name="Person", annotation_type=ClassType.CUBOID)
    dog_object = label_interface.object_tracking.get_object_class(
        name="Dog", annotation_type=ClassType.CUBOID)

    label_interface.object_tracking.set_object_group(
        name="Organism",
        id="92851114-f8ab-46f0-b472-9b81032afb02",
        groups=[person_object, dog_object]
    )
    label_interface.object_tracking.set_object_group(
        name="Vehicles",
        id="4ab741f2-1522-417e-8989-ae7629a25606",
        groups=[car_object]
    )

    assert json.dumps(label_interface.to_dict(), sort_keys=True) == json.dumps(
        label_interface_sample_v6, sort_keys=True
    )
