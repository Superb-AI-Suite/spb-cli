from .. import __version__
from .label_interface import LabelInterface


class ProjectInfo:
    @staticmethod
    def get_default_w_label_interface(
        name: str,
        label_interface: LabelInterface,
        allow_advanced_qa: bool = False,
        is_public: bool = False,
    ):
        return {
            "name": name,
            "workapp": "image-siesta",
            "label_interface": label_interface.to_dict(),
            "settings": {"allow_advanced_qa": allow_advanced_qa},
            "is_public": is_public,
        }

    @staticmethod
    def get_default(name: str):
        return ProjectInfo.get_default_w_label_interface(
            name=name, label_interface=LabelInterface.get_default()
        )
