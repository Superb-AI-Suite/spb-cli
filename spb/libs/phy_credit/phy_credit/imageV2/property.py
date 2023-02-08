from uuid import uuid4


class PropertyOptionsDef:
    # children is list of type (PropertyOptionsDef | PropertyOptionsItemDef)
    def __init__(self, name: str, id: str = None, children=[]):
        self.name = name
        self.id = str(uuid4()) if id is None else id
        self.children = children

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "children": [child.to_dict() for child in self.children],
        }


class PropertyOptionsItemDef:
    def __init__(self, name: str, id: str = None):
        self.name = name
        self.id = str(uuid4()) if id is None else id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class PropertyDef:
    # options is list of type (PropertyOptionsDef | PropertyOptionsItemDef)
    @staticmethod
    def multiple_choice_property(
        name: str,
        options: list,
        id: str = None,
        default_value: str = None,
        description: str = "",
        render_value: bool = False,
        is_required: bool = False,
    ):
        # options_list = [{"id": str(uuid4()), "name": item} for item in options]
        options_list = [_options.to_dict() for _options in options]
        id = str(uuid4()) if id is None else id
        return {
            "id": id,
            "name": name,
            "default_value": default_value,
            "description": description,
            "options": options_list,
            "render_value": render_value,
            "required": is_required,
            "type": "radio",
        }

    # options is list of type (PropertyOptionsDef | PropertyOptionsItemDef)
    @staticmethod
    def multiple_selection_property(
        name: str,
        options: list,
        id: str = None,
        default_value: list = [],
        description: str = "",
        render_value: bool = False,
        is_required: bool = False,
    ):
        # options_list = [{"id": str(uuid4()), "name": item} for item in options]
        options_list = [_options.to_dict() for _options in options]
        id = str(uuid4()) if id is None else id
        return {
            "id": id,
            "name": name,
            "default_value": default_value,
            "description": description,
            "options": options_list,
            "render_value": render_value,
            "required": is_required,
            "type": "checkbox",
        }

    @staticmethod
    def free_response_property(
        name: str,
        blank: bool = True,
        constraints: dict = {
            "digit": True,
            "space": True,
            "special": True,
            "alphabet": True,
        },
        id: str = None,
        default_value: str = "",
        description: str = "",
        render_value: bool = False,
    ):
        id = str(uuid4()) if id is None else id
        return {
            "id": id,
            "name": name,
            "default_value": default_value,
            "description": description,
            "constraints": constraints,
            "render_value": render_value,
            "blank": blank,
            "type": "free response",
        }
