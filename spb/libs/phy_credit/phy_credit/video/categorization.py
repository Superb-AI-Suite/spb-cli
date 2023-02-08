from uuid import uuid4

from .property import PropertyDef


class CategorizationDef:
    def __init__(self, properties: list):
        self.properties = properties

    @classmethod
    def get_default(cls):
        return cls(properties=[])

    def add_multiple_choice_category(
        self,
        name: str,
        options: list,
        id: str = None,
        is_required: bool = False,
        description: str = "",
        render_value: bool = False,
        default_value: bool = "",
        is_per_frame: bool = False,
    ):
        for category in self.properties:
            if category["name"] == name:
                return print(f"[ERROR] {name} already exists")
        self.properties.append(
            PropertyDef.multiple_choice_property(
                name=name,
                options=options,
                id=id,
                default_value=default_value,
                description=description,
                render_value=render_value,
                is_required=is_required,
                is_per_frame=is_per_frame,
            )
        )

    def add_multiple_selection_category(
        self,
        name: str,
        options: list,
        id: str = None,
        is_required: bool = False,
        description: str = "",
        render_value: bool = False,
        default_value: list = [],
        is_per_frame: bool = False,
    ):
        for category in self.properties:
            if category["name"] == name:
                return print(f"[ERROR] {name} already exists")
        self.properties.append(
            PropertyDef.multiple_selection_property(
                name=name,
                options=options,
                id=id,
                default_value=default_value,
                description=description,
                render_value=render_value,
                is_required=is_required,
                is_per_frame=is_per_frame,
            )
        )

    def add_free_response_category(
        self,
        name: str,
        id: str = None,
        blank: bool = True,
        constraints: dict = {
            "digit": True,
            "space": True,
            "special": True,
            "alphabet": True,
        },
        description: str = "",
        render_value: bool = False,
        default_value: str = "",
        is_per_frame: bool = False,
    ):
        for category in self.properties:
            if category["name"] == name:
                return print(f"[ERROR] {name} already exists")
        id = str(uuid4()) if id is None else id
        self.properties.append(
            PropertyDef.free_response_property(
                name=name,
                id=id,
                blank=blank,
                constraints=constraints,
                description=description,
                render_value=render_value,
                default_value=default_value,
                is_per_frame=is_per_frame,
            )
        )

    def remove_category(self, name: str):
        for category in self.properties:
            if category["name"] == name:
                self.properties.remove(category)
                return

    def remove_category_by_id(self, id: str):
        for category in self.result["properties"]:
            if category["id"] == id:
                self.properties.remove(category)
                return

    def to_dict(self):
        return {
            "properties": self.properties,
        }

    @classmethod
    def from_dict(cls, categorization_dict: dict):
        return cls(properties=categorization_dict["properties"])
